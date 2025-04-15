# 📂 ======================= 基本套件導入 =======================

import random                            # 🎲 隨機模組
import discord                           # 🤖 Discord Embed 嵌入訊息
import asyncio                         # ⏱️ 非同步倒數
import pytz                            # 🌏 時區設定
from datetime import datetime          # 📅 取得日期時間
import os                              # 🗂️ 路徑操作
import yaml                            # 📒 YAML 讀取
from utils.file_utils import check_file_exists  # 🧩 工具：檢查檔案是否存在
from utils.log_utils import log_message, exception_logger         # 📝 統一日誌管理

# 📂 ======================= 資料檔案路徑 =======================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # 📁 當前目錄
DATA_DIR = os.path.join(BASE_DIR, 'data')               # 📂 資料夾路徑

# 🗂️ 各 YAML 路徑
ANIME_FILE = os.path.join(DATA_DIR, "anime_quotes.yaml")
COLOR_FILE = os.path.join(DATA_DIR, "colors.yaml")
COUNTDOWN_FILE = os.path.join(DATA_DIR, "countdown_messages.yaml")
PROBABILITY_FILE = os.path.join(DATA_DIR, "fortune_probability.yaml")
FORTUNE_FILE = os.path.join(DATA_DIR, "fortunes.yaml")
SUGGESTIONS_FILE = os.path.join(DATA_DIR, "suggestions.yaml")

# 📂 ======================= 通用 YAML 讀取工具 =======================

def load_yaml(file_path: str, default=None):
    """
    📖 通用 YAML 讀取器
    :param file_path: YAML 檔案路徑
    :param default: 預設值
    :return: 讀取結果
    """
    if not check_file_exists(file_path):
        log_message(f"⚠️ 找不到 YAML：{file_path}，使用預設值。", level="WARNING", print_to_console=False)
        return default or {}

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file) or default
    except Exception as e:
        log_message(f"❌ 讀取 YAML 失敗：{e}｜檔案：{file_path}", level="ERROR", print_to_console=False)
        return default or {}

# 📂 ======================= 讀取 YAML 資料 =======================

# 🧩 運勢內容
fortune_data = load_yaml(FORTUNE_FILE, {})
# 🧩 機率配置
probability_data = load_yaml(PROBABILITY_FILE, {})
# 🧩 倒數訊息
countdown_messages = load_yaml(COUNTDOWN_FILE, {}).get("countdown_messages", ["請稍候 {count} 秒..."])
# 🧩 幸運顏色
lucky_colors = load_yaml(COLOR_FILE, {}).get("colors", ["黑色"])
# 🧩 小建議
suggestions = load_yaml(SUGGESTIONS_FILE, {}).get("suggestions", ["保持微笑"])
# 🧩 動漫金句
anime_quotes = load_yaml(ANIME_FILE, {}).get("anime_quotes", ["要堅強！"])

# 📂 ======================= 功能邏輯 =======================

# 🆕 ✅ 使用獨立亂數生成器，讓倒數訊息每次都隨機
countdown_rng = random.Random()

def get_random_countdown_message(count: int) -> str:
    """
    ⏳ 取得隨機倒數訊息
    """
    return countdown_rng.choice(countdown_messages).format(count=count)

def get_random_color() -> str:
    """
    🎨 取得隨機幸運顏色（每日固定）
    """
    return random.choice(lucky_colors)

def get_random_suggestion() -> str:
    """
    💡 取得隨機小建議（每日固定）
    """
    return random.choice(suggestions)

def get_random_anime_quote() -> str:
    """
    🎴 取得隨機動漫金句（每日固定）
    """
    return random.choice(anime_quotes)

def pick_fortune():
    """
    🎯 核心邏輯：挑選運勢結果
    :return: 運勢名稱 + 對應訊息列表
    """
    # 分層邏輯
    level_choice = random.choices(
        population=["special", "normal"],
        weights=[probability_data.get("level", {}).get("special", 2),
                 probability_data.get("level", {}).get("normal", 98)],
        k=1
    )[0]

    if level_choice == "special":
        special_probs = probability_data.get("special", {})
        if not special_probs:
            log_message("⚠️ special 區域無資料，請檢查 fortune_probability.yaml", level="WARNING")
            return "特殊運勢", ["今天是特別的一天！"]

        special_types = list(special_probs.keys())
        special_weights = list(special_probs.values())

        fortune_type = random.choices(
            population=special_types,
            weights=special_weights,
            k=1
        )[0]
    else:
        normal_probs = probability_data.get("normal", {})
        if not normal_probs:
            log_message("⚠️ normal 區域無資料，請檢查 fortune_probability.yaml", level="WARNING")
            return "普通運勢", ["今天是平凡的一天！"]

        normal_types = list(normal_probs.keys())
        normal_weights = list(normal_probs.values())

        fortune_type = random.choices(
            population=normal_types,
            weights=normal_weights,
            k=1
        )[0]

    # 📦 找到對應訊息清單
    messages = fortune_data.get(fortune_type, [f"今天是特別的一天！"])

    return fortune_type, messages

# 📂 ======================= Discord Embed 生成功能 =======================

async def generate_lucky_embed(interaction: discord.Interaction):
    """
    🔮 生成 Discord 嵌入式運勢訊息
    :param interaction: Discord 互動對象
    """
    try:
        # 🆔 使用者識別與日期種子，保證每天結果固定
        user_id = interaction.user.id
        taiwan_tz = pytz.timezone('Asia/Taipei')
        today_seed = datetime.now(taiwan_tz).date().toordinal() + user_id
        random.seed(today_seed)

        # ⏱️ 先回覆初始倒數，避免超時
        thinking_msg = await interaction.followup.send(get_random_countdown_message(count=3))

        # ⏳ 倒數動畫
        for i in range(3, 0, -1):
            countdown_text = get_random_countdown_message(count=i)
            await thinking_msg.edit(content=countdown_text)
            await asyncio.sleep(1)

        # 🎯 取得運勢結果
        fortune_type, fortune_messages = pick_fortune()
        fortune_text = random.choice(fortune_messages)

        # 🎨 取得其他元素
        lucky_color = get_random_color()
        suggestion = get_random_suggestion()
        anime_quote = get_random_anime_quote()
        lucky_number = random.randint(0, 9)

        # 🖼️ 組裝 Discord Embed 訊息
        embed = discord.Embed(
            title=f"🔮 今日運勢：【{fortune_type}】",
            description=fortune_text,
            color=discord.Color.random()
        )
        embed.add_field(name="🎨 幸運顏色", value=lucky_color, inline=True)
        embed.add_field(name="🔢 幸運數字", value=str(lucky_number), inline=True)
        embed.add_field(name="💡 小建議", value=suggestion, inline=False)
        embed.add_field(name="🎴 動漫金句", value=anime_quote, inline=False)
        embed.set_footer(text=f"今天的運勢類型：{fortune_type}")

        # 📤 發送結果
        await thinking_msg.edit(content=None, embed=embed)

        # 📝 Log：運勢結果
        log_message(f"🎯 {interaction.user} 完成 /運勢｜運勢：{fortune_type}｜顏色：{lucky_color}｜建議：{suggestion}", level="INFO", print_to_console=False)

    except Exception as e:
        # ❌ 回覆錯誤訊息
        await interaction.followup.send(f"❌ 發生錯誤：{str(e)}", ephemeral=True)
        exception_logger(e, context="生成運勢結果出錯")

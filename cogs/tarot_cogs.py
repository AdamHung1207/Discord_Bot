import json                        # 📦 用於處理塔羅牌與倒數語句的 JSON 檔案
import random                      # 🎲 用於隨機抽牌與倒數語句
import discord                     # 🤖 Discord API 套件
import asyncio                     # ⏱️ 非同步倒數使用
from discord.ext import commands   # 🧠 擴充 Discord Cog 功能
from discord import app_commands   # ⌨️ 用於建立斜線指令

# 📂 讀取塔羅牌 JSON 檔案
def load_tarot_cards(file_path, deck_name):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            tarot_cards = json.load(file)
        return tarot_cards  # ✅ 成功載入塔羅資料
    except Exception as e:
        return []  # ❌ 載入失敗則回傳空清單

# ⏳ 讀取倒數語句 JSON 檔案
def load_countdown_messages(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            countdown_data = json.load(file)
        return countdown_data["countdown_messages"]  # ✅ 取得倒數語句列表
    except Exception as e:
        return []  # ❌ 若格式錯誤或檔案讀取錯誤則回傳空

# 🔮 定義塔羅牌占卜模組（Cog）
class TarotCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.big_tarot = load_tarot_cards("data/tarot_big.json", "大阿爾克那")        # 📘 大牌資料
        self.small_tarot = load_tarot_cards("data/tarot_small.json", "小阿爾克那")    # 📙 小牌資料
        self.all_tarot_cards = self.big_tarot + self.small_tarot                      # 🃏 組合為 78 張牌
        self.countdown_messages = load_countdown_messages("data/tarot_countdown.json")  # ⏳ 載入倒數語句

    # 🎴 斜線指令：從 78 張塔羅牌中抽一張
    @app_commands.command(name="塔羅牌_抽單張", description="🎴 從 78 張塔羅牌中隨機抽取一張！")
    async def tarot_single(self, interaction: discord.Interaction):
        # ⚠️ 若資料未正確載入，回報錯誤
        if not self.all_tarot_cards:
            await interaction.response.send_message("❌ 無法讀取塔羅牌資料，請聯絡管理員！")
            return

        # 🔢 初始倒數提示（3 秒）
        initial_msg = random.choice(self.countdown_messages).format(count=3)
        await interaction.response.send_message(initial_msg)  # 發送初始訊息
        countdown_msg = await interaction.original_response()  # 取得訊息物件供後續編輯

        # 🔄 每秒抽一句新的倒數提示更新
        for i in [2, 1]:
            await asyncio.sleep(1)
            new_msg = random.choice(self.countdown_messages).format(count=i)
            await countdown_msg.edit(content=new_msg)

        await asyncio.sleep(1)

        # 🃏 抽一張塔羅牌並判斷正逆位
        card = random.choice(self.all_tarot_cards)
        is_reversed = random.choice([True, False])  # 🎯 是否為逆位
        position = "逆位" if is_reversed else "正位"
        adjectives = card["reversed_adjective"] if is_reversed else card["upright_adjective"]
        meaning = card["reversed"] if is_reversed else card["upright"]

        # 🖼️ 建立塔羅牌嵌入式訊息
        embed = discord.Embed(title="🔮 你的塔羅牌結果：", color=discord.Color.purple())
        embed.add_field(name="📖 牌名：", value=f"{card['tarot_zh_name']} ({card['tarot_en_name']})", inline=False)
        embed.add_field(name="🔄 正逆位：", value=position, inline=False)
        embed.add_field(name="📝 對應的形容詞：", value=adjectives, inline=False)
        embed.add_field(name="📌 牌義：", value=meaning, inline=False)
        embed.add_field(name="📖 完整解析：", value=card["meaning"], inline=False)
        embed.set_image(url=card["image"])  # 📷 插入牌面圖片

        # 🌟 編輯原本倒數訊息，加入塔羅結果
        await countdown_msg.edit(content="✨ 你的塔羅牌結果如下：", embed=embed)

# 🔧 註冊塔羅牌模組（Cog）
async def setup(bot):
    await bot.add_cog(TarotCog(bot))

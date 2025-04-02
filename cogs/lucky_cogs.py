import discord                    # 引入 Discord API 套件
from discord import app_commands  # 用於建立斜線指令（Application Commands）
from discord.ext import commands  # 擴展命令模組，用於 Bot 功能模組化
import random                     # 隨機數模組，用於隨機選擇
from datetime import datetime     # 用於處理日期時間
import asyncio                    # 異步模組，用於協程執行
import pytz                       # 用於處理時區
import json                       # JSON 處理模組，用於讀取外部資料檔案

# 工具函數，用於讀取 JSON 檔案
def load_json(file_path):
    """
    從指定路徑讀取 JSON 檔案。
    :param file_path: JSON 檔案的路徑
    :return: JSON 資料內容（字典或列表）
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"❌ 無法讀取 {file_path}：{e}")
        return {}

class LuckyCogs(commands.Cog):
    def __init__(self, bot):
        """
        初始化 LuckyCogs 類別，載入所有必要的 JSON 資料。
        :param bot: Discord Bot 實例
        """
        self.bot = bot
        # 載入 JSON 資料
        self.fortunes = load_json("data/lucky_fortunes.json")["fortunes"]
        self.lucky_colors = load_json("data/lucky_color.json")["colors"]
        self.suggestions = load_json("data/lucky_suggestions.json")["suggestions"]
        self.anime_quotes = load_json("data/lucky_Anime.json")["anime_quotes"]
        self.countdown_messages = load_json("data/lucky_countdown.json")["countdown_messages"]

    # 斜線指令 /運勢
    @app_commands.command(name="運勢", description="🔮 查看你今天的專屬運勢！")
    async def fortune(self, interaction: discord.Interaction):
        """
        生成使用者的今日運勢。
        :param interaction: Discord 互動對象
        """
        user_id = interaction.user.id
        taiwan_tz = pytz.timezone('Asia/Taipei')  # 設定時區為台北
        today = datetime.now(taiwan_tz).date().toordinal()

        # 回應延遲處理
        await interaction.response.defer()

        # 提供占卜中提示並進行倒數效果
        thinking_msg = await interaction.followup.send(random.choice(self.countdown_messages).format(count=3))
        for i in range(3, 0, -1):
            countdown_text = random.choice(self.countdown_messages).format(count=i)
            await thinking_msg.edit(content=countdown_text)
            await asyncio.sleep(1)

        # 確保同一人當天運勢不變
        random.seed(today + user_id)

        # 定義運勢類型
        fortune_types = [
            "大吉", "中吉", "小吉", "吉", "半吉", "末吉", "末小吉",
            "凶", "小凶", "半凶", "末凶", "大凶"
        ]
        special_fortunes = ["超吉", "吉娃娃"]  # 彩蛋運勢
        fortune_type = (
            random.choice(special_fortunes) if random.random() < 0.02 else random.choice(fortune_types)
        )

        # 生成運勢相關內容
        fortune_text = random.choice(self.fortunes[fortune_type])
        lucky_color = random.choice(self.lucky_colors)
        lucky_number = random.randint(0, 9)
        suggestion = random.choice(self.suggestions)
        anime_quote = random.choice(self.anime_quotes)

        # 製作 Embed 回應
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

        # 編輯最終結果
        await thinking_msg.edit(content=None, embed=embed)

# Cog 載入
async def setup(bot):
    """
    將 LuckyCogs 模組加載至 Bot。
    :param bot: Discord Bot 實例
    """
    await bot.add_cog(LuckyCogs(bot))

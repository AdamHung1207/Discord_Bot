# 📂 ======================= 基本套件導入 =======================

import discord                                  # 🤖 Discord API
from discord.ext import commands               # 🧩 指令管理
from discord import app_commands                # 🧩 Discord 斜線指令
from services.tarot import service              # 🎴 塔羅牌邏輯

# 📂 ======================= 指令註冊 =======================

class TarotCog(commands.Cog):
    """
    🃏 塔羅牌功能模組
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="塔羅牌_抽單張", description="🃏 隨機抽取一張塔羅牌，解析今日運勢")
    async def draw_tarot(self, interaction: discord.Interaction):
        """
        🎴 指令：抽取一張塔羅牌
        :param interaction: Discord 互動物件
        """
        await service.draw_tarot_card(interaction)

# 📂 ======================= Cog 載入函式 =======================

async def setup(bot: commands.Bot):
    await bot.add_cog(TarotCog(bot))

# 📂 ======================= 基本套件導入 =======================

import discord                         # 🤖 Discord API 套件
from discord import app_commands       # 🧩 Discord 應用程式指令
from discord.ext import commands       # 🧩 Discord 指令擴展
from services.lucky import service     # 🧩 引入運勢邏輯服務

# 🧩 ======================= 指令 Cog 類 =======================

class LuckyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # 🤖 Bot 實例化

    @app_commands.command(name="運勢", description="🔮 抽取今日運勢！")
    async def lucky(self, interaction: discord.Interaction):
        """
        🔮 使用者觸發 /運勢 指令，抽取專屬運勢！
        """
        try:
            # ⏳ 先延遲回應，避免 Discord 超時報錯
            await interaction.response.defer()

            # 📤 呼叫邏輯服務生成運勢 Embed
            await service.generate_lucky_embed(interaction)

        except Exception as e:
            # ❌ 錯誤處理：發送錯誤訊息給使用者
            await interaction.followup.send(
                f"❌ 執行運勢指令時發生錯誤：{str(e)}", ephemeral=True
            )

# 🧩 ======================= 註冊 Cog =======================

async def setup(bot: commands.Bot):
    """
    ✅ 指令註冊進 Bot
    """
    await bot.add_cog(LuckyCog(bot))

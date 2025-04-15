# 📂 ======================= 基本套件導入 =======================

import discord                          # 🤖 Discord API 套件
from discord import app_commands        # 🧩 Discord 應用指令
from discord.ext import commands        # 🧩 Discord 指令擴展

from services.zhezhe import service as zhezhe_service  # 🖼️ 哲哲圖片服務模組

# 📂 ======================= Discord Cog 模組 =======================

class ZhezheCog(commands.Cog):
    """
    🖼️ 哲哲圖片指令模組
    """

    def __init__(self, bot):
        self.bot = bot

    # 🔍 自動補全功能
    async def autocomplete_keyword(self, interaction: discord.Interaction, current: str):
        """
        🔍 自動補全：根據輸入的文字提供建議選項
        :param interaction: Discord 互動物件
        :param current: 當前輸入的文字
        """
        choices = zhezhe_service.service_instance.get_autocomplete_choices(current)
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices
        ]

    # 🎮 指令：/哲哲
    @app_commands.command(name="哲哲", description="🖼️ 查看哲哲經典語錄圖片")
    @app_commands.describe(keyword="📖 輸入關鍵字自動補全選擇")
    @app_commands.autocomplete(keyword=autocomplete_keyword)
    async def zhezhe(self, interaction: discord.Interaction, keyword: str):
        """
        🖼️ 傳送對應的哲哲圖片
        """
        image_url = zhezhe_service.service_instance.get_image_url(keyword)

        if image_url:
            await interaction.response.send_message(image_url)
        else:
            await interaction.response.send_message("❌ 找不到對應的圖片關鍵字，請重新輸入！")

    # 🎮 指令：/哲哲_新增
    @app_commands.command(name="哲哲_新增", description="➕ 新增哲哲圖片關鍵字")
    @app_commands.describe(keyword="🖊️ 新的關鍵字", url="🔗 圖片網址")
    async def zhezhe_add(self, interaction: discord.Interaction, keyword: str, url: str):
        """
        ➕ 新增哲哲圖片關鍵字與對應 URL
        """
        zhezhe_service.service_instance.add_image(keyword, url)
        await interaction.response.send_message(f"✅ 已成功新增圖片：**{keyword}** 👉 {url}")

# 📂 ======================= Cog 載入函數 =======================

async def setup(bot):
    """
    🧩 載入 Cog 函數
    :param bot: Discord Bot 實例
    """
    await bot.add_cog(ZhezheCog(bot))

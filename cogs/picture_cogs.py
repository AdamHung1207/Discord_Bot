import discord
from discord import app_commands
from discord.ext import commands

class Picture(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 斜線指令 /查圖
    @app_commands.command(name="查圖", description="🖼️ 查看目前可用的哲哲圖片關鍵字")
    async def list_images(self, interaction: discord.Interaction):
        """ 📸 列出哲哲圖片庫所有可用關鍵字 """
        # 嘗試取得 Zhezhe COG
        zhezhe_cog = self.bot.get_cog("Zhezhe")
        if not zhezhe_cog or not hasattr(zhezhe_cog, 'image_dict'):
            await interaction.response.send_message(
                "❌ 找不到哲哲圖片資料庫或資料庫尚未加載。",
                ephemeral=True
            )
            return

        if not zhezhe_cog.image_dict:
            await interaction.response.send_message(
                "⚠️ 哲哲圖片資料庫目前是空的，請先新增圖片！",
                ephemeral=True
            )
            return

        # 生成關鍵字列表
        keyword_list = "\n".join([f"- `{key}`" for key in zhezhe_cog.image_dict.keys()])

        # 製作 Embed 美化輸出
        embed = discord.Embed(
            title="📸 哲哲圖片關鍵字清單",
            description=keyword_list,
            color=discord.Color.blue()
        )
        embed.set_footer(text="使用 /哲哲 <關鍵字> 來呼叫對應圖片")

        await interaction.response.send_message(embed=embed)

# 必須的 setup，讓主程式可以加載這個 COG
async def setup(bot):
    await bot.add_cog(Picture(bot))
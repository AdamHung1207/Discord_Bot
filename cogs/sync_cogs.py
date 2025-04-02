import discord
from discord.ext import commands      # 用於建立 Cog 功能模組

class SyncCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot                # 傳入主程式的 Bot 實例
        self.owner_id = bot.owner_id  # 取得主程式中設定的擁有者 ID

    # 當 Bot 啟動時自動同步所有斜線指令
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()          # 同步斜線指令
        print("✅ 斜線指令已自動同步完成！")  # 在終端顯示同步完成訊息

    # 手動同步指令（僅限擁有者或管理員使用）
    @discord.app_commands.command(name="同步", description="👑 手動同步斜線指令（擁有者和管理員可使用）")
    async def sync(self, interaction: discord.Interaction):
        # 判斷使用者是否是擁有者或具有管理員權限
        if interaction.user.id == self.owner_id or interaction.user.guild_permissions.administrator:
            await self.bot.tree.sync()  # 執行指令同步
            await interaction.response.send_message("✅ 指令已同步成功！", ephemeral=True)       # 回覆同步成功
        else:
            await interaction.response.send_message("🚫 你沒有權限執行此指令！", ephemeral=True)  # 回覆權限不足

# 非同步函數：添加 SyncCog 至 Bot
async def setup(bot):
    await bot.add_cog(SyncCog(bot))  # 將 SyncCog 加入 Bot 的 Cog 系統

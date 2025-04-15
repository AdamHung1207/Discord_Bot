# 📂 ======================= 基本套件導入 =======================

import discord                         # 🤖 Discord API
from discord.ext import commands       # 🧩 Cog 擴充模組
import random                          # 🎲 隨機選取語錄

# 🧩 功能模組導入
from services.sync.repository import load_success_messages, load_error_messages  # 📚 語錄來源

# 📝 日誌工具導入（升級版）
from utils.log_utils import (
    log_command_usage,        # 📌 指令觸發紀錄
    exception_logger,         # 🪤 錯誤追蹤紀錄
    log                       # ✅ 快捷 log 工具
)

# 🧩 ======================= 斜線指令同步模組 =======================

class SyncCogs(commands.Cog):
    """
    🔄 斜線指令同步功能模組
    """

    def __init__(self, bot):
        """
        🚀 初始化 SyncCogs 類別
        :param bot: Discord Bot 實例
        """
        self.bot = bot
        self.synced_flag = False  # ✅ 避免多次同步

    @commands.Cog.listener()
    async def on_ready(self):
        """
        🚀 Bot 啟動時自動同步所有斜線指令
        """
        if self.synced_flag:
            return  # ✅ 已同步過就略過

        try:
            synced = await self.bot.tree.sync()
            log.success(f"✅ 指令已自動同步：共 {len(synced)} 個指令。")
            self.synced_flag = True

        except Exception as e:
            exception_logger(e, context="自動同步指令")
    
    @discord.app_commands.command(name="同步", description="🔄 手動同步斜線指令（管理員限定）")
    async def manual_sync(self, interaction: discord.Interaction):
        """
        🔄 手動同步指令（僅限管理員使用）
        :param interaction: Discord 互動對象
        """
        # 📵 防止私訊使用
        if not interaction.guild:
            await interaction.response.send_message("⚠️ 無法在私訊中使用本指令！", ephemeral=True)
            return

        # 🔒 權限檢查：只允許伺服器管理員使用
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("🚫 你沒有權限執行此指令！", ephemeral=True)
            return

        try:
            # 📌 紀錄指令觸發
            log_command_usage(interaction, "同步")

            # 🔄 執行同步
            synced = await self.bot.tree.sync(guild=interaction.guild)

            # 🎲 成功語錄
            success_messages = load_success_messages()
            random_message = random.choice(success_messages)

            # ✅ 成功回覆
            embed = discord.Embed(
                title="✅ 指令同步成功！",
                description=f"已同步 **{len(synced)}** 個指令至伺服器：{interaction.guild.name}\n\n{random_message}",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

            # 📝 成功 log
            log.success(f"✅ {interaction.user} 手動同步成功：{interaction.guild.name} ({len(synced)} 個指令)｜{random_message}")

        except Exception as e:
            # 🎲 失敗語錄
            error_messages = load_error_messages()
            random_error_message = random.choice(error_messages)

            # ❌ 回覆錯誤
            embed = discord.Embed(
                title="❌ 指令同步失敗！",
                description=f"發生錯誤：{e}\n\n{random_error_message}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

            # 🪤 錯誤 log
            exception_logger(e, context="手動同步指令")
            log.warning(f"❗ {interaction.user} 手動同步失敗｜{random_error_message}")

# 🧩 註冊此 Cog 模組
async def setup(bot):
    await bot.add_cog(SyncCogs(bot))

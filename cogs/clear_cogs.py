# 📂 ======================= 基本套件導入 =======================

import discord                    # 🤖 Discord API
from discord import app_commands  # ⌨️ 用於建立斜線指令
from discord.ext import commands  # 🧠 擴展命令模組

from services.clear.controller import handle_clear_command  # 🧩 清除訊息控制層
from utils.log_utils import (
    log_command_usage,            # 📌 統一格式記錄指令觸發
    exception_logger,             # 🪤 錯誤記錄工具
    log                           # ✅ 快捷 log 工具（.info/.success/.error）
)

# 🧩 ======================= 定義清除訊息的 Cog 類別 =======================

class ClearCogs(commands.Cog):
    """
    🧹 清除訊息功能模組
    """

    def __init__(self, bot):
        """
        🚀 初始化 ClearCogs 類別
        :param bot: Discord Bot 實例
        """
        self.bot = bot

        # ✅ 初始化時註冊指令到 CommandTree
        @app_commands.command(
            name="清除",
            description="🧹 清除指定數量的訊息（可選擇指定用戶）"
        )
        @app_commands.describe(
            amount="要刪除的訊息數量（最多 100）",
            user="指定要刪除訊息的用戶（可選）"
        )
        @app_commands.checks.has_permissions(manage_messages=True)  # 🔐 僅限擁有管理訊息權限的用戶
        async def clear_messages(interaction: discord.Interaction, amount: int, user: discord.Member = None):
            """
            🧩 清除訊息指令入口
            :param interaction: Discord 互動對象
            :param amount: 要刪除的訊息數量
            :param user: 指定要刪除訊息的用戶（可選）
            """
            try:
                # 📌 log：統一記錄指令觸發（使用者 + 數量 + 目標用戶）
                log_command_usage(interaction, "清除", {
                    "amount": amount,
                    "target_user": user.display_name if user else "未指定"
                })

                # 🧩 呼叫控制層執行邏輯
                await handle_clear_command(interaction, amount, user)

                # ✅ log：清除成功後紀錄（頻道名稱、數量）
                channel_name = interaction.channel.name if hasattr(interaction.channel, "name") else "Private"
                log.success(f"🧹 成功清除訊息｜使用者: {interaction.user}｜數量: {amount}｜頻道: #{channel_name}")

            except Exception as e:
                # ❌ log：如有錯誤，詳細記錄
                exception_logger(e, context="清除指令 /clear")
                await interaction.response.send_message("❌ 發生錯誤，請稍後再試或聯絡管理員。", ephemeral=True)

        # ✅ 將指令加入 Bot 的 CommandTree
        self.bot.tree.add_command(clear_messages)

# 🔧 註冊此 Cog 模組
async def setup(bot):
    """
    🧩 將 ClearCogs 模組加載至 Bot
    :param bot: Discord Bot 實例
    """
    await bot.add_cog(ClearCogs(bot))

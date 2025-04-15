# 📂 ======================= 基本套件導入 =======================

import random                                          # 🎲 開機標語用
from discord.ext import commands                       # 🤖 Discord 指令框架（for 錯誤分類）
from config import VERSION, ENV_MODE                   # ⚙️ 全局設定
from utils.log_utils import log_message                # 📝 日誌工具
from utils.startup_utils import print_startup_message  # 🚀 啟動畫面輸出

# 🌟 開機標語列表（可自行擴充）
STARTUP_QUOTES = [
    "🌈 今天也是充滿希望的一天！",
    "🚀 引擎啟動，準備起飛！",
    "✨ 系統準備就緒，冒險開始！",
    "🧩 模組檢查完成，正在載入功能！",
    "🎉 歡迎回來，準備迎接新挑戰！"
]

# 🧩 ======================= 設定事件處理器 =======================

def setup_event_handlers(bot, json_status: list, cog_status: list):
    """
    ⚙️ 初始化 Discord Bot 事件處理器
    :param bot: Discord Bot 實例
    :param json_status: JSON / config 載入狀態列表
    :param cog_status: Cogs 模組載入狀態列表
    """

    @bot.event
    async def on_ready():
        """
        🚀 Bot 啟動完成事件
        """
        startup_quote = random.choice(STARTUP_QUOTES)

        # 📝 啟動完成 log
        log_message(f"✅ Bot 已成功啟動，使用者：{bot.user}", level="SUCCESS", print_to_console=False)

        # 🚀 輸出開機畫面
        print_startup_message(
            json_status,
            cog_status,
            username=str(bot.user),
            version=VERSION,
            env_mode=ENV_MODE,
            startup_quote=startup_quote
        )

    @bot.event
    async def on_command_error(ctx, error):
        """
        ❌ 指令錯誤事件處理（進階分類版）
        """
        # 📝 預設錯誤訊息
        user_message = "⚠️ 執行指令時發生錯誤！"

        # 🎯 分類處理不同錯誤類型
        if isinstance(error, commands.CommandNotFound):
            user_message = "❌ 指令不存在，請確認輸入正確。"
        elif isinstance(error, commands.MissingRequiredArgument):
            user_message = "⚠️ 指令參數不足，請補齊後再試！"
        elif isinstance(error, commands.CommandInvokeError):
            user_message = "⚠️ 執行指令過程發生錯誤！"

        # 📨 回應使用者錯誤訊息
        await ctx.send(user_message)

        # 📝 錯誤記錄至 log 檔案
        log_message(f"❌ 指令錯誤：{error}", level="ERROR", print_to_console=False)

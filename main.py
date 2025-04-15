# 📂 ======================= 基本套件導入 =======================

import os                         # 🗂️ 系統檔案操作
import sys                        # 🖥️ 系統控制（程式退出等）

# ✅ 自動加入專案根目錄到系統路徑，確保所有模組正常 import
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# 📝 這樣就能正常 import services / utils / cogs 等自訂模組
# ✅ 無論 VSCode / 終端 / 生產環境 / Docker / .exe 打包 都能正常運行

# 📂 ======================= 其他基礎套件與初始化 =======================

import asyncio                    # ⏱️ 異步協程支援
import random                     # 🎲 開機標語使用
import discord                    # 🤖 Discord API
from discord.ext import commands  # 🤖 Discord 指令框架
from dotenv import load_dotenv    # 🛠️ 讀取 .env 環境變數

# 📂 自訂模組導入（utils 模組化設計）
from utils.log_utils import log_message                    # 📝 日誌工具
from utils.startup_utils import print_startup_message      # 🚀 啟動訊息輸出
from utils.file_utils import clean_old_logs                # 🧹 自動清理 log 檔案
from utils.error_utils import setup_global_error_handler   # 🚨 全域錯誤處理
from utils.cog_utils import load_all_cogs, hot_reload_cogs # 📂 Cogs 模組管理
from utils.event_handler import setup_event_handlers       # ⚙️ Discord 事件管理
# 預留：未來可加自動掃描 service/controller.py

# 📂 配置檔（優化後的 config.py）
import config

# 📝 ======================= 環境初始化 =======================

# ✅ 載入 .env 環境變數
load_dotenv()

# ✅ log 設定（不輸出到終端機，只寫入檔案）
LOG_TO_CONSOLE = False

# ✅ 初始化全域錯誤處理器（log 捕捉全局異常）
setup_global_error_handler()

# 🧹 啟動時自動清理過期 log 檔案
clean_old_logs(retention_days=config.LOG_RETAIN_DAYS)

# 🧩 ======================= Discord Bot 基本設定 =======================

# 🔍 設定 Discord Bot 權限 Intents（全開）
intents = discord.Intents.all()

# 🤖 初始化指令 bot
bot = commands.Bot(command_prefix=config.COMMAND_PREFIX, intents=intents)

# 📦 狀態記錄：啟動狀態 / 模組載入情況
json_status = ["✅ 環境變數與設定載入成功"]
cog_status = []

# 🌟 開機隨機標語列表
STARTUP_QUOTES = [
    "🌈 今天也是充滿希望的一天！",
    "🚀 引擎啟動，準備起飛！",
    "✨ 系統準備就緒，冒險開始！",
    "🧩 模組檢查完成，正在載入功能！",
    "🎉 歡迎回來，準備迎接新挑戰！"
]

# 🧩 ======================= 啟動流程（Async） =======================

async def startup():
    """
    🚀 Bot 啟動初始化流程
    """
    # ✅ 設定 Discord 事件處理器（如 on_ready）
    setup_event_handlers(bot, json_status, cog_status)

    # ✅ 載入所有 Cogs 模組（指令集）
    await load_all_cogs(bot, cog_status, log_to_console=LOG_TO_CONSOLE)

    # 🔄 啟用模組熱重載（開發期間自動重新載入）
    asyncio.create_task(hot_reload_cogs(bot, cog_status, log_to_console=LOG_TO_CONSOLE))

    # （預留）✅ 未來可加自動掃描 services/controller.py 並注入

# 🧩 ======================= 主程式入口 =======================

def main():
    try:
        # ✅ 執行 Bot 啟動流程
        asyncio.run(startup())

        # ✅ 啟動 Discord Bot
        bot.run(config.DISCORD_TOKEN)

    except KeyboardInterrupt:
        # 🛑 使用者手動中斷（Ctrl + C）
        log_message("🛑 停止啟動程序 (使用者中斷)", level="WARNING", print_to_console=LOG_TO_CONSOLE)
        sys.exit()

    except Exception as e:
        # 🚨 啟動流程發生異常
        log_message(f"🚨 啟動失敗：{e}", level="ERROR", print_to_console=LOG_TO_CONSOLE)
        sys.exit()

# 🚀 程式啟動點
if __name__ == "__main__":
    main()

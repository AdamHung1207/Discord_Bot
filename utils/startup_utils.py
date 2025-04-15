# 📂 ======================= 基本套件導入 =======================

import os                  # 🗂️ 系統檔案操作
import time                # ⏱️ 計算啟動耗時
from config import ENV_MODE, VERSION, LOG_DIR, SERVICES_DIR, COGS_DIR  # ⚙️ 全局設定
from utils.log_utils import log_message  # 📝 日誌工具

# 🌟 隨機開機標語
STARTUP_QUOTES = [
    "🌈 今天也是充滿希望的一天！",
    "🚀 引擎啟動，準備起飛！",
    "✨ 系統準備就緒，冒險開始！",
    "🧩 模組檢查完成，正在載入功能！",
    "🎉 歡迎回來，準備迎接新挑戰！"
]

# 🧩 ======================= 啟動畫面輸出工具 =======================

def print_startup_message(
    json_status: list,
    cog_status: list,
    username: str = "未知使用者",
    version: str = "未定義",
    env_mode: str = "PROD",
    startup_quote: str = "",
    start_time: float = None
):
    """
    🚀 輸出專業級啟動畫面
    :param json_status: JSON / config 載入狀態
    :param cog_status: Cogs 模組載入狀態
    :param username: Bot 使用者名稱
    :param version: Bot 版本號
    :param env_mode: 環境模式（DEV / PROD）
    :param startup_quote: 隨機開機標語
    :param start_time: 啟動計時器開始時間
    """

    # 🕒 計算啟動耗時（秒）
    if start_time:
        elapsed_time = round(time.time() - start_time, 2)
    else:
        elapsed_time = None

    # 📊 統計 Cogs / Services 模組數量
    cogs_count = count_py_files(COGS_DIR)
    services_count = count_services(SERVICES_DIR)

    # ✅ 必要資料夾檢查
    log_folder_status = check_directory(LOG_DIR)
    services_folder_status = check_directory(SERVICES_DIR)

    # 🧩 開始輸出畫面
    print()
    print("╔══════════════════════════════════════════╗")
    print("║        🤖 Discord Bot 啟動成功！         ║")
    print("╚══════════════════════════════════════════╝\n")

    # 📝 系統資訊
    print(f"🧩 模組統計：Cogs {cogs_count} 個｜Services {services_count} 個")
    print(f"🗂️ 資料夾檢查：logs/ {log_folder_status}｜services/ {services_folder_status}")
    print(f"🌍 環境模式：{env_mode}")
    print(f"🏷️ 版本號：{version}")

    if elapsed_time is not None:
        print(f"🕒 啟動耗時：{elapsed_time} 秒")

    print(f"🎉 開機標語：{startup_quote}\n")

    # ✅ 使用者 / 啟動時間
    print(f"👤 使用者：{username}")
    print(f"🕒 啟動時間：{time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 📦 JSON / Config 載入狀態
    print("📦 JSON / 環境變數載入狀態：")
    for status in json_status:
        print(f"{status}")

    # 🔧 Cogs 載入狀態
    print("\n🔧 Cogs 載入狀態：")
    for status in cog_status:
        print(f"{status}")

    print("\n✅ Bot 模組：已準備就緒！正在等待指令輸入中...\n")

# 🧩 ======================= 工具函數 =======================

def count_py_files(directory: str) -> int:
    """
    📊 統計指定資料夾中的 Python 檔案數量
    """
    if not os.path.exists(directory):
        return 0
    return len([f for f in os.listdir(directory) if f.endswith(".py") and not f.startswith("_")])

def count_services(directory: str) -> int:
    """
    📊 統計 Services 模組數量（以資料夾計算）
    """
    if not os.path.exists(directory):
        return 0
    return len([
        f for f in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, f)) and not f.startswith("_")
    ])

def check_directory(path: str) -> str:
    """
    🗂️ 檢查資料夾是否存在，回傳狀態字串
    """
    return "✅" if os.path.exists(path) else "❌"

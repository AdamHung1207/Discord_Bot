# 📂 ======================= 基本套件導入 =======================

import os                                              # 🗂️ 檔案 / 資料夾操作
import traceback                                       # 🪤 錯誤追蹤堆疊
from datetime import datetime                          # 📅 取得日期時間
from colorama import init, Fore                        # 🎨 顏色工具（可選：目前不輸出終端機）
from config import LOG_DIR, LOG_TO_CONSOLE, LOG_LEVEL  # ⚙️ 導入全局設定值
from utils.file_utils import ensure_directory          # 🧩 檔案工具：確認資料夾存在

# ✅ 初始化 colorama（目前未輸出終端，但保留擴充彈性）
init(autoreset=True)

# 📋 日誌層級對應（保留擴充用）
LOG_LEVELS = ["DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR"]

# 🎨 各等級對應顏色（若啟用終端輸出用）
LEVEL_COLORS = {
    "DEBUG": Fore.LIGHTBLUE_EX,
    "INFO": Fore.CYAN,
    "SUCCESS": Fore.GREEN,
    "WARNING": Fore.YELLOW,
    "ERROR": Fore.RED,
}

# 🧩 ======================= 日誌主寫入工具 =======================

def log_message(message: str, level: str = "INFO", print_to_console: bool = LOG_TO_CONSOLE):
    """
    📝 寫入日誌主工具函式
    :param message: 要寫入的訊息內容
    :param level: 日誌等級（預設為 INFO）
    :param print_to_console: 是否輸出到終端（預設為 config 設定）
    """
    ensure_directory(LOG_DIR)  # ✅ 確保 logs 資料夾存在

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 🕒 時間戳
    color = LEVEL_COLORS.get(level.upper(), Fore.WHITE)       # 🎨 對應顏色
    full_message = f"[{timestamp}] [{level.upper()}] {message}"  # 📋 完整格式化訊息

    # 📤 終端輸出（目前關閉）
    if print_to_console:
        print(color + full_message)

    # 🗂️ 檔案名稱：logs/2025-04-15.log
    log_filename = datetime.now().strftime("%Y-%m-%d") + ".log"
    log_filepath = os.path.join(LOG_DIR, log_filename)

    # ✍️ 寫入檔案
    with open(log_filepath, "a", encoding="utf-8") as f:
        f.write(full_message + "\n")

# 🧩 ======================= 快捷寫入類別 =======================

class LogHelper:
    """
    🧩 快捷 log 類別，用於調用各等級日誌
    """
    @staticmethod
    def debug(message: str):
        log_message(message, level="DEBUG")

    @staticmethod
    def info(message: str):
        log_message(message, level="INFO")

    @staticmethod
    def success(message: str):
        log_message(message, level="SUCCESS")

    @staticmethod
    def warning(message: str):
        log_message(message, level="WARNING")

    @staticmethod
    def error(message: str):
        log_message(message, level="ERROR")

# ✅ 建立全域 log 實例
log = LogHelper()

# 🧩 ======================= 舊版兼容接口 =======================

def write_log(message: str):
    """
    🧩 向下相容的寫入方式（預設為 INFO）
    """
    log.info(message)

# 🪤 ======================= 錯誤記錄工具（含 traceback） =======================

def exception_logger(err: Exception, context: str = ""):
    """
    🪤 捕捉例外錯誤並寫入日誌（含 traceback）
    :param err: 例外錯誤物件
    :param context: 錯誤上下文描述（可選）
    """
    error_type = type(err).__name__
    error_message = str(err)
    tb = traceback.format_exc()
    log.error(f"{context} ❌ 發生錯誤：{error_type} - {error_message}\n{tb}")

# 🙋 ======================= 使用者資訊格式化工具 =======================

def format_user(user) -> str:
    """
    🙋 格式化 Discord 使用者資訊為可讀字串
    :param user: discord.User / Member 物件
    :return: 使用者名稱#ID (ID: 數字)
    """
    return f"{user.name}#{user.discriminator} (ID: {user.id})"

# 📌 ======================= 指令觸發紀錄工具（支援 ctx + interaction） =======================

def log_command_usage(ctx_or_interaction, command_name: str, extra_info: dict = None):
    """
    📌 統一格式記錄使用者觸發指令（支援 ctx 或 interaction）
    :param ctx_or_interaction: 指令上下文或互動物件（ctx 或 interaction）
    :param command_name: 指令名稱（不含 / 符號）
    :param extra_info: 額外資訊（dict 形式，可選）
    """
    user = getattr(ctx_or_interaction, "author", None) or getattr(ctx_or_interaction, "user", None)
    channel = getattr(ctx_or_interaction.channel, "name", "Private")
    user_info = format_user(user)

    base = f"[指令觸發] /{command_name}｜使用者: {user_info}｜頻道: #{channel}"
    if extra_info:
        details = "｜" + "｜".join(f"{k}: {v}" for k, v in extra_info.items())
        base += details
    log.info(base)

# 📦 ======================= Cogs 載入統計工具 =======================

def log_startup_summary(success: list, failed: list):
    """
    📦 啟動時統一記錄模組載入結果
    :param success: 成功的模組清單
    :param failed: 失敗的模組清單
    """
    log.info(f"🧩 Cogs 載入完成：成功 {len(success)} 個，失敗 {len(failed)} 個，總共 {len(success) + len(failed)} 個。")
    if failed:
        log.warning("❗ 失敗 Cogs 清單：" + "、".join(failed))

# 🧪 ======================= Debug 模式限定輸出 =======================

DEBUG_MODE = True  # 可由 config 控制開關

def debug_only(message: str):
    """
    🧪 僅在 DEBUG 模式下輸出 debug 日誌
    """
    if DEBUG_MODE:
        log.debug(message)

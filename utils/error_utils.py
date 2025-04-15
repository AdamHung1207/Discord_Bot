# 📂 ======================= 基本套件導入 =======================

import sys                                # 🖥️ 系統操作（異常退出）
import traceback                          # 🧩 堆疊追蹤
from config import STRICT_ERROR_HANDLING  # ⚙️ 全局嚴格模式開關
from utils.log_utils import log_message   # 📝 導入 log 工具

# 🧩 ======================= 全域錯誤處理器 =======================

def setup_global_error_handler():
    """
    🚨 初始化全域錯誤處理器
    📌 捕捉所有未處理例外，避免程式直接崩潰。
    """
    def handle_exception(exc_type, exc_value, exc_traceback):
        # 🚫 忽略 KeyboardInterrupt（手動中斷 Ctrl + C）
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        # 📝 組合錯誤訊息
        error_message = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))

        # 🚨 寫入 log（全局錯誤）
        log_message(f"🚨 全域異常捕獲：\n{error_message}", level="ERROR", print_to_console=False)

        # ⚠️ 嚴格模式：遇到錯誤直接退出
        if STRICT_ERROR_HANDLING:
            sys.exit(1)

    # ✅ 設定系統全域異常處理 hook
    sys.excepthook = handle_exception

# 🧩 ======================= 局部錯誤處理工具 =======================

def try_catch(func):
    """
    🧩 裝飾器：局部 try-except 自動處理錯誤
    📌 適用於需要自動 log，但不想中斷主程式的功能模組
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            # 📝 捕捉局部錯誤並記錄
            error_message = traceback.format_exc()
            log_message(f"⚠️ 局部異常捕獲：\n{error_message}", level="ERROR", print_to_console=False)

            # ⚠️ 嚴格模式：局部異常亦可選擇拋出
            if STRICT_ERROR_HANDLING:
                raise

    return wrapper

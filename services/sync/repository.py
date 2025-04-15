# 📂 ======================= 基本套件導入 =======================

import os                                       # 🗂️ 檔案系統操作
import yaml                                     # 📒 處理 YAML 文件
from utils.file_utils import check_file_exists  # 🧩 工具：檢查檔案存在
from utils.log_utils import log_message         # 📝 統一日誌紀錄

# 📂 資料檔案路徑
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
SUCCESS_MESSAGES_FILE = os.path.join(DATA_DIR, "success_messages.yaml")
ERROR_MESSAGES_FILE = os.path.join(DATA_DIR, "error_messages.yaml")

# 🧩 ======================= 讀取成功語錄 =======================

def load_success_messages() -> list:
    """
    📖 讀取成功語錄（從 YAML 檔案）
    :return: 成功訊息列表，失敗則回傳預設列表
    """
    return _load_messages(SUCCESS_MESSAGES_FILE, default_messages=[
        "✅ 指令同步成功！"
    ])

# 🧩 ======================= 讀取失敗語錄 =======================

def load_error_messages() -> list:
    """
    📖 讀取失敗語錄（從 YAML 檔案）
    :return: 失敗訊息列表，失敗則回傳預設列表
    """
    return _load_messages(ERROR_MESSAGES_FILE, default_messages=[
        "❌ 指令同步失敗！"
    ])

# 🧩 ======================= 通用讀取邏輯 =======================

def _load_messages(file_path: str, default_messages: list) -> list:
    """
    🧩 通用訊息讀取工具
    :param file_path: YAML 檔案路徑
    :param default_messages: 預設訊息列表（檔案缺失或異常時使用）
    :return: 訊息列表
    """
    if not check_file_exists(file_path):
        log_message(f"⚠️ 找不到 YAML：{file_path}，使用預設訊息列表。", level="WARNING", print_to_console=False)
        return default_messages

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            # 檔案格式正常但內容空，回傳預設列表
            if not data:
                log_message(f"⚠️ YAML 檔案為空：{file_path}，使用預設訊息列表。", level="WARNING", print_to_console=False)
                return default_messages

            messages = data.get("success_messages" if "success" in file_path else "error_messages", [])
            if not messages:
                log_message(f"⚠️ YAML 檔案列表為空：{file_path}，使用預設訊息列表。", level="WARNING", print_to_console=False)
                return default_messages

            return messages

    except Exception as e:
        log_message(f"❌ 讀取 YAML 發生錯誤：{e}", level="ERROR", print_to_console=False)
        return default_messages

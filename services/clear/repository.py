# 📂 ======================= 基本套件導入 =======================

import os                                       # 🗂️ 系統檔案操作
import yaml                                     # 📒 處理 YAML 檔案
from utils.file_utils import check_file_exists  # 📝 工具：檢查檔案是否存在
from utils.log_utils import log_message         # 📝 工具：log 記錄

# 📂 資料檔案路徑
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
SUCCESS_MESSAGES_FILE = os.path.join(DATA_DIR, "success_messages.yaml")

# 🧩 ======================= 資料存取功能 =======================

def load_success_messages() -> list:
    """
    📖 讀取成功訊息列表（從 YAML 檔案）
    :return: 成功訊息列表，失敗則回傳預設列表
    """
    if not check_file_exists(SUCCESS_MESSAGES_FILE):
        log_message(f"⚠️ 找不到成功訊息 YAML：{SUCCESS_MESSAGES_FILE}，將使用預設訊息列表。", level="WARNING", print_to_console=False)
        return [
            "🧹 清潔機器人上線，成功刪除 {count} 則訊息！"
        ]

    try:
        with open(SUCCESS_MESSAGES_FILE, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            messages = data.get("success_messages", [])

            if not messages:
                log_message("⚠️ YAML 成功訊息列表為空，請檢查文件內容。", level="WARNING", print_to_console=False)
                return ["🧹 清潔機器人上線，成功刪除 {count} 則訊息！"]

            return messages

    except Exception as e:
        log_message(f"❌ 讀取成功訊息 YAML 發生錯誤：{e}", level="ERROR", print_to_console=False)
        return ["🧹 清潔機器人上線，成功刪除 {count} 則訊息！"]

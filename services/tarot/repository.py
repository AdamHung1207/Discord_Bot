# 📂 ======================= 基本套件導入 =======================

import os                                       # 🗂️ 檔案系統操作
import yaml                                     # 📒 處理 YAML 文件
from utils.file_utils import check_file_exists  # 🧹 工具：檢查檔案存在
from utils.log_utils import log_message         # 📝 統一日誌紀錄

# 📂 資料檔案路徑
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
BIG_CARDS_FILE = os.path.join(DATA_DIR, "big_cards.yaml")
SMALL_CARDS_FILE = os.path.join(DATA_DIR, "small_cards.yaml")
COUNTDOWN_MESSAGES_FILE = os.path.join(DATA_DIR, "countdown_messages.yaml")

# 🧹 ======================= 讀取大牌 =======================

def load_big_cards() -> dict:
    """
    📖 讀取塔羅大牌資料
    :return: dict 格式，如：{"big_cards": [...]} 
    """
    data = _load_yaml(BIG_CARDS_FILE)
    return {"big_cards": data if isinstance(data, list) else []}

# 🧹 ======================= 讀取小牌 =======================

def load_small_cards() -> dict:
    """
    📖 讀取塔羅小牌資料
    :return: dict 格式，如：{"small_cards": [...]} 
    """
    data = _load_yaml(SMALL_CARDS_FILE)
    return {"small_cards": data if isinstance(data, list) else []}

# 🧹 ======================= 讀取倒數語錄 =======================

def load_countdown_messages() -> dict:
    """
    📖 讀取倒數動畫語錄
    :return: dict 格式，如：{"countdown_messages": [...]} 
    """
    data = _load_yaml(COUNTDOWN_MESSAGES_FILE, default_messages={"countdown_messages": ["倒數 {count} 秒！"]})
    return {"countdown_messages": data.get("countdown_messages", []) if isinstance(data, dict) else []}

# 🧹 ======================= 通用讀取邏輯 =======================

def _load_yaml(file_path: str, default_messages=None) -> dict | list:
    """
    🧹 通用 YAML 讀取工具
    :param file_path: YAML 檔案路徑
    :param default_messages: 預設訊息（檔案缺失或異常時使用）
    :return: YAML 資料
    """
    if not check_file_exists(file_path):
        log_message(f"⚠️ 找不到 YAML：{file_path}，使用預設資料。", level="WARNING", print_to_console=False)
        return default_messages or {}

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            if not data:
                log_message(f"⚠️ YAML 檔案為空：{file_path}，使用預設資料。", level="WARNING", print_to_console=False)
                return default_messages or {}

            return data

    except Exception as e:
        log_message(f"❌ 讀取 YAML 發生錯誤：{e}", level="ERROR", print_to_console=False)
        return default_messages or {}

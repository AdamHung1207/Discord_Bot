# 📂 ======================= 基本套件導入 =======================

import os                                       # 🗂️ 檔案路徑操作
import yaml                                     # 📒 讀取 YAML 文件
from utils.file_utils import check_file_exists, load_yaml  # 🧩 檔案工具
from utils.log_utils import log_message         # 📝 統一日誌管理

# 📂 ======================= 資料檔案路徑 =======================

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")          # 📂 資料夾路徑
ANSWER_FILE = os.path.join(DATA_DIR, "answer_messages.yaml")        # 📜 答案語錄
COUNTDOWN_FILE = os.path.join(DATA_DIR, "countdown_messages.yaml")  # ⏳ 倒數語錄
DIVIDERS_FILE = os.path.join(DATA_DIR, "dividers.yaml")             # 🎀 分隔線樣式

# 🧩 ======================= 通用 YAML 讀取工具 =======================

def _load_yaml(file_path: str, data_key: str, default: list) -> list:
    """
    🧩 通用 YAML 讀取工具
    :param file_path: YAML 檔案路徑
    :param data_key: YAML 主資料鍵名
    :param default: 預設回傳列表
    :return: 資料列表
    """
    if not check_file_exists(file_path):
        log_message(f"⚠️ 找不到 YAML：{file_path}，使用預設值。", level="WARNING", print_to_console=False)
        return default

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            if not data or data_key not in data:
                log_message(f"⚠️ YAML 格式異常或缺少 `{data_key}`：{file_path}，使用預設值。", level="WARNING", print_to_console=False)
                return default

            return data.get(data_key, default)

    except Exception as e:
        log_message(f"❌ 讀取 YAML 失敗：{e}｜檔案：{file_path}", level="ERROR", print_to_console=False)
        return default

# 🧩 ======================= 讀取各類 YAML 資料 =======================

def load_answer_messages() -> dict:
    """
    📖 讀取答案訊息模板
    :return: 回傳字典，包含 1%、98% 等回答模板
    """
    if not check_file_exists(ANSWER_FILE):
        log_message(f"⚠️ 找不到答案 YAML：{ANSWER_FILE}，使用預設空字典。", level="WARNING", print_to_console=False)
        return {}

    try:
        with open(ANSWER_FILE, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            return data or {}
    except Exception as e:
        log_message(f"❌ 讀取答案 YAML 失敗：{e}｜檔案：{ANSWER_FILE}", level="ERROR", print_to_console=False)
        return {}

def load_countdown_messages() -> list:
    """
    ⏳ 讀取倒數訊息模板
    :return: 倒數訊息列表
    """
    return _load_yaml(
        file_path=COUNTDOWN_FILE,
        data_key="countdown_messages",
        default=["思考中... {count}"]
    )

def load_dividers() -> list:
    """
    🎀 讀取分隔線樣式
    :return: 分隔線列表
    """
    return _load_yaml(
        file_path=DIVIDERS_FILE,
        data_key="dividers",
        default=["----------"]
    )

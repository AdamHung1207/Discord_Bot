# 📂 ======================= 基本套件導入 =======================

import os                                       # 🗂️ 檔案路徑操作
from utils.file_utils import check_file_exists, load_yaml, _load_yaml  # 🧩 工具函式
from utils.log_utils import log_message         # 📝 統一日誌管理

# 📂 ======================= 資料檔案路徑 =======================

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")             # 📂 資料夾路徑
FORTUNE_FILE = os.path.join(DATA_DIR, "fortunes.yaml")                 # 🎯 運勢語錄
COLOR_FILE = os.path.join(DATA_DIR, "colors.yaml")                     # 🎨 幸運顏色
COUNTDOWN_FILE = os.path.join(DATA_DIR, "countdown_messages.yaml")     # ⏳ 倒數語錄
SUGGESTIONS_FILE = os.path.join(DATA_DIR, "suggestions.yaml")          # 💡 小建議
ANIME_FILE = os.path.join(DATA_DIR, "anime_quotes.yaml")               # 🎴 動漫金句

# 🧩 ======================= YAML 讀取工具 =======================

def load_fortunes() -> dict:
    """
    🎯 讀取運勢詳細內容
    :return: 運勢字典
    """
    if not check_file_exists(FORTUNE_FILE):
        log_message(f"⚠️ 找不到運勢 YAML：{FORTUNE_FILE}，使用預設空字典。", level="WARNING", print_to_console=False)
        return {}

    try:
        return load_yaml(FORTUNE_FILE).get("fortunes", {})
    except Exception as e:
        log_message(f"❌ 讀取運勢 YAML 失敗：{e}｜檔案：{FORTUNE_FILE}", level="ERROR", print_to_console=False)
        return {}

def load_colors() -> list:
    """
    🎨 讀取幸運顏色
    :return: 顏色列表
    """
    return _load_yaml(
        file_path=COLOR_FILE,
        data_key="colors",
        default=["黑色"]
    )

def load_countdown_messages() -> list:
    """
    ⏳ 讀取倒數訊息模板
    :return: 倒數訊息列表
    """
    return _load_yaml(
        file_path=COUNTDOWN_FILE,
        data_key="countdown_messages",
        default=["請稍候 {count} 秒..."]
    )

def load_suggestions() -> list:
    """
    💡 讀取小建議
    :return: 建議列表
    """
    return _load_yaml(
        file_path=SUGGESTIONS_FILE,
        data_key="suggestions",
        default=["保持微笑"]
    )

def load_anime_quotes() -> list:
    """
    🎴 讀取動漫金句
    :return: 動漫語錄列表
    """
    return _load_yaml(
        file_path=ANIME_FILE,
        data_key="anime_quotes",
        default=["要堅強！"]
    )

# 📂 ======================= 基本套件導入 =======================

import os                                 # 🗂️ 處理路徑
import shutil                             # 🧹 刪除檔案或目錄
from datetime import datetime, timedelta  # 📅 處理日期時間
import yaml                               # 📒 讀取 YAML 檔案

# 🧩 ======================= 工具類：檔案 / 目錄處理 =======================

def ensure_directory(path: str):
    """
    📂 確認資料夾是否存在，若無則自動建立
    :param path: 資料夾路徑
    """
    # ✅ 延遲導入，避免循環引用
    from utils.log_utils import log_message

    if not os.path.exists(path):
        os.makedirs(path)
        log_message(f"📂 已自動建立資料夾：{path}", level="INFO")

def clean_old_logs(retention_days=3):
    """
    🧹 自動清理 logs 目錄，保留最近 N 天
    :param retention_days: 保留天數
    """
    # ✅ 延遲導入，避免循環引用
    from utils.log_utils import log_message

    log_dir = "logs"
    if not os.path.exists(log_dir):
        return

    cutoff_time = datetime.now() - timedelta(days=retention_days)

    for filename in os.listdir(log_dir):
        file_path = os.path.join(log_dir, filename)
        if os.path.isfile(file_path):
            file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_mtime < cutoff_time:
                os.remove(file_path)
                log_message(f"🧹 自動清理過期日誌：{filename}", level="INFO")

def check_file_exists(file_path: str) -> bool:
    """
    📝 檢查檔案是否存在
    :param file_path: 檔案路徑
    :return: 存在則返回 True，否則 False
    """
    # ✅ 延遲導入，避免循環引用
    from utils.log_utils import log_message

    exists = os.path.isfile(file_path)
    if exists:
        log_message(f"✅ 檔案存在：{file_path}", level="INFO")
    else:
        log_message(f"❌ 檔案不存在：{file_path}", level="WARNING")
    return exists

# 🧩 ======================= 工具類：YAML 讀取 =======================

def load_yaml(file_path: str) -> dict:
    """
    📒 讀取整份 YAML 文件
    :param file_path: YAML 檔案路徑
    :return: YAML 資料字典
    """
    # ✅ 延遲導入，避免循環引用
    from utils.log_utils import log_message

    if not check_file_exists(file_path):
        log_message(f"⚠️ 找不到 YAML：{file_path}，返回空字典。", level="WARNING", print_to_console=False)
        return {}

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}
    except Exception as e:
        log_message(f"❌ 讀取 YAML 失敗：{e}｜檔案：{file_path}", level="ERROR", print_to_console=False)
        return {}

def _load_yaml(file_path: str, data_key: str, default: list) -> list:
    """
    🧩 通用 YAML 讀取工具（專讀某一個 key）
    :param file_path: YAML 檔案路徑
    :param data_key: YAML 主資料鍵名
    :param default: 預設回傳列表
    :return: 資料列表
    """
    from utils.log_utils import log_message

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

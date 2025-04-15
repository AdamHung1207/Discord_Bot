# 📂 ======================= 基本套件導入 =======================

import os                                       # 🗂️ 處理檔案與路徑
import yaml                                     # 📒 處理 YAML 文件
from utils.file_utils import check_file_exists  # 🧩 工具：檢查檔案存在
from utils.log_utils import log_message         # 📝 統一日誌管理

# 📂 ======================= 資料檔案路徑 =======================

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
IMAGE_FILE = os.path.join(DATA_DIR, "zhezhe_image.yaml")  # ✅ 圖片列表檔案

# 📂 ======================= 通用 YAML 讀取器 =======================

def load_image_data() -> dict:
    """
    🖼️ 讀取哲哲圖片 YAML
    :return: 圖片字典
    """
    if not check_file_exists(IMAGE_FILE):
        log_message(f"⚠️ 找不到 YAML：{IMAGE_FILE}，回傳空字典。", level="WARNING", print_to_console=False)
        return {}

    try:
        with open(IMAGE_FILE, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}
            if not isinstance(data, dict):
                log_message(f"⚠️ YAML 格式錯誤：{IMAGE_FILE}，應為字典格式。", level="WARNING", print_to_console=False)
                return {}
            return data

    except Exception as e:
        log_message(f"❌ 讀取 YAML 發生錯誤：{e}", level="ERROR", print_to_console=False)
        return {}

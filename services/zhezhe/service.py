# 📂 ======================= 基本套件導入 =======================

import os                                       # 🗂️ 檔案系統操作
import yaml                                     # 📒 處理 YAML 文件
from utils.file_utils import check_file_exists  # 🧩 工具：檢查檔案是否存在
from utils.log_utils import log_message         # 📝 統一日誌管理

# 📂 ======================= 資料檔案路徑 =======================

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")   # 📁 資料夾路徑
IMAGE_FILE = os.path.join(DATA_DIR, "zhezhe_images.yaml")   # 🖼️ 圖片資料路徑

# 📂 ======================= 通用 YAML 讀取工具 =======================

def load_yaml(file_path: str, default=None):
    """
    📖 通用 YAML 讀取器
    :param file_path: YAML 檔案路徑
    :param default: 預設值
    :return: 讀取結果
    """
    if not check_file_exists(file_path):
        log_message(f"⚠️ 找不到 YAML：{file_path}，使用預設值。", level="WARNING", print_to_console=False)
        return default or {}

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file) or default
    except Exception as e:
        log_message(f"❌ 讀取 YAML 失敗：{e}｜檔案：{file_path}", level="ERROR", print_to_console=False)
        return default or {}

# 📂 ======================= 功能服務：哲哲圖片服務模組 =======================

class ZhezheService:
    """
    🖼️ 哲哲圖片服務模組
    """
    def __init__(self):
        """
        🧩 初始化，載入 YAML 資料
        """
        self.image_dict = load_yaml(IMAGE_FILE, {})

    def get_autocomplete_choices(self, current: str):
        """
        🔍 提供關鍵字自動補全（最多 10 筆）
        :param current: 當前輸入文字
        :return: 符合的關鍵字列表
        """
        return [
            key for key in self.image_dict.keys()
            if current in key
        ][:10]

    def get_image_url(self, keyword: str):
        """
        🖼️ 根據關鍵字取得圖片 URL
        :param keyword: 使用者輸入的關鍵字
        :return: 對應圖片網址，若無則回傳 None
        """
        return self.image_dict.get(keyword)

    def get_all_keywords(self):
        """
        🧩 取得所有關鍵字與總數
        :return: 關鍵字列表與總數
        """
        keywords = list(self.image_dict.keys())
        total = len(keywords)
        return keywords, total

    def add_image(self, keyword: str, url: str):
        """
        ➕ 新增圖片關鍵字與 URL
        :param keyword: 新增的關鍵字
        :param url: 對應的圖片網址
        """
        self.image_dict[keyword] = url
        self.save_image_data()

    def save_image_data(self):
        """
        💾 儲存圖片資料到 YAML 檔案
        """
        try:
            with open(IMAGE_FILE, "w", encoding="utf-8") as file:
                yaml.dump(self.image_dict, file, allow_unicode=True)
            log_message("✅ 已成功儲存哲哲圖片資料。")
        except Exception as e:
            log_message(f"❌ 儲存 YAML 失敗：{e}", level="ERROR")

# 🧩 初始化服務實例
service_instance = ZhezheService()

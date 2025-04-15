# 📂 ======================= 資料處理工具模組 =======================

import os                           # 🗂️ 檔案與路徑操作
import json                         # 🧾 JSON 處理
import yaml                         # 📦 YAML 處理
from utils.log_utils import log     # 📝 日誌工具（log.warning 等）

# 🧩 ======================= YAML 載入工具 =======================

def load_yaml(file_path: str, fallback=None):
    """
    📦 載入 YAML 檔案內容
    :param file_path: 路徑
    :param fallback: 讀取失敗時回傳的預設值
    :return: dict / list / fallback
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        log.warning(f"❗ YAML 讀取失敗：{file_path}｜錯誤：{e}")
        return fallback

# 🧩 ======================= YAML 儲存工具 =======================

def save_yaml(data, file_path: str):
    """
    📦 將資料儲存為 YAML 檔案
    :param data: dict / list
    :param file_path: 輸出路徑
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True)
        log.success(f"✅ YAML 已儲存：{file_path}")
    except Exception as e:
        log.warning(f"❗ YAML 儲存失敗：{file_path}｜錯誤：{e}")

# 🧾 ======================= JSON 載入工具 =======================

def load_json(file_path: str, fallback=None):
    """
    🧾 載入 JSON 檔案內容
    :param file_path: 路徑
    :param fallback: 讀取失敗時回傳的預設值
    :return: dict / list / fallback
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log.warning(f"❗ JSON 讀取失敗：{file_path}｜錯誤：{e}")
        return fallback

# 🧾 ======================= JSON 儲存工具 =======================

def save_json(data, file_path: str):
    """
    🧾 將資料儲存為 JSON 檔案
    :param data: dict / list
    :param file_path: 輸出路徑
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        log.success(f"✅ JSON 已儲存：{file_path}")
    except Exception as e:
        log.warning(f"❗ JSON 儲存失敗：{file_path}｜錯誤：{e}")

# 📝 ======================= 純文字讀取工具 =======================

def load_text(file_path: str, fallback: str = "") -> str:
    """
    📝 載入純文字檔案內容
    :param file_path: 檔案路徑
    :param fallback: 失敗時回傳的預設文字
    :return: str
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        log.warning(f"❗ 文字檔載入失敗：{file_path}｜錯誤：{e}")
        return fallback

# 📝 ======================= 純文字儲存工具 =======================

def save_text(content: str, file_path: str):
    """
    📝 儲存純文字內容到檔案
    :param content: 文字內容
    :param file_path: 儲存位置
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        log.success(f"✅ 文字檔已儲存：{file_path}")
    except Exception as e:
        log.warning(f"❗ 文字檔儲存失敗：{file_path}｜錯誤：{e}")

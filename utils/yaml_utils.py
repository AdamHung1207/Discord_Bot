# 📂 ======================= YAML 工具模組 =======================

import os                            # 🗂️ 檔案與路徑管理
import yaml                          # 📄 YAML 讀寫操作
from collections import OrderedDict  # 🧩 資料排序輔助
from utils.log_utils import write_log  # 📝 日誌管理

# 🧩 ======================= 讀取 YAML 檔案 =======================
def read_yaml(file_path: str) -> dict:
    """
    📖 讀取 YAML 檔案
    - 檔案不存在時，回傳空 dict
    - 發生錯誤時，自動回傳空 dict
    """
    if not os.path.exists(file_path):
        return {}

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file) or {}
            return data
    except Exception as e:
        write_log(f"🚨 讀取 YAML 發生錯誤：{e}")
        return {}

# 🧩 ======================= 寫入 YAML 檔案 =======================
def write_yaml(file_path: str, data: dict) -> None:
    """
    📝 寫入 YAML 檔案
    - 自動建立資料夾路徑
    - 自動格式化並排序 key
    - 轉換 OrderedDict 為普通 dict，避免寫入錯誤
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        # 自動排序 key，保持 YAML 乾淨一致
        sorted_data = sort_dict(data)

        # ✅ 避免 OrderedDict 寫入錯誤：轉為普通 dict
        def ordered_to_dict(obj):
            if isinstance(obj, OrderedDict):
                return {k: ordered_to_dict(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [ordered_to_dict(i) for i in obj]
            else:
                return obj

        clean_data = ordered_to_dict(sorted_data)

        with open(file_path, 'w', encoding='utf-8') as file:
            yaml.safe_dump(clean_data, file, allow_unicode=True, sort_keys=False)

    except Exception as e:
        write_log(f"🚨 寫入 YAML 發生錯誤：{e}")

# 🧩 ======================= 確保 YAML 檔案存在 =======================
def ensure_yaml_exists(file_path: str, default_data: dict = None) -> None:
    """
    🗂️ 確保 YAML 檔案存在
    - 不存在時自動建立，並可選擇填入預設資料
    """
    if not os.path.exists(file_path):
        default_data = default_data or {}
        write_yaml(file_path, default_data)

# 🧩 ======================= 合併 YAML 新資料 =======================
def merge_yaml(file_path: str, new_data: dict) -> None:
    """
    ➕ 合併新資料進現有 YAML
    - 自動讀取現有資料
    - 合併後自動排序並寫回 YAML
    """
    current_data = read_yaml(file_path)
    merged_data = deep_merge(current_data, new_data)

    # 📝 Debug log：確認合併後資料內容
    write_log(f"[Debug] merge_yaml｜file_path: {file_path}｜merged_data: {merged_data}")

    write_yaml(file_path, merged_data)

# 🧩 ======================= 深層合併字典工具 =======================
def deep_merge(source: dict, updates: dict) -> dict:
    """
    🔄 深層合併兩個字典
    """
    for key, value in updates.items():
        if isinstance(value, dict) and key in source and isinstance(source[key], dict):
            source[key] = deep_merge(source[key], value)
        else:
            source[key] = value
    return source

# 🧩 ======================= 排序字典工具 =======================
def sort_dict(data: dict) -> OrderedDict:
    """
    🧩 遞歸排序字典 key
    """
    if not isinstance(data, dict):
        return data
    return OrderedDict(
        sorted(
            ((key, sort_dict(value)) for key, value in data.items()),
            key=lambda x: x[0]
        )
    )

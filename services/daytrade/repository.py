# 📂 ======================= 資料存取層：手續費折數管理 =======================

import os  # 🗂️ 系統檔案管理
from utils.yaml_utils import read_yaml, write_yaml, ensure_yaml_exists, merge_yaml  # 📂 YAML 工具模組
from datetime import datetime  # 📅 時間處理工具

# 🧩 ======================= 基本檔案設定 =======================
DATA_FOLDER = os.path.join(os.path.dirname(__file__), 'data')  # 📂 資料夾路徑
USER_FEE_FILE = os.path.join(DATA_FOLDER, 'user_fee.yaml')  # 📄 用戶手續費 YAML 路徑

# 🧩 ======================= 初始化：確保 YAML 存在 =======================
ensure_yaml_exists(USER_FEE_FILE, default_data={
    "users": {},
    "default": {
        "fee_discount": 0.4  # 預設手續費折數：四折
    }
})

# 🧩 ======================= 讀取用戶折數 =======================
def get_user_fee_discount(user_id: int) -> float:
    """
    📖 讀取用戶的手續費折數
    - 若無設定則回傳預設值
    """
    data = read_yaml(USER_FEE_FILE)
    user_id_str = str(user_id)
    return data.get("users", {}).get(user_id_str, {}).get("fee_discount") or data.get("default", {}).get("fee_discount", 0.4)

# 🧩 ======================= 更新用戶折數 =======================
def update_user_fee_discount(user_id: int, fee_discount: float) -> None:
    """
    📝 更新用戶的手續費折數
    - 自動寫入 YAML 並更新時間戳記
    """
    user_id_str = str(user_id)
    update_data = {
        "users": {
            user_id_str: {
                "fee_discount": fee_discount,
                "last_update": datetime.now().strftime('%Y-%m-%d')
            }
        }
    }
    merge_yaml(USER_FEE_FILE, update_data)

# 🧩 ======================= 讀取所有用戶折數（可選擴充） =======================
def get_all_user_fee_discounts() -> dict:
    """
    📖 讀取所有用戶的手續費折數資料
    - 可用於報表或管理用途
    """
    data = read_yaml(USER_FEE_FILE)
    return data.get("users", {})

# 📂 ======================= 計算工具模組 =======================

import math  # ➗ 數學運算工具

# 🧩 ======================= 金額進位（手續費 / 稅金專用） =======================
def ceil_amount(value: float) -> int:
    """
    ⬆️ 將金額進位至整數（符合券商實務）
    - 用於：手續費、交易稅
    - 例如：68.1 ➔ 69
    """
    return math.ceil(value)

# 🧩 ======================= 通用四捨五入 =======================
def round_amount(value: float, digits: int = 2) -> float:
    """
    🔄 將數字四捨五入，預設保留 2 位小數
    - 用於：損益計算、比例計算
    """
    return round(value, digits)

# 🧩 ======================= 損益百分比計算 =======================
def calculate_profit_percentage(profit: float, cost: float) -> float:
    """
    📊 計算損益百分比
    - (損益金額 / 成本) * 100
    - 預設保留兩位小數
    - 若成本為 0，自動回傳 0，避免除零錯誤
    """
    if cost == 0:
        return 0.0
    return round((profit / cost) * 100, 2)

# 🧩 ======================= 安全除法（防止除以零） =======================
def safe_divide(numerator: float, denominator: float) -> float:
    """
    🛡️ 安全除法，避免除以零錯誤
    - 若分母為 0，回傳 0
    """
    if denominator == 0:
        return 0.0
    return numerator / denominator

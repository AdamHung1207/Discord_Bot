# 📂 ======================= 表格格式化工具模組 =======================

# 🧩 ======================= 數字格式化：加千分號 + 正負號 =======================
def format_number(value: float) -> str:
    """
    ➕ 將數字格式化為千分號並保留符號
    - 例如：+1,234 / -567 / ±0
    """
    if value > 0:
        return f"+{format(abs(int(value)), ',')}"
    elif value < 0:
        return f"-{format(abs(int(value)), ',')}"
    else:
        return "±0"

# 🧩 ======================= 產生表格表頭 =======================
def format_header() -> str:
    """
    🏷️ 輸出當沖計算表格的表頭
    """
    return "價位   | 損益金額\n--------|------------"

# 🧩 ======================= 格式化單行表格資料 =======================
def format_row(price: float, profit: float) -> str:
    """
    📊 格式化單行資料
    - 價格：保持 6 字符寬度對齊
    - 損益：格式化金額，對齊欄位
    """
    price_str = f"{price:<6}"  # 🧩 靠左對齊，寬度 6
    profit_str = f"{format_number(profit):>10}"  # 🧩 靠右對齊，寬度 10
    return f"{price_str} | {profit_str}"

# 🧩 ======================= 組合完整表格 =======================
def format_table(data: list) -> str:
    """
    🧾 組合整張表格
    - data: List of Tuple(price, profit)
    - 回傳格式化完成的字串
    """
    lines = [format_header()]
    for price, profit in data:
        lines.append(format_row(price, profit))
    return "\n".join(lines)

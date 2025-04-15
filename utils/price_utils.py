# 📂 ======================= 價格階梯工具模組 =======================

# 🧩 ======================= 獲取價格跳動單位 =======================
def get_tick_size(price: float) -> float:
    """
    🧮 傳入股價，自動回傳對應的跳動價差
    - 依照台股股價階梯對照表
    """
    if price < 10:
        return 0.01
    elif price < 50:
        return 0.05
    elif price < 100:
        return 0.1
    elif price < 500:
        return 0.5
    elif price < 1000:
        return 1.0
    else:
        return 5.0

# 🧩 ======================= 生成價格區間列表 =======================
def generate_price_range(center_price: float, tick_count: int) -> list:
    """
    📊 依據中心價格與檔數，生成價格區間清單（由高至低）
    - center_price：中心價格（float）
    - tick_count：上下檔數（int）
    - 回傳：由高到低的價格列表
    """
    tick_size = get_tick_size(center_price)
    price_range = []

    # 計算範圍：由高到低
    for i in range(tick_count, -tick_count - 1, -1):
        price = round(center_price + (tick_size * i), 2)
        if price > 0:  # 🛡️ 確保價格不能為負
            price_range.append(price)

    return price_range

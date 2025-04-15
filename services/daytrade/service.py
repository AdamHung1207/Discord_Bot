# 📂 ======================= 業務邏輯層：當沖功能 =======================

from services.daytrade import repository
from utils.price_utils import get_tick_size  # 📈 價格跳動單位
from utils.calc_utils import round_amount  # 🔄 四捨五入工具
from utils.date_utils import get_today_date_str  # 📅 日期工具
from utils.log_utils import write_log  # 📝 日誌管理

# 📊 交易成本參數
FEE_RATE = 0.001425  # 手續費率 0.1425%
TAX_RATE = 0.0015    # 證交稅率 0.15%

# 🧩 格式化金額（加上千分位符號）
def _format_currency(amount: float) -> str:
    amount = int(amount)
    return f"{amount:+,} 元"

# 🧩 分組行數（為避免 Discord 限制，建議 8～10）
GROUP_SIZE = 8

# 🧩 ======================= 當沖試算：共用邏輯 =======================
def _generate_daytrade_message(user_id: int, price: float, quantity: int, range_count: int, trade_type: str) -> dict:
    today = get_today_date_str()
    fee_discount = repository.get_user_fee_discount(user_id)
    display_discount = round_amount(fee_discount * 10, 1)
    is_custom = str(user_id) in repository.get_all_user_fee_discounts()
    fee_text = f"{display_discount} 折（{'自訂' if is_custom else '預設'}）"

    write_log(f"[當沖試算] user_id: {user_id}｜trade_type: {trade_type}｜price: {price}｜quantity: {quantity}｜range: {range_count}｜fee_discount: {fee_discount}")

    # ✅ 價格列表（動態計算，跨區間重算 tick size）
    price_list = []

    # ✅ 向上價格區間
    current_price_up = price
    for _ in range(range_count):
        tick_size = get_tick_size(current_price_up)
        current_price_up = round_amount(current_price_up + tick_size, 2)
        price_list.append(current_price_up)

    # ✅ 當前價格
    price_list.append(price)

    # ✅ 向下價格區間（✅ 已修正：動態 tick size）
    current_price_down = price
    for _ in range(range_count):
        tentative_price = round_amount(current_price_down - get_tick_size(current_price_down), 2)
        tick_size = get_tick_size(tentative_price)
        current_price_down = round_amount(current_price_down - tick_size, 2)
        price_list.append(current_price_down)

    # ✅ 價格高到低排序
    price_list = sorted(price_list, reverse=True)

    # 📊 組合結果行
    result_lines = []

    for target_price in price_list:
        price_diff = target_price - price
        profit_per_share = price_diff if trade_type == "buy" else -price_diff
        gross_profit = profit_per_share * quantity * 1000

        buy_price = price if trade_type == "buy" else target_price
        sell_price = target_price if trade_type == "buy" else price

        fee_day = (buy_price + sell_price) * quantity * 1000 * FEE_RATE * fee_discount
        tax = sell_price * quantity * 1000 * TAX_RATE
        net_profit_day = gross_profit - fee_day - tax

        fee_full = (buy_price + sell_price) * quantity * 1000 * FEE_RATE
        rebate = fee_full * (1 - fee_discount)
        net_profit_month_now = gross_profit - fee_full - tax
        net_profit_month_rebate = rebate

        net_profit_day = round_amount(net_profit_day, 0)
        net_profit_month_now = round_amount(net_profit_month_now, 0)
        net_profit_month_rebate = round_amount(net_profit_month_rebate, 0)

        # ✅ 標示顏色符號（台股紅漲綠跌）
        if net_profit_day > 0:
            color_emoji = "🔴"
            arrow_emoji = "🔺"
        elif net_profit_day < 0:
            color_emoji = "🟢"
            arrow_emoji = "🔻"
        else:
            color_emoji = "⚪"
            arrow_emoji = "➖"

        is_current_price = target_price == price
        current_price_marker = " ← 🎯 當前價格" if is_current_price else ""

        month_profit_text = f"{_format_currency(net_profit_month_now)} ({_format_currency(net_profit_month_rebate)})"

        profit_text = (
            f"{color_emoji} {arrow_emoji} "
            f"{'**' if is_current_price else ''}{target_price}{'**' if is_current_price else ''} ｜ "
            f"日退：{_format_currency(net_profit_day)} ｜ 月退：{month_profit_text}"
            f"{current_price_marker}"
        )

        result_lines.append(profit_text)

    # ✅ 分欄位結果切割
    def split_lines(lines):
        return [lines[i:i + GROUP_SIZE] for i in range(0, len(lines), GROUP_SIZE)]

    line_groups = split_lines(result_lines)

    # ✅ Embed 欄位組裝
    fields = [
        {
            "name": "🧾 試算參數",
            "value": f"📅 日期：{today}\n💰 張數：{quantity} 張\n🧾 手續費：{fee_text}",
            "inline": False
        }
    ]

    for idx, group in enumerate(line_groups):
        fields.append({
            "name": f"💹 價格區間損益（區間 {idx + 1}）",
            "value": "```diff\n" + "\n".join(group) + "\n```",
            "inline": False
        })

    fields.append({
        "name": "📄 說明提醒",
        "value": "📄 日退：立即入帳。\n📄 月退：當下實收 + 括號內次月退費。\n📄 當前價格已標示「← 🎯 當前價格」",
        "inline": False
    })

    message = {
        "title": f"📊 當沖{'買進' if trade_type == 'buy' else '賣出'}試算結果",
        "fields": fields,
        "color": 0x00FF00 if trade_type == "buy" else 0xFF0000
    }

    return message

# 🧩 ======================= 當沖試算：買單 =======================
def get_daytrade_buy_message(user_id: int, price: float, quantity: int, range_count: int) -> dict:
    return _generate_daytrade_message(user_id, price, quantity, range_count, trade_type="buy")

# 🧩 ======================= 當沖試算：賣單 =======================
def get_daytrade_sell_message(user_id: int, price: float, quantity: int, range_count: int) -> dict:
    return _generate_daytrade_message(user_id, price, quantity, range_count, trade_type="sell")

# 🧩 ======================= 手續費折數查詢 =======================
def get_user_fee_discount_message(user_id: int) -> str:
    fee_discount = repository.get_user_fee_discount(user_id)
    today = get_today_date_str()
    data = repository.get_all_user_fee_discounts()
    is_custom = str(user_id) in data
    display_discount = round_amount(fee_discount * 10, 1)
    status_emoji = "🔧 已自訂折數" if is_custom else "📝 使用預設折數"

    return (
        f"📅 日期：{today}\n"
        f"🔍 目前手續費折數：{display_discount} 折\n"
        f"{status_emoji}"
    )

# 🧩 ======================= 手續費折數修改 =======================
def set_user_fee_discount(user_id: int, fee_discount: float) -> str:
    if not (1.0 <= fee_discount <= 9.0):
        return "🚨 錯誤：請輸入有效的折數範圍（1.0 ~ 9.0）"

    store_discount = round_amount(fee_discount / 10, digits=2)
    repository.update_user_fee_discount(user_id, store_discount)

    data = repository.get_all_user_fee_discounts()
    is_custom = str(user_id) in data
    status_emoji = "🔧 已自訂折數" if is_custom else "📝 使用預設折數"

    today = get_today_date_str()
    return (
        f"✅ 設定成功！\n"
        f"📅 日期：{today}\n"
        f"🔧 更新手續費折數為：{fee_discount} 折\n"
        f"{status_emoji}"
    )

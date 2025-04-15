# 📂 ======================= 控制層：當沖功能 =======================

import discord  # 📦 Discord 套件
from services.daytrade import service  # 🧩 當沖邏輯層
from utils.log_utils import log  # 📝 日誌管理

# 🧩 ======================= 建立 Embed 工具 =======================
def _build_embed(message_data: dict) -> discord.Embed:
    """
    🧩 建立 Discord Embed 物件
    :param message_data: 從 service.py 回傳的格式化 dict
    :return: discord.Embed 物件
    """
    # ✅ 初始化 Embed，設定標題與顏色
    embed = discord.Embed(
        title=message_data.get("title", "📊 當沖試算結果"),
        color=message_data.get("color", 0x00FF00)
    )

    # ✅ 加入每一個欄位
    for field in message_data.get("fields", []):
        embed.add_field(
            name=field.get("name", ""),
            value=field.get("value", ""),
            inline=field.get("inline", False)
        )

    # ✅ 可擴充：加上底部備註
    embed.set_footer(text="試算結果僅供參考，實際交易請以券商成交資訊為準。")

    return embed

# 🧩 ======================= 當沖買進：Embed 回傳 =======================
def get_daytrade_buy_embed(user_id: int, price: float, quantity: int, range_count: int) -> discord.Embed:
    """
    📊 當沖買進試算 Embed
    """
    log.info(f"[當沖試算-BUY] user_id: {user_id}｜price: {price}｜quantity: {quantity}｜range: {range_count}")

    # ✅ 呼叫 service.py 邏輯計算
    message_data = service.get_daytrade_buy_message(user_id, price, quantity, range_count)

    # ✅ 組裝成 Discord Embed
    return _build_embed(message_data)

# 🧩 ======================= 當沖賣出：Embed 回傳 =======================
def get_daytrade_sell_embed(user_id: int, price: float, quantity: int, range_count: int) -> discord.Embed:
    """
    📊 當沖賣出試算 Embed
    """
    log.info(f"[當沖試算-SELL] user_id: {user_id}｜price: {price}｜quantity: {quantity}｜range: {range_count}")

    # ✅ 呼叫 service.py 邏輯計算
    message_data = service.get_daytrade_sell_message(user_id, price, quantity, range_count)

    # ✅ 組裝成 Discord Embed
    return _build_embed(message_data)

# 🧩 ======================= 手續費折數查詢 =======================
def handle_fee_discount_query(user_id: int) -> str:
    """
    📖 查詢手續費折數訊息
    """
    log.info(f"[手續費查詢] user_id: {user_id}")

    return service.get_user_fee_discount_message(user_id)

# 🧩 ======================= 手續費折數修改 =======================
def handle_fee_discount_update(user_id: int, fee_discount: float) -> str:
    """
    📝 修改手續費折數
    """
    log.info(f"[手續費修改] user_id: {user_id}｜fee_discount: {fee_discount}")

    return service.set_user_fee_discount(user_id, fee_discount)

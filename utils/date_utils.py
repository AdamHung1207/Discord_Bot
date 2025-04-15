# 📂 ======================= 日期處理工具模組 =======================

from datetime import datetime, timedelta  # 📅 日期與時間管理

# 🧩 ======================= 取得今日日期字串 =======================
def get_today_date_str() -> str:
    """
    📅 取得今日日期字串（格式：YYYY-MM-DD）
    """
    return datetime.now().strftime('%Y-%m-%d')

# 🧩 ======================= 格式化日期物件 =======================
def format_date(date_obj: datetime) -> str:
    """
    🗓️ 將日期物件格式化為字串（格式：YYYY-MM-DD）
    """
    return date_obj.strftime('%Y-%m-%d')

# 🧩 ======================= 取得目前完整日期時間字串 =======================
def get_current_datetime_str() -> str:
    """
    ⏰ 取得目前日期與時間字串（格式：YYYY-MM-DD HH:MM:SS）
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 🧩 ======================= 取得昨日日期字串 =======================
def get_yesterday_date_str() -> str:
    """
    📆 取得昨日日期字串（格式：YYYY-MM-DD）
    """
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')

# 🧩 ======================= 取得指定區間日期列表 =======================
def get_date_range(start_days_ago: int, end_days_ago: int) -> list:
    """
    🔄 計算指定天數範圍的日期列表
    - start_days_ago: 開始天數前（int）
    - end_days_ago: 結束天數前（int）
    - 回傳：日期字串列表（由近至遠）
    """
    today = datetime.now()
    return [
        (today - timedelta(days=day)).strftime('%Y-%m-%d')
        for day in range(start_days_ago, end_days_ago - 1, -1)
    ]

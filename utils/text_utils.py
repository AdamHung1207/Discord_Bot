# 📂 ======================= 文字處理工具模組 =======================

# 🧩 ======================= 補空白對齊工具 =======================
def pad_text(text: str, width: int, align: str = 'left') -> str:
    """
    📏 補空白，控制文字對齊
    - align: 'left' / 'right' / 'center'
    """
    text = str(text)
    if align == 'right':
        return text.rjust(width)
    elif align == 'center':
        return text.center(width)
    else:
        return text.ljust(width)

# 🧩 ======================= 當前價位標記工具 =======================
def mark_current_price(text: str) -> str:
    """
    ➡️ 標記當前價位
    - 在文字前加上箭頭符號
    """
    return f"➡️ {text}"

# 🧩 ======================= 加入 Emoji 裝飾 =======================
def add_emoji(text: str, emoji: str) -> str:
    """
    😊 在文字旁邊加上 emoji
    - 例如：add_emoji("損益", "🔥") ➔ "損益 🔥"
    """
    return f"{text} {emoji}"

# 🧩 ======================= 多文字組合工具 =======================
def combine_text(*args) -> str:
    """
    🔗 多段文字組合，保持整齊格式
    - 自動以空白分隔
    """
    return " ".join(str(arg) for arg in args if arg)

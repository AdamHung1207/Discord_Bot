import os                       # 📁 存取作業系統功能（如讀取環境變數）
from dotenv import load_dotenv  # 🔐 載入 .env 檔案內容（通常放機密設定）

# 📦 載入 .env 檔案中的環境變數（如 Discord Token、Owner ID）
load_dotenv()

# 🔐 Discord Bot 設定
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")               # ✅ Discord Bot Token
OWNER_ID = int(os.getenv("OWNER_ID", "0"))               # 👤 Bot 擁有者 ID（限定指令用）

# ⚙️ 機器人設定參數
COMMAND_PREFIX = "!"                                     # 🔣 指令前綴符號（可改從 .env 取）
DEFAULT_USERNAME = "未知使用者"                          # 🧑‍💻 啟動畫面顯示用名稱
DEBUG_MODE = False                                       # 🐞 是否啟用除錯模式（未來可使用）

# 📂 資料夾與檔案路徑
DATA_DIR = "data"                                        # 📁 存放 JSON 檔案的資料夾名稱

# 📁 Cog 模組清單（按英文順序）
COGS = [
    "choose_cogs",    # 🎲 隨機選擇
    "clear_cogs",     # 🧹 清除訊息
    "lucky_cogs",     # 🍀 幸運籤詩
    "picture_cogs",   # 🖼️ 隨機圖片
    "sync_cogs",      # 🔄 同步指令
    "tarot_cogs",     # 🔮 塔羅牌功能
    "zhezhe_cogs"     # 📸 哲哲語錄
]

# 📊 常用 JSON 檔案（可搭配迴圈統計筆數）
JSON_FILES = {
    "選擇回答": "choose_answer.json",
    "選擇倒數語": "choose_countdown.json",
    "分隔樣式": "choose_divider.json",
    "幸運動畫": "lucky_Anime.json",
    "幸運顏色": "lucky_color.json",
    "幸運倒數": "lucky_countdown.json",
    "幸運籤詩": "lucky_fortunes.json",
    "吉祥建議": "lucky_suggestions.json",
    "塔羅大牌": "tarot_big.json",
    "塔羅小牌": "tarot_small.json",
    "塔羅倒數": "tarot_countdown.json",
    "哲哲圖片": "zhezhe_images.json"
}

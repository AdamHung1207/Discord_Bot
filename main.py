import discord                      # 🤖 Discord API 主套件
from discord.ext import commands    # 🧠 Cog 擴充指令系統
import asyncio                      # ⏱️ 非同步處理（for sleep）
from config import (                # ⚙️ 匯入所有設定
    DISCORD_TOKEN,
    COMMAND_PREFIX,
    DEFAULT_USERNAME,
    COGS,
    JSON_FILES,
    DATA_DIR
)
from utils import (                 # 🛠️ 匯入自訂工具函式
    count_json,
    print_startup_message
)

# 🧠 初始化 Bot（設定前綴與權限）
intents = discord.Intents.default()
intents.message_content = True           # ✅ 啟用 message content 權限
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

# 🟢 當機器人成功啟動時
@bot.event
async def on_ready():
    # 📊 統計所有 JSON 資料筆數（搭配 JSON_FILES 與 DATA_DIR）
    json_status = []
    for desc, filename in JSON_FILES.items():
        full_path = f"{DATA_DIR}/{filename}"
        count = count_json(full_path)
        json_status.append(f"✅ {count} 筆{desc} - 來源: {full_path}")

    # 🧠 載入所有 Cogs 模組並紀錄狀態
    cog_status = []
    for cog in COGS:
        try:
            await bot.load_extension(f"cogs.{cog}")
            cog_status.append(f"🟢 {cog:<15} ➝ ✅ 載入成功")
        except Exception as e:
            cog_status.append(f"🔴 {cog:<15} ➝ ❌ 載入失敗：{e}")

    # 🖨️ 顯示完整啟動畫面
    print_startup_message(json_status, cog_status, username=DEFAULT_USERNAME)

# 🚀 啟動 Bot（從 .env 中取得 Token）
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)

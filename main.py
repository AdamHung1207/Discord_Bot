import discord                          # 引入 Discord API 套件
from discord.ext import commands        # 引入擴展命令模組，用於管理 Bot 指令
from discord import app_commands        # 用於斜線指令（Application Commands）
from dotenv import load_dotenv          # 載入 .env 檔案中的環境變數
import os                               # 操作系統模組，用於讀取環境變數
import asyncio                          # 異步功能模組，用於管理協程
from datetime import datetime           # 日期時間模組，用於顯示執行時間
from colorama import init, Fore, Style  # 色彩模組，用於終端文字顯示
import logging                          # 記錄模組，用於記錄程式執行訊息

# 初始化 colorama（確保終端字體顏色自動重置）
init(autoreset=True)

# 設定 logging（用於記錄程式執行日誌，INFO 級別以上的訊息都會被記錄）
logging.basicConfig(
    level=logging.INFO,  # 設定記錄級別為 INFO
    format="%(asctime)s - %(levelname)s - %(message)s"  # 記錄格式：時間、級別、訊息
)

# 載入 .env 環境變數檔案（包括敏感的 Token 和 ID 資訊）
load_dotenv()

# 從環境變數中讀取 DISCORD_TOKEN 和 OWNER_ID
TOKEN = os.getenv('DISCORD_TOKEN')       # 機器人 Token
OWNER_ID = os.getenv('OWNER_ID')         # 擁有者的 Discord ID

# 檢查是否成功讀取 Token 和 Owner ID，若未設置則拋出錯誤
if not TOKEN:
    raise ValueError("❌ 環境變數 DISCORD_TOKEN 未設置！")  # 提示未設置 Token
if not OWNER_ID:
    raise ValueError("❌ 環境變數 OWNER_ID 未設置！")       # 提示未設置 Owner ID
OWNER_ID = int(OWNER_ID)                                   # 確保 OWNER_ID 轉換為整數型態

# 設定 Intents 權限（用於控制 Bot 能夠收到哪些事件）
intents = discord.Intents.default()                        # 使用 Discord 提供的預設權限
intents.message_content = True                             # 額外啟用讀取訊息內容權限

# 建立 Bot 實例（指令前綴設定為 '!' 並附加設定的 Intents 權限）
bot = commands.Bot(command_prefix='!', intents=intents)

# 定義 Cog 擴展模組列表（功能模組路徑）
cogs = [
    'cogs.choose_cogs',                                    # 🎲 多選一       - 功能模組
    'cogs.clear_cogs',                                     # 🧹 清理訊息     - 功能模組
    'cogs.lucky_cogs',                                     # 🍀 今日運勢     - 功能模組
    'cogs.picture_cogs',                                   # 🖼️ 圖片統整     - 功能模組
    'cogs.sync_cogs',                                      # 🔄 手動同步     - 功能模組
    'cogs.tarot_cogs',                                     # 🎴 塔羅牌       - 功能模組
    'cogs.zhezhe_cogs',                                    # 😂 哲哲梗圖     - 功能模組
]

# 定義異步加載功能模組的函數
async def load_cogs():
    tasks = [bot.load_extension(cog) for cog in cogs]               # 準備加載每個模組的任務
    results = await asyncio.gather(*tasks, return_exceptions=True)  # 執行加載並收集結果
    
    print("\n" + "=" * 50)
    print(Fore.CYAN + f"🎉  Bot 安裝已經完成 🚀【{bot.user}】 已成功啟動！")
    print("📅 當前時間：" + Fore.YELLOW + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("=" * 50 + "\n")
    
    for cog, result in zip(cogs, results):                                   # 遍歷加載結果並打印至終端
        if isinstance(result, Exception):
            print(Fore.RED + f"❌ [FAILED] {cog:<20} ➝ 加載失敗：{result}")  # 顯示失敗模組
            logging.error(f"❌ {cog} 加載失敗：{result}")                     # 記錄失敗資訊
        else:
            print(Fore.GREEN + f"✅ [OK]    {cog:<20} ➝ 加載成功")           # 顯示成功模組
            logging.info(f"✅ {cog} 加載成功")  # 記錄成功資訊
    print("\n🚀 伺服器正在運行，Bot【#3898】已準備就緒！ 🟢\n")                 # 最後提示 Bot 啟動完成

# Bot 啟動事件，當 Bot 上線時觸發
@bot.event
async def on_ready():
    await load_cogs()                           # 加載所有功能模組
    await bot.tree.sync()                       # 同步斜線指令
    logging.info(f"🚀 {bot.user} 已準備就緒！")  # 記錄 Bot 啟動完成訊息

# 錯誤處理事件（當指令錯誤時觸發）
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("⚠️ 沒有這個指令喔！")                    # 未找到指令的提示
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ 指令缺少必要參數！")                  # 指令缺少參數的提示
    elif isinstance(error, commands.NotOwner):
        await ctx.send("🚫 只有擁有者可以執行這個指令！")         # 非擁有者嘗試執行限制指令
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("❌ Bot 欠缺必要權限，請檢查伺服器設定！")  # Bot 權限不足的提示
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("❌ 指令執行發生錯誤，請稍後再試！")        # 指令執行發生錯誤的提示
    else:
        await ctx.send(f"❌ 發生未知錯誤：{str(error)}")         # 提示未知錯誤

# 啟動 Bot，根據 TOKEN 執行程式
bot.run(TOKEN)

# 📂 ======================= 基本套件導入 =======================

import os                  # 🗂️ 系統檔案與環境變數管理
from dotenv import load_dotenv  # 🛠️ 載入 .env 環境變數

# ✅ 載入 .env 環境變數檔案
load_dotenv()

# 🧩 ======================= Discord Bot 基本設定 =======================

# 🔑 Discord Bot Token（從 .env 讀取，啟動 Bot 時使用）
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# 💬 指令前綴符號（例如：! 或 /）
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")

# 🌍 環境模式（DEV：開發模式 / PROD：生產模式）
ENV_MODE = os.getenv("ENV_MODE", "PROD").upper()

# 🏷️ 版本號（目前 Bot 版本）
VERSION = os.getenv("VERSION", "v1.0.0")

# 🧹 Log 保留天數（單位：天）
LOG_RETAIN_DAYS = int(os.getenv("LOG_RETAIN_DAYS", "3"))

# 🗝️ API Token（例如 FinMind API，用於擴展功能）
FINMIND_API_TOKEN = os.getenv("FINMIND_API_TOKEN", "")

# 🧩 ======================= 路徑設定 =======================

# 📁 log 資料夾路徑
LOG_DIR = "logs"

# 📁 指令模組 (Cogs) 資料夾路徑
COGS_DIR = "cogs"

# 📁 服務模組 (Services) 資料夾路徑
SERVICES_DIR = "services"

# 🗂️ 每個 service 的 data 路徑，統一在各自的 services/XXX/data/
# ✅ config.py 不再管理 JSON / YAML 清單，由各 service 自主管理

# 🧩 ======================= 全局設定 =======================

# 📝 Log 記錄選項
LOG_TO_CONSOLE = False                   # ❌ 預設不輸出到終端機，僅寫入 log 檔案
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  # 🛠️ 預設日誌層級

# 🔍 自動掃描功能模組開關（cogs 與 services）
AUTO_SCAN_COGS = True                   # ✅ 啟動時自動掃描 cogs 模組
AUTO_SCAN_SERVICES = True               # ✅ 預留：啟動時自動掃描 services/controller.py

# 🚨 異常處理模式
STRICT_ERROR_HANDLING = True            # ✅ 嚴格模式：遇到異常即時記錄 log

# 🧩 ======================= 配置總結輸出 =======================

# ✅ 啟動時輸出環境設定簡報（用於 debug / 啟動記錄）
print(f"✅ 配置檔 config.py 載入完成：")
print(f"   └─ 環境模式：{ENV_MODE}")
print(f"   └─ 版本號：{VERSION}")
print(f"   └─ LOG 保留天數：{LOG_RETAIN_DAYS} 天")
print(f"   └─ 自動掃描 COGS：{AUTO_SCAN_COGS}")
print(f"   └─ 自動掃描 SERVICES：{AUTO_SCAN_SERVICES}")
print(f"   └─ Log 層級：{LOG_LEVEL}")
print(f"   └─ Log 輸出至終端機：{LOG_TO_CONSOLE}")

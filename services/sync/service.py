# 📂 ======================= 同步模組服務 =======================

import subprocess                          # 🖥️ 執行終端指令
from datetime import datetime             # 📅 時間戳記
from utils.log_utils import log_info, log_error  # 📝 日誌工具
from config import SYNC_SCRIPT_PATH       # ⚙️ 同步腳本路徑


# 🔄 執行同步模組
def sync_module(module_name: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        result = subprocess.run(
            ["python", SYNC_SCRIPT_PATH, module_name],
            capture_output=True,
            text=True,
            check=True
        )
        log_info("sync", f"✅ [{timestamp}] 成功同步模組：{module_name}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        log_error("sync", f"❌ [{timestamp}] 同步模組失敗：{module_name}，錯誤：{e.stderr.strip()}")
        return None

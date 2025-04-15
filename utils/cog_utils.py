# 📂 ======================= 基本套件導入 =======================

import os                                                    # 🗂️ 系統檔案操作
import asyncio                                               # ⏱️ 異步協程
from watchdog.observers import Observer                      # 👀 檔案監控（熱重載）
from watchdog.events import FileSystemEventHandler
from config import COGS_DIR, AUTO_SCAN_COGS, LOG_TO_CONSOLE  # ⚙️ 全局設定
from utils.log_utils import log_message                      # 📝 log 工具

# 🧩 ======================= 自動載入 Cogs =======================

async def load_all_cogs(bot, cog_status: list, log_to_console: bool = LOG_TO_CONSOLE):
    """
    📂 自動載入 cogs 資料夾內所有指令模組
    :param bot: Discord Bot 實例
    :param cog_status: 載入狀態記錄列表
    :param log_to_console: 是否輸出到終端機（由 config 控制）
    """
    if not AUTO_SCAN_COGS:
        log_message("⚠️ Cogs 自動掃描功能已關閉。", level="WARNING", print_to_console=log_to_console)
        return

    success_count = 0
    fail_count = 0

    # 📂 掃描 cogs 資料夾
    for filename in os.listdir(COGS_DIR):
        if filename.endswith(".py") and not filename.startswith("_"):
            cog_name = filename[:-3]  # 去除 .py 副檔名
            module_path = f"{COGS_DIR.replace('/', '.')}.{cog_name}"

            try:
                await bot.load_extension(module_path)
                log_message(f"✅ 成功載入 Cog：{cog_name}", level="SUCCESS", print_to_console=log_to_console)
                cog_status.append(f"✅ {cog_name} 載入成功")
                success_count += 1
            except Exception as e:
                log_message(f"❌ 載入 Cog 失敗：{cog_name}｜錯誤：{e}", level="ERROR", print_to_console=log_to_console)
                cog_status.append(f"❌ {cog_name} 載入失敗：{e}")
                fail_count += 1

    log_message(
        f"🧩 Cogs 載入完成：成功 {success_count} 個，失敗 {fail_count} 個，總共 {success_count + fail_count} 個。",
        level="INFO",
        print_to_console=log_to_console
    )

# 🧩 ======================= 模組熱重載 =======================

async def hot_reload_cogs(bot, cog_status: list, log_to_console: bool = LOG_TO_CONSOLE):
    """
    🔄 熱重載：監控 cogs 資料夾，檔案變動自動重新載入
    :param bot: Discord Bot 實例
    :param cog_status: 載入狀態記錄列表
    :param log_to_console: 是否輸出到終端機（由 config 控制）
    """
    class CogReloadHandler(FileSystemEventHandler):
        async def reload(self, event):
            if event.src_path.endswith(".py"):
                cog_name = os.path.splitext(os.path.basename(event.src_path))[0]
                module_path = f"{COGS_DIR.replace('/', '.')}.{cog_name}"

                try:
                    await bot.reload_extension(module_path)
                    log_message(f"🔄 熱重載成功：{cog_name}", level="SUCCESS", print_to_console=log_to_console)
                except Exception as e:
                    log_message(f"❌ 熱重載失敗：{cog_name}｜錯誤：{e}", level="ERROR", print_to_console=log_to_console)

        def on_modified(self, event):
            asyncio.run_coroutine_threadsafe(self.reload(event), bot.loop)

    event_handler = CogReloadHandler()
    observer = Observer()
    observer.schedule(event_handler, path=COGS_DIR, recursive=False)
    observer.start()

    log_message("👀 已啟用 Cogs 熱重載功能。", level="INFO", print_to_console=log_to_console)

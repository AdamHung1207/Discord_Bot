import json                        # 📦 用於讀取 JSON 檔案
from datetime import datetime      # 🕒 用於產生現在時間字串

# 🔧 函式：統計指定 JSON 檔案內的資料筆數
# 📌 若成功，回傳資料筆數（int）
# 📌 若失敗，回傳錯誤訊息字串（str）
def count_json(file_path):
    try:
        # 📂 嘗試開啟並解析 JSON 檔案
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return len(data)  # ✅ 成功則回傳 JSON 資料的筆數
    except Exception as e:
        # ❌ 失敗時顯示錯誤訊息
        return f"❌ 無法讀取 {file_path}：{e}"

# 🌟 函式：印出 Bot 啟動畫面
# 參數：
#   - json_status：每個 JSON 載入狀態字串組成的列表
#   - cog_status：每個 cog 載入結果組成的列表
#   - username：啟動者 Discord 名稱（預設為「未知使用者」）
def print_startup_message(json_status: list[str], cog_status: list[str], username: str = "未知使用者"):
    # 🕒 取得現在時間
    startup_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 🖨️ 印出主標題區塊
    print("╔══════════════════════════════════════════════╗")
    print("║        🤖 Discord Bot 啟動成功！              ║")
    print("╠══════════════════════════════════════════════╣")
    print(f"║ 👤 使用者：{username:<30}║")
    print(f"║ 🕒 啟動時間：{startup_time:<22}║")
    print("╚══════════════════════════════════════════════╝\n")

    # 📦 顯示 JSON 載入統計狀態
    print("📦 JSON 資料載入狀態：")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    for line in json_status:
        print(line)
    print("")

    # 🧠 顯示 Cog 模組載入狀態
    print("🧠 Cogs 載入狀態：")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    for line in cog_status:
        print(line)
    print("")

    # 🎉 完成提示
    print("🎉 Bot 狀態：已準備就緒！正在等待指令輸入中…\n")

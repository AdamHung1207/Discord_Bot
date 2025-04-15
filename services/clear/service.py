# 📂 ======================= 基本套件導入 =======================

import discord                                               # 🤖 Discord API
import random                                                # 🎲 隨機選擇訊息模板
from services.clear.repository import load_success_messages  # 📂 讀取成功訊息
from utils.log_utils import log_message                      # 📝 log 記錄工具

# 🧩 ======================= 清除訊息核心邏輯 =======================

async def delete_messages_service(interaction: discord.Interaction, amount: int, user: discord.Member = None):
    """
    🧹 執行清除訊息邏輯
    :param interaction: Discord 互動對象
    :param amount: 要刪除的訊息數量
    :param user: 指定要刪除的用戶（可選）
    """

    # ✅ 資料初始化
    success_messages = load_success_messages()

    # ⚠️ 輸入檢查：數字不能小於等於 0
    if amount <= 0:
        await interaction.response.send_message("⚠️ 請輸入大於 0 的數字！", ephemeral=True)
        return

    # ⚠️ 輸入檢查：Discord 限制 100 則內
    if amount > 100:
        await interaction.response.send_message("⚠️ 一次最多只能刪除 100 則訊息！", ephemeral=True)
        return

    # ⏳ 延遲回應，避免互動超時
    await interaction.response.defer(ephemeral=True)

    # 🔍 定義訊息刪除篩選條件
    def check(msg: discord.Message):
        if msg.pinned:
            return False  # 📌 排除置頂訊息
        if user:
            return msg.author == user  # 🎯 只刪除指定用戶訊息
        return True  # ✅ 預設：刪除所有非置頂訊息

    try:
        # 🧹 執行訊息清除
        deleted = await interaction.channel.purge(limit=amount, check=check)

        # 🎯 隨機挑選成功訊息模板並格式化數量
        response_template = random.choice(success_messages)
        response_message = response_template.format(count=len(deleted))

        # ✅ 回傳成功訊息（隱藏訊息，只有操作者可見）
        await interaction.followup.send(response_message, ephemeral=True)

        # 📝 log 紀錄操作結果
        log_message(f"✅ {interaction.user} 成功清除 {len(deleted)} 則訊息。", level="SUCCESS", print_to_console=False)

    except discord.Forbidden:
        # ❌ 權限不足錯誤提示
        await interaction.followup.send("❌ 我沒有權限刪除訊息，請確認機器人權限！", ephemeral=True)
        log_message(f"❌ {interaction.user} 嘗試刪除訊息，但權限不足。", level="ERROR", print_to_console=False)

    except Exception as e:
        # 🛑 其他未知錯誤處理
        await interaction.followup.send(f"❌ 清除失敗：{str(e)}", ephemeral=True)
        log_message(f"❌ {interaction.user} 嘗試刪除訊息失敗：{e}", level="ERROR", print_to_console=False)

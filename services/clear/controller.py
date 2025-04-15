# 📂 ======================= 基本套件導入 =======================

import discord                                              # 🤖 Discord API
from services.clear.service import delete_messages_service  # 🧩 清除訊息核心邏輯
from utils.error_utils import try_catch                     # 🛡️ 裝飾器：異常捕獲

# 🧩 ======================= 控制層：對外接口 =======================

@try_catch
async def handle_clear_command(interaction: discord.Interaction, amount: int, user: discord.Member = None):
    """
    🎮 清除訊息控制器
    :param interaction: Discord 互動對象
    :param amount: 要刪除的訊息數量
    :param user: 指定要刪除訊息的用戶（可選）
    """
    await delete_messages_service(interaction, amount, user)

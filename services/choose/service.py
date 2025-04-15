# 📂 ======================= 基本套件導入 =======================

import random                            # 🎲 隨機模組
import discord                           # 🤖 Discord Embed 嵌入訊息
from utils.log_utils import log_message  # 📝 日誌統一管理
from services.choose.repository import ( # 📦 匯入資料存取層
    load_answer_messages,
    load_dividers
)

# 🧩 ======================= 核心邏輯：產生選擇結果 Embed =======================

def get_choice_result(choices: list, user: discord.User = None) -> discord.Embed:
    """
    🎯 根據使用者選項產生嵌入式訊息作為選擇結果
    :param choices: 使用者輸入的選項清單
    :param user: Discord 使用者（用於 log 紀錄）
    :return: discord.Embed 格式的結果
    """

    # 📦 載入 YAML 資料
    answer_messages = load_answer_messages()
    dividers = load_dividers()

    # 🎲 開始隨機抽選
    rand = random.random()

    # 🎨 建立 Embed 訊息
    embed = discord.Embed(title="命運選擇", color=discord.Color.random())
    embed.add_field(name="🎲【選項清單】", value="、".join(choices), inline=False)

    # 📝 預設結果描述（供 log 使用）
    result_description = ""

    # 🎉 判斷隨機結果
    if rand < 0.01:
        # 🎉 1% 全選
        result_description = f"命運選擇了全部：{'、'.join(choices)}！"
        embed.add_field(
            name="🎉【驚喜】奇蹟發生！",
            value=result_description,
            inline=False
        )
    elif rand < 0.02:
        # 💀 1% 全不選
        messages = answer_messages.get("1_percent_2", {}).get("message", ["什麼都不選！"])
        result_description = random.choice(messages)
        embed.add_field(
            name="💀【無情】什麼都不選！",
            value=result_description,
            inline=False
        )
    else:
        # 🎯 98% 正常選擇其中一項
        picked = random.choice(choices)
        comments = answer_messages.get("98_percent", {}).get("comments", [f"命運選中了：{picked}"])
        result_description = random.choice(comments).format(picked=picked)
        embed.add_field(
            name="🎯【結果出爐】",
            value=result_description,
            inline=False
        )

    # 🎀 隨機選擇分隔線裝飾
    divider = random.choice(dividers) if dividers else "----------"
    embed.description = f"{divider}\n讓命運的齒輪轉動吧！\n{divider}"

    # 📝 設定訊息底部註解
    embed.set_footer(text="由命運與智慧共同選出，絕不後悔！")

    # 📝 Log 紀錄：選項 & 結果
    if user:
        log_message(
            f"🎯 {user} 執行 /選擇 指令｜選項：{choices}｜結果：{result_description}",
            level="INFO",
            print_to_console=False
        )

    return embed

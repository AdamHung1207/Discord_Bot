# 📂 ======================= 基本套件導入 =======================

import random                                    # 🎲 隨機選擇
import asyncio                                   # ⏱️ 非同步倒數
import discord                                   # 🤖 Discord API
from services.tarot import repository            # 🧩 資料讀取層
from utils.log_utils import log_message          # 📝 日誌工具

# 🧩 ======================= 資料初始化 =======================

# 使用 .get() 來讀取資料，若無資料時使用空列表作為預設
big_cards = repository.load_big_cards().get("big_cards", [])
small_cards = repository.load_small_cards().get("small_cards", [])
all_tarot_cards = big_cards + small_cards  # 🎴 合併成完整塔羅牌列表
countdown_messages = repository.load_countdown_messages().get("countdown_messages", [])  # ⏳ 倒數訊息

# 🧩 ======================= 功能邏輯 =======================

async def draw_tarot_card(interaction: discord.Interaction):
    """
    🎴 抽取一張塔羅牌並產生嵌入式訊息
    :param interaction: Discord 互動物件
    """
    try:
        # ⚠️ 確保資料正常讀取
        if not all_tarot_cards:
            error_message = "❌ 無法讀取塔羅牌資料，請聯絡管理員！"
            log_message(error_message, level="ERROR", print_to_console=False)
            await interaction.response.send_message(error_message)
            return

        # 🌀 初始倒數提示
        initial_msg = random.choice(countdown_messages).format(count=3) if countdown_messages else "⏳ 倒數開始！"
        await interaction.response.send_message(initial_msg)
        countdown_msg = await interaction.original_response()

        # ⏱️ 倒數動畫：3, 2, 1
        for i in [2, 1]:
            await asyncio.sleep(1)
            next_msg = random.choice(countdown_messages).format(count=i) if countdown_messages else f"倒數 {i}..."
            await countdown_msg.edit(content=next_msg)

        await asyncio.sleep(1)  # 🕒 停一秒準備結果

        # 🃏 隨機抽一張塔羅牌
        card = random.choice(all_tarot_cards)

        # 🔄 隨機決定正位 / 逆位
        is_reversed = random.choice([True, False])
        position = "逆位" if is_reversed else "正位"

        # 📝 抓取對應資料
        adjectives = card.get("reversed_adjective", "無") if is_reversed else card.get("upright_adjective", "無")
        meaning = card.get("reversed", "無") if is_reversed else card.get("upright", "無")

        # 🖼️ 組裝嵌入式訊息 Embed
        embed = discord.Embed(
            title="🔮 你的塔羅牌結果：",
            color=discord.Color.purple()
        )
        embed.add_field(name="📖 牌名：", value=f"{card.get('tarot_zh_name', '未知')} ({card.get('tarot_en_name', '未知')})", inline=False)
        embed.add_field(name="🔄 正逆位：", value=position, inline=False)
        embed.add_field(name="📝 對應的形容詞：", value=adjectives, inline=False)
        embed.add_field(name="📌 牌義：", value=meaning, inline=False)
        embed.add_field(name="📖 完整解析：", value=card.get("meaning", "無解讀內容"), inline=False)
        embed.set_image(url=card.get("image", ""))

        # 📤 發送結果
        await countdown_msg.edit(content="✨ 你的塔羅牌結果如下：", embed=embed)

        # 📝 成功紀錄：記錄抽牌結果
        log_message(f"🎴 {interaction.user} 執行 /塔羅牌_抽單張｜抽到的塔羅牌：{card.get('tarot_zh_name', '未知')}｜解讀：{meaning}", level="INFO", print_to_console=False)

    except Exception as e:
        # 🛑 捕捉錯誤並記錄 log
        error_message = f"❌ 抽牌過程發生錯誤：{str(e)}"
        log_message(error_message, level="ERROR", print_to_console=False)
        await interaction.response.send_message(error_message)


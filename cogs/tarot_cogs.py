import json
import random
import discord
from discord.ext import commands
from discord import app_commands

# 讀取塔羅牌 JSON 檔案
# 這個函數用於讀取 tarot_big.json 和 tarot_small.json 兩個檔案，並返回一個包含所有卡片的列表
def load_tarot_cards(file_path, deck_name):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            tarot_cards = json.load(file)
        print(f"✅ 成功讀取 {len(tarot_cards)} 張{deck_name} - 來源: {file_path}")
        return tarot_cards
    except Exception as e:
        print(f"❌ 讀取 {file_path} 失敗：{e}")
        return []  # 讀取失敗時返回空列表，防止 bot 崩潰

# 定義 TarotCog 類別，作為 Discord Bot 的一部分
class TarotCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.big_tarot = load_tarot_cards("data/tarot_big.json", "大阿爾克那")  # 讀取大阿爾克那
        self.small_tarot = load_tarot_cards("data/tarot_small.json", "小阿爾克那")  # 讀取小阿爾克那
        self.all_tarot_cards = self.big_tarot + self.small_tarot  # 合併兩者，形成 78 張完整塔羅牌組

    @app_commands.command(name="塔羅牌_抽單張", description="🎴 從 78 張塔羅牌中隨機抽取一張！")
    async def tarot_single(self, interaction: discord.Interaction):
        """隨機抽取一張塔羅牌，並顯示詳細解釋"""
        if not self.all_tarot_cards:
            await interaction.response.send_message("❌ 無法讀取塔羅牌資料，請聯絡管理員！")
            return

        # 隨機選取一張塔羅牌
        card = random.choice(self.all_tarot_cards)
        is_reversed = random.choice([True, False])  # 隨機決定是否為逆位
        position = "逆位" if is_reversed else "正位"
        adjectives = card["reversed_adjective"] if is_reversed else card["upright_adjective"]
        meaning = card["reversed"] if is_reversed else card["upright"]

        # 生成美化後的輸出文字
        embed = discord.Embed(title="🔮 你的塔羅牌結果：", color=discord.Color.purple())
        embed.add_field(name="📖 牌名：", value=f"{card['tarot_zh_name']} ({card['tarot_en_name']})", inline=False)
        embed.add_field(name="🔄 正逆位：", value=position, inline=False)
        embed.add_field(name="📝 對應的形容詞：", value=adjectives, inline=False)
        embed.add_field(name="📌 牌義：", value=meaning, inline=False)
        embed.add_field(name="📖 完整解析：", value=card["meaning"], inline=False)
        embed.set_image(url=card["image"])

        # 發送回應
        await interaction.response.send_message(embed=embed)

# 註冊 Cog
async def setup(bot):
    await bot.add_cog(TarotCog(bot))

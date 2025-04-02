import discord                    # 引入 Discord API 套件，用於建立與 Discord 互動的 Bot
from discord import app_commands  # 用於建立斜線指令（Application Commands）
from discord.ext import commands  # 擴展命令模組，用於 Bot 功能模組化
import random                     # 隨機數模組，用於隨機選擇
import asyncio                    # 異步模組，用於協程執行
import re                         # 正則表達式模組，用於分割字串
import json                       # JSON 處理模組，用於讀取外部資料檔案
import os                         # 操作系統模組，用於處理檔案路徑

# 讀取 JSON 檔案的函數
def load_json(file_path, key, display_name):
    """
    從指定路徑讀取 JSON 檔案，並取得指定鍵的內容。
    :param file_path: JSON 檔案的路徑
    :param key: 要取出的主鍵名稱
    :param display_name: 顯示在終端的資料名稱
    :return: 對應鍵的內容，若不存在則回傳空字典
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)  # 解析 JSON 檔案
        items = data.get(key, {})  # 取得指定鍵的內容

        # 判斷結構並計算數量
        if isinstance(items, dict) and "message" in items:
            count = len(items["message"])  # 如果有 "message"，計算其數量
        elif isinstance(items, dict) and "comments" in items:
            count = len(items["comments"])  # 如果有 "comments"，計算其數量
        elif isinstance(items, list):
            count = len(items)  # 如果是列表，直接計算數量
        else:
            count = 1  # 如果既不是字典也不是列表，視為單一項目

        print(f"✅ 成功讀取 {count} 種{display_name} - 來源：{file_path}")
        return items
    except Exception as e:
        print(f"❌ 讀取 {file_path} 失敗：{e}")  # 錯誤提示
        return {}

class ChooseCogs(commands.Cog):
    def __init__(self, bot):
        """
        初始化 ChooseCogs 類別，載入必要的 JSON 資料檔案。
        :param bot: Discord Bot 實例
        """
        self.bot = bot

        # 載入選擇相關的回答資料
        self.answer_messages = load_json("data/choose_answer.json", "1_percent_1", "全都選的結果回應")
        self.answer_messages_2 = load_json("data/choose_answer.json", "1_percent_2", "全不選結果回應")
        self.answer_messages_98 = load_json("data/choose_answer.json", "98_percent", "多選一結果回應")
        self.thinking_messages = load_json("data/choose_countdown.json", "countdown_messages", "思考中的回應")
        self.dividers = load_json("data/choose_divider.json", "dividers", "分隔線的格式")

    @app_commands.command(name="選擇", description="🎯 從多個選項中隨機選一個！（支援空格或逗號分隔）")
    @app_commands.describe(options="輸入多個選項，例如：蘋果 香蕉 橘子")
    async def choose(self, interaction: discord.Interaction, options: str):
        """
        執行隨機選擇指令，提供命運的答案。
        :param interaction: Discord 互動對象
        :param options: 使用者提供的選項字串
        """
        # 使用正則表達式將用戶輸入的選項轉為清單
        choices = re.split(r"[,\s，]+", options.strip())
        choices = [c for c in choices if c]  # 過濾空選項

        # 如果選項少於兩個，回傳錯誤提示
        if len(choices) < 2:
            return await interaction.response.send_message("⚠️ 至少需要兩個選項喔！", ephemeral=True)

        await interaction.response.defer()  # 延遲回應，顯示指令執行中

        # 顯示初始的倒數提示
        thinking_msg = await interaction.followup.send(
            random.choice(self.thinking_messages).format(count=3)
        )

        # 動態倒數效果，每秒更新一次提示內容
        for i in range(3, 0, -1):
            countdown_text = random.choice(self.thinking_messages).format(count=i)
            await thinking_msg.edit(content=countdown_text)
            await asyncio.sleep(1)

        # 判斷隨機值以決定輸出結果
        rand = random.random()  # 產生隨機浮點數 (0 到 1)
        result_embed = discord.Embed(title="命運選擇")  # 嵌入消息標題
        result_embed.add_field(name="🎲【選項清單】", value="、".join(choices), inline=False)  # 顯示所有選項

        if rand < 0.01:
            # 1% 全選
            result_embed.add_field(
                name="🎉【驚喜】奇蹟發生！",
                value=f"命運選擇了全部：{'、'.join(choices)}！",
                inline=False
            )
        elif rand < 0.02:
            # 1% 全不選
            result_embed.add_field(
                name="💀【無情】什麼都不選！",
                value=random.choice(self.answer_messages_2["message"]),
                inline=False
            )
        else:
            # 98% 隨機選擇
            picked = random.choice(choices)  # 隨機選擇一個選項
            comment = random.choice(self.answer_messages_98["comments"]).format(picked=picked)
            result_embed.add_field(
                name="🎯【結果出爐】",
                value=comment,
                inline=False
            )

        # 隨機加入分隔線作為裝飾
        result_embed.description = (
            f"{random.choice(self.dividers)}\n"
            f"讓命運的齒輪轉動吧！\n"
            f"{random.choice(self.dividers)}"
        )

        # 設定嵌入消息的底部註解
        result_embed.set_footer(text="由命運與智慧共同選出，絕不後悔！")

        # 編輯最終結果消息
        await thinking_msg.edit(content=None, embed=result_embed)

# Cog 載入
async def setup(bot):
    await bot.add_cog(ChooseCogs(bot))

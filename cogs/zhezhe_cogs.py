import discord                    # 引入 Discord API 套件
from discord import app_commands  # 用於斜線指令（Application Commands）
from discord.ext import commands  # 引入擴展命令模組，用於管理 Bot 指令
import json                       # 用於讀取 JSON 檔案
import os                         # 操作系統模組，用於處理檔案路徑

class Zhezhe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.image_dict = self.load_image_dict()  # 初始化時從 JSON 檔案讀取圖片字典

        # 檢查是否成功載入圖片字典並顯示簡化訊息
        if self.image_dict:
            print(f"✅ 成功讀取 {len(self.image_dict)} 張哲哲梗圖 - 來源: data/zhezhe_images.json")
        else:
            print("❌ 無法載入 zhezhe_images.json，請確認檔案是否存在並正確設置。")

    # 從 JSON 檔案中載入圖片字典
    @staticmethod
    def load_image_dict():
        try:
            # 獲取檔案的相對路徑
            json_path = os.path.join('data', 'zhezhe_images.json')
            # 打開並讀取 JSON 檔案，返回字典
            with open(json_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            # 如果檔案不存在，回傳空字典並提示錯誤
            print("❌ 找不到 data/zhezhe_images.json 檔案！請確認檔案位置。")
            return {}
        except json.JSONDecodeError:
            # 如果檔案格式錯誤，回傳空字典並提示錯誤
            print("❌ data/zhezhe_images.json 格式錯誤！請檢查檔案內容。")
            return {}

    # 提供自動補全支援（最多 10 筆）
    async def autocomplete_keywords(self, interaction: discord.Interaction, current: str):
        return [
            app_commands.Choice(name=key, value=key)
            for key in self.image_dict.keys()
            if current in key  # 過濾符合當前輸入的關鍵字
        ][:10]                 # 限制最多 10 個結果

    # /哲哲 指令，傳送對應圖片
    @app_commands.command(name="哲哲", description="📸 發送對應的哲哲圖片")
    @app_commands.describe(文字="選擇要發送的哲哲圖片關鍵字")
    @app_commands.autocomplete(文字=autocomplete_keywords)
    async def zhezhe(self, interaction: discord.Interaction, 文字: str):
        if 文字 in self.image_dict:
            # 建立 Embed 美化輸出（可選）
            embed = discord.Embed(
                title=f"📸 哲哲語錄：{文字}",
                color=discord.Color.orange()                      # 設定 Embed 顏色
            )
            embed.set_image(url=self.image_dict[文字])            # 設定圖片 URL
            await interaction.response.send_message(embed=embed)  # 發送 Embed
        else:
            # 如果關鍵字不存在，回覆錯誤提示
            await interaction.response.send_message("❌ 找不到對應的圖片關鍵字", ephemeral=True)

# Cog 載入
async def setup(bot):
    await bot.add_cog(Zhezhe(bot))

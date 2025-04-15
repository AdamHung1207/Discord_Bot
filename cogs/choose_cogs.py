# 📂 ======================= 基本套件導入 =======================

import discord                    # 🤖 Discord API 套件
from discord import app_commands  # ⌨️ 斜線指令模組
from discord.ext import commands  # 🧠 擴展命令模組
import asyncio                    # ⏱️ 非同步執行
import random                     # 🎲 隨機數
import re                         # 🔎 正則運算分割

# 📦 專案自訂模組
from services.choose.service import get_choice_result           # 🧩 選擇邏輯處理
from utils.data_utils import load_yaml                          # 📚 YAML 載入工具
from utils.log_utils import (                                   # 📝 日誌工具整合
    log_command_usage, log, exception_logger
)

# 🧠 指令模組 Cog
class ChooseCogs(commands.Cog):
    def __init__(self, bot):
        """
        🎮 初始化 ChooseCogs 類別，載入倒數訊息資料
        :param bot: Discord Bot 實例
        """
        self.bot = bot

        # ✅ 加入 try-except 防呆處理
        try:
            raw_data = load_yaml("services/choose/data/countdown_messages.yaml") or {}

            self.thinking_messages = raw_data.get("countdown_messages", [])
            self.ultimate_messages = raw_data.get("1_percent_1", {}).get("message", [])
            self.dividers = raw_data.get("dividers", [])

            # ⚠️ fallback 預設值
            if not self.thinking_messages:
                self.thinking_messages = ["思考中... {count}"]
            if not self.ultimate_messages:
                self.ultimate_messages = ["✨ 結果：全部都選！"]
            if not self.dividers:
                self.dividers = ["✨━━━━━━━━━━━━━✨"]

        except Exception as e:
            # 🪤 錯誤記錄到 log
            exception_logger(e, context="載入 Choose 模組 YAML 時發生錯誤")

            # 🧩 fallback 預設值
            self.thinking_messages = ["思考中... {count}"]
            self.ultimate_messages = ["✨ 結果：全部都選！"]
            self.dividers = ["✨━━━━━━━━━━━━━✨"]

    # 🎯 指令：/選擇
    @app_commands.command(name="選擇", description="🎯 從多個選項中隨機選一個！（支援空格或逗號分隔）")
    @app_commands.describe(options="輸入多個選項，例如：蘋果 香蕉 橘子")
    async def choose(self, interaction: discord.Interaction, options: str):
        """
        🧩 執行隨機選擇指令，給出命運的答案
        :param interaction: Discord 互動對象
        :param options: 使用者提供的選項字串
        """
        try:
            # 🔍 分割選項字串為清單
            choices = re.split(r"[,\s，]+", options.strip())
            choices = [c for c in choices if c]  # 🧹 過濾空白

            # 🚧 防呆：少於兩個選項則回應錯誤
            if len(choices) < 2:
                await interaction.response.send_message(
                    "⚠️ 至少需要兩個選項喔！", ephemeral=True
                )
                log.warning(f"{interaction.user} 執行 /選擇 失敗：選項不足")
                return

            # 📌 記錄使用者觸發行為
            log_command_usage(interaction, "選擇", {
                "選項數量": len(choices),
                "內容": "、".join(choices[:5]) + ("..." if len(choices) > 5 else "")
            })

            # ⏳ 延遲回應
            await interaction.response.defer()

            # 🌀 發送倒數訊息
            thinking_msg = await interaction.followup.send(
                random.choice(self.thinking_messages).format(count=3)
            )

            for i in range(3, 0, -1):
                countdown_text = random.choice(self.thinking_messages).format(count=i)
                await thinking_msg.edit(content=countdown_text)
                await asyncio.sleep(1)

            # ✅ 美化選項顯示格式
            if len(choices) <= 5:
                choices_text = "、".join(choices)
            else:
                choices_text = "\n".join(f"🔸 {c}" for c in choices)

            # 🧩 呼叫 service 層產出結果 Embed
            embed = get_choice_result(choices, user=interaction.user)

            # 📝 加入選項清單
            embed.set_field_at(0, name="🎲【選項清單】", value=choices_text, inline=False)

            # 📤 發送結果
            await thinking_msg.edit(content=None, embed=embed)

            # ✅ 成功紀錄
            log.success(f"{interaction.user} 完成 /選擇，結果：{embed.title}")

        except Exception as e:
            # ❌ 回覆錯誤訊息
            await interaction.followup.send(
                f"❌ 執行指令時發生錯誤：{str(e)}", ephemeral=True
            )
            exception_logger(e, context="選擇指令")

# 🔧 Cog 註冊
async def setup(bot):
    await bot.add_cog(ChooseCogs(bot))

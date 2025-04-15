# 📂 ======================= 指令入口層：當沖計算器 =======================

import discord  # 🤖 Discord 框架
from discord.ext import commands
from discord import app_commands  # 🧩 Discord 指令模組
from services.daytrade import controller  # 📥 調用控制層
from utils.log_utils import log  # 📝 日誌管理

# 🧩 ======================= 建立指令模組 =======================
class DayTradeCog(commands.Cog):
    """
    🤖 當沖計算器指令模組
    - 包含手續費查詢與修改
    - 當沖買 / 賣試算功能
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ======================= /手續費查詢 =======================
    @app_commands.command(name="手續費查詢", description="📖 查詢目前手續費折數")
    async def fee_discount_query(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        log.info(f"[指令觸發] /手續費查詢 | user: {user_id}")

        message = controller.handle_fee_discount_query(user_id)
        await interaction.response.send_message(message)

    # ======================= /手續費修改 =======================
    @app_commands.command(name="手續費修改", description="📝 修改手續費折數（例如：3.8 表示 3.8 折）")
    async def fee_discount_set(self, interaction: discord.Interaction, fee_discount: float):
        user_id = interaction.user.id
        log.info(f"[指令觸發] /手續費修改 | user: {user_id} | fee_discount: {fee_discount}")

        message = controller.handle_fee_discount_update(user_id, fee_discount)
        await interaction.response.send_message(message)

    # ======================= /當沖_買 =======================
    @app_commands.command(name="當沖_買", description="📈 當沖買進試算（價格、數量、區間）")
    @app_commands.describe(
        price="買進價格（必填）",
        quantity="數量（張數，必填）",
        range_count="價差區間（選填，預設 5）"
    )
    async def daytrade_buy(self, interaction: discord.Interaction, price: float, quantity: int, range_count: int = 5):
        user_id = interaction.user.id
        log.info(f"[指令觸發] /當沖_買 | user: {user_id} | price: {price} | quantity: {quantity} | range: {range_count}")

        # ✅ 基本參數檢查
        if price <= 0 or quantity <= 0 or range_count <= 0:
            await interaction.response.send_message("🚨 請輸入有效的數值（價格、數量、區間均需大於 0）", ephemeral=True)
            return

        # ✅ 呼叫邏輯層計算結果
        embed = controller.get_daytrade_buy_embed(user_id, price, quantity, range_count)

        # ✅ 輸出 Embed 結果
        await interaction.response.send_message(embed=embed)

    # ======================= /當沖_賣 =======================
    @app_commands.command(name="當沖_賣", description="📉 當沖賣出試算（價格、數量、區間）")
    @app_commands.describe(
        price="賣出價格（必填）",
        quantity="數量（張數，必填）",
        range_count="價差區間（選填，預設 5）"
    )
    async def daytrade_sell(self, interaction: discord.Interaction, price: float, quantity: int, range_count: int = 5):
        user_id = interaction.user.id
        log.info(f"[指令觸發] /當沖_賣 | user: {user_id} | price: {price} | quantity: {quantity} | range: {range_count}")

        # ✅ 基本參數檢查
        if price <= 0 or quantity <= 0 or range_count <= 0:
            await interaction.response.send_message("🚨 請輸入有效的數值（價格、數量、區間均需大於 0）", ephemeral=True)
            return

        # ✅ 呼叫邏輯層計算結果
        embed = controller.get_daytrade_sell_embed(user_id, price, quantity, range_count)

        # ✅ 輸出 Embed 結果
        await interaction.response.send_message(embed=embed)

# 🧩 ======================= 設定指令模組 =======================
async def setup(bot: commands.Bot):
    await bot.add_cog(DayTradeCog(bot))

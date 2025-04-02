import discord                    # 引入 Discord API 套件，用於建立與 Discord 互動的 Bot
from discord import app_commands  # 用於建立斜線指令（Application Commands）
from discord.ext import commands  # 引入擴展命令模組，用於 Bot 功能模組化
import random                     # 隨機數模組，用於隨機產生回應

class ClearCogs(commands.Cog):
    def __init__(self, bot):
        """
        初始化 ClearCogs 類別。
        :param bot: Discord Bot 實例
        """
        self.bot = bot

    # 斜線指令 /清除，限有管理訊息權限的人使用
    @app_commands.command(name="清除", description="🗑️ 清除指定數量的訊息（可選擇只刪除機器人或特定用戶的訊息）")
    @app_commands.describe(amount="要刪除的訊息數量（最多 100）", user="指定要刪除訊息的用戶（可選）")
    @app_commands.checks.has_permissions(manage_messages=True)  # 檢查是否擁有管理訊息權限
    async def clear_messages(self, interaction: discord.Interaction, amount: int, user: discord.Member = None):
        """
        清除訊息指令，僅限擁有管理訊息權限的使用者。
        :param interaction: Discord 互動對象
        :param amount: 要刪除的訊息數量
        :param user: 指定要刪除訊息的用戶（可選）
        """
        # 檢查刪除訊息的數量是否合理
        if amount <= 0:
            return await interaction.response.send_message("⚠️ 請輸入大於 0 的數字！", ephemeral=True)  # 提示錯誤並隱藏消息
        if amount > 100:
            return await interaction.response.send_message("⚠️ 一次最多只能刪除 100 則訊息！", ephemeral=True)  # 提示錯誤並隱藏消息
        
        # 延遲回應（使執行看起來更流暢）
        await interaction.response.defer(ephemeral=True)

        # 定義檢查訊息的條件
        def check(msg):
            if msg.pinned:
                return False  # 排除置頂訊息，這些訊息不會被刪除
            if user:
                return msg.author == user  # 若指定了用戶，只刪除該用戶的訊息
            return True  # 預設刪除所有普通訊息

        try:
            # 執行刪除訊息的操作
            deleted = await interaction.channel.purge(limit=amount, check=check)
            responses = [
                f"🗑️ 清理完畢！成功刪除 **{len(deleted)}** 則訊息！", 
                f"🔥 訊息清除完成！已移除 **{len(deleted)}** 則對話！", 
                f"⚡ 清掃作業結束，{len(deleted)} 則訊息已灰飛煙滅！", 
                f"💨 一陣風過去……{len(deleted)} 則訊息消失無蹤！", 
                f"🧹 清潔機器人上線，{len(deleted)} 則訊息已經處理！"
            ]
            # 隨機回覆刪除成功的訊息
            await interaction.followup.send(random.choice(responses), ephemeral=True)
        except discord.Forbidden:
            # 權限不足時的錯誤處理
            await interaction.followup.send("❌ 我沒有權限刪除訊息，請確認機器人權限！", ephemeral=True)
        except Exception as e:
            # 其他錯誤處理
            await interaction.followup.send(f"❌ 清除失敗：{str(e)}", ephemeral=True)

    # 針對權限錯誤的專屬處理
    @clear_messages.error
    async def clear_messages_error(self, interaction: discord.Interaction, error):
        """
        處理權限錯誤或其他未知錯誤。
        :param interaction: Discord 互動對象
        :param error: 發生的錯誤
        """
        if isinstance(error, app_commands.MissingPermissions):
            # 使用者缺少管理訊息權限時的提示
            await interaction.response.send_message("❌ 你沒有權限使用此指令！需要 **管理訊息** 權限。", ephemeral=True)
        elif isinstance(error, app_commands.CheckFailure):
            # 使用者檢查失敗（權限不足）
            await interaction.response.send_message("❌ 你沒有權限執行此操作。", ephemeral=True)
        else:
            # 發生未知錯誤的提示
            await interaction.response.send_message(f"❌ 發生未知錯誤：{str(error)}", ephemeral=True)

# 必須的 setup，讓主程式可以加載這個 COG
async def setup(bot):
    """
    將 ClearCogs 模組加載至 Bot。
    :param bot: Discord Bot 實例
    """
    await bot.add_cog(ClearCogs(bot))

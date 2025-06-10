import sqlite3

import discord
from discord.ext import commands
import db.db_utils as db_utils
from db import DB_PATH

TARGET_CHANNEL_ID = 1373919737892962398  # 채팅방

class Default(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="내정보")
    async def inquiry(self, ctx):
        if ctx.channel.id != TARGET_CHANNEL_ID:
            return

        user_id = ctx.author.id

        with sqlite3.connect(DB_PATH) as conn:
            data = db_utils.get_user_info(user_id, conn)

        if data is None:
            await ctx.send("정보를 불러오는 중 오류가 발생했습니다.")
            return

        embed = discord.Embed(
            title=f'{data["boj_id"]}님의 유저 정보',
            description="",
            url=f'https://solved.ac/profile/{data["boj_id"]}',
            color=discord.Color.green()
        )

        embed.add_field(name="현재 레이팅", value=data['rating'], inline=False)
        embed.add_field(name="현재 티어", value=data['tier'], inline=False)
        embed.add_field(name="푼 문제 수", value=data['solved_count'], inline=False)
        embed.add_field(name="일 주 목표 개수", value=data['number_per_week'], inline=False)
        # embed.add_field(name="지난주 레이팅 대비" value=data[''] ~)

        embed.set_footer(text=f"information by solved.ac\n마지막 수정 날짜:{data['updated_at']}")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Default(bot))

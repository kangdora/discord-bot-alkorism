import sqlite3

import discord
from discord.ext import commands

from api.solvedac_api import solvedac_api
import util.verify_vaild as verify
import db.db_utils as db_utils

TARGET_MESSAGE_ID = 1374308065830113322 # 규칙 메시지 ID
TARGET_CHANNEL_ID = 1374207235705671813 # id 채널
TARGET_EMOJI = "✅"
ROLE_NAME_TEMP = "임시"
ROLE_NAME_MEMBER = "회원"

class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id != TARGET_MESSAGE_ID:
            return

        if str(payload.emoji) != TARGET_EMOJI:
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if member is None:
            return

        role = discord.utils.get(guild.roles, name=ROLE_NAME_TEMP)
        if role is None:
            return  # 역할이 없으면 무시

        # 역할 부여
        if role not in member.roles:
            await member.add_roles(role)
            print(f"{member.name}에게 인증 역할 부여됨.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.channel.id != TARGET_CHANNEL_ID:
            return

        # 여기까지 왔으면, 감지 대상 채널에서 유저가 보낸 메시지
        print(f"[감지됨] {message.author}가 메시지 보냄: {message.content}")

        if not verify.is_valid_id(message.content):
            return

        try:
            data = solvedac_api(message.content)
        except Exception as e:
            await message.channel.send("solved.ac 정보를 불러오는 중 오류가 발생했습니다.")
            print(f"[오류] solvedac_api 실패: {e}")
            return

        if not verify.is_valid_response(data):
            await message.channel.send("잘못된 BOJ ID입니다. 다시 확인해 주세요.")
            return

        if verify.is_valid_response(data):
            parsed_data = verify.parse_user_info(data)

            with sqlite3.connect("data.db") as conn:
                db_utils.save_new_user(
                    message.author.id,
                    parsed_data["boj_id"],
                    parsed_data["rating"],
                    parsed_data["tier"],
                    parsed_data["solved_count"],
                    conn
                )

            guild = message.guild
            member = message.author

            role = discord.utils.get(guild.roles, name=ROLE_NAME_MEMBER)
            if role is None:
                return  # 역할이 없으면 무시

            # 역할 부여
            if role not in member.roles:
                await member.add_roles(role)
                await member.remove_roles(discord.utils.get(guild.roles, name=ROLE_NAME_TEMP))
                print(f"{member.name}에게 인증 역할 부여됨.")


def setup(bot):
    bot.add_cog(Verify(bot))

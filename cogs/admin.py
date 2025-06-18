import os
import sqlite3

from discord.ext import commands

from api.solvedac_api import solvedac_api
import util.verify_vaild as verify
import db.db_utils as db_utils
from db import DB_PATH


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="리로드")
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx, extension: str):
        try:
            self.bot.reload_extension(f'cogs.{extension}')
            await ctx.send(f'✅ `{extension}` reloaded.')
        except Exception as e:
            await ctx.send(f'❌ Reload failed: {e}')

    @commands.command(name="로드", aliases=["loadall"])
    @commands.has_permissions(administrator=True)
    async def load_all(self, ctx):
        loaded = []
        failed = []
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and filename != '__init__.py':
                extension = filename[:-3]
                try:
                    self.bot.load_extension(f'cogs.{extension}')
                    loaded.append(extension)
                except Exception as e:
                    failed.append((extension, str(e)))

        msg = f'✅ Loaded: {", ".join(loaded) if loaded else "None"}'
        if failed:
            msg += f'\n❌ Failed:\n' + '\n'.join([f'{ext}: {err}' for ext, err in failed])
        await ctx.send(msg)

    @commands.command(name="언로드")
    @commands.has_permissions(administrator=True)
    async def unload(self, ctx, extension: str):
        self.bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f'✅ `{extension}` unloaded.')

    @commands.command(name="유저삭제")
    @commands.has_permissions(administrator=True)
    async def delete_user(self, ctx, user):

        with sqlite3.connect(DB_PATH) as conn:
            try:
                db_utils.delete_user(user, conn)
            except Exception as e:
                await ctx.send("정보를 삭제하는 중 오류가 발생했습니다.")
                print(f"[오류] 유저삭제 실패: {e}")
                return

        await ctx.send(f"[성공] {user}의 정보가 성공적으로 지워졌습니다.")

    @commands.command(name="유저갱신전체")
    @commands.has_permissions(administrator=True)
    async def refresh_all_users(self, ctx):
        """DB에 등록된 모든 유저 정보를 solved.ac에서 갱신"""
        with sqlite3.connect(DB_PATH) as conn:
            boj_ids = db_utils.get_all_boj_ids(conn)
            updated = 0
            for boj_id in boj_ids:
                try:
                    data = solvedac_api(boj_id)
                except Exception as e:
                    await ctx.send(f"❌ {boj_id} 업데이트 실패: {e}")
                    continue

                if not verify.is_valid_response(data):
                    await ctx.send(f"❌ {boj_id} 데이터 오류")
                    continue

                parsed = verify.parse_user_info(data)
                db_utils.upsert_user_items(
                    parsed["boj_id"],
                    parsed["rating"],
                    parsed["tier"],
                    parsed["solved_count"],
                    conn,
                )
                updated += 1

        await ctx.send(f"✅ {updated}명 유저 정보 갱신 완료")


async def setup(bot):
    await bot.add_cog(Admin(bot))

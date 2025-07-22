import os
import sqlite3

from discord.ext import commands
import db


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="리로드")
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx, extension: str):
        try:
            await self.bot.reload_extension(f'cogs.{extension}')
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
                    await self.bot.load_extension(f'cogs.{extension}')
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
        await self.bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f'✅ `{extension}` unloaded.')

    @commands.command(name="유저삭제")
    @commands.has_permissions(administrator=True)
    async def delete_user(self, ctx, user):

        with sqlite3.connect(r"C:\Users\ioprt\Desktop\개발\discord-bot-alkorism\db\data.db") as conn:
            try:
                db.db_utils.delete_user(user, conn)
            except Exception as e:
                await ctx.send("정보를 삭제하는 중 오류가 발생했습니다.")
                print(f"[오류] 유저삭제 실패: {e}")
                return

        await ctx.send(f"[성공] {user}의 정보가 성공적으로 지워졌습니다.")

    @commands.command(name="삭제")
    @commands.has_permissions(administrator=True)
    async def delete_message(self, ctx, count: int):
        deleted = await ctx.channel.purge(limit=count + 1)  # 명령어 메시지까지 포함
        await ctx.send(f"{len(deleted) - 1}개의 메시지를 삭제했습니다.", delete_after=3)


async def setup(bot):
    await bot.add_cog(Admin(bot))

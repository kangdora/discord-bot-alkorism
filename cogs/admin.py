import os
from discord.ext import commands


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


async def setup(bot):
    await bot.add_cog(Admin(bot))

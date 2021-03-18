from discord.ext.commands import Cog


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        await self.bot.stdout.send('Cog braba funcionando')
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('fun')


def setup(bot):
    bot.add_cog(Fun(bot))
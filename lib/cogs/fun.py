from typing import Optional
from random import choice, randint

from discord.errors import HTTPException
from discord import Member, message
from discord.ext.commands import Cog, command
from discord.ext.commands.errors import BadArgument



class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="olá", aliases=["oi"], hidden=True)
    async def falar_oi(self, ctx):
        await ctx.send(f"Opa bom dia, {ctx.author.mention}.")

    @command(name="dado", aliases=["dice", "roll", "dadin"], hidden=True)
    async def rolar_dado(self, ctx, dice_string: str):
        dice, value= (int(term) for term in dice_string.split("d"))
        rolls = [randint(1, value) for i in range(dice)]

        await ctx.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")

    @rolar_dado.error
    async def rolar_dado_error(self, ctx, exc):
        if isinstance(exc.original, HTTPException):
            await ctx.send("A mensagem ultrapassou o limite de 2000 caracteres. Por favor, tente um número menor.")


    @command(name="slap", aliases=["hit"], hidden=True)
    async def slap(self, ctx, member: Member, *, reason: Optional[str] = "por nenhuma razão"):
        await ctx.send(f"{ctx.author.display_name} estapeou {member.mention} {reason.strip()}.")

    @slap.error
    async def slap_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send("Eu não consegui encontrar esse membro.")

    @command(name="fala", aliases=["say"], hidden=True)
    async def say_something(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    @Cog.listener()
    async def on_ready(self):
        # await self.bot.stdout.send('Cog braba funcionando')
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('fun')


def setup(bot):
    bot.add_cog(Fun(bot))
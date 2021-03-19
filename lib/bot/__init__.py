from sqlite3.dbapi2 import Timestamp
from apscheduler.triggers.cron import CronTrigger
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Intents, Embed
from datetime import datetime
from asyncio import sleep
from glob import glob
from discord.ext.commands.context import Context

from discord.ext.commands.core import command
from discord.ext.commands.errors import BadArgument, MissingRequiredArgument
from ..db import db


PREFIX = "+"
OWNER_IDS = [208388659634765825]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORED_EXCEPTIONS = (CommandNotFound, BadArgument, MissingRequiredArgument)


class Ready(object):
	def __init__(self):
		for cog in COGS:
			setattr(self, cog, False)

	def ready_up(self, cog):
		setattr(self, cog, True)
		print(f' {cog} cog carregado.')

	def all_ready(self):
		return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.ready = False
		self.cogs_ready = Ready()
		self.guild = None
		self.scheduler = AsyncIOScheduler()

		db.autosave(self.scheduler)
		super().__init__(	
			command_prefix=PREFIX,
			owner_ids=OWNER_IDS,
			intents=Intents.all()
		)
	
	def setup(self):
		for cog in COGS:
			self.load_extension(f'lib.cogs.{cog}')
			print(f' {cog} cog carregado')
		print('Setup completo\n')

	def run(self, version):
		self.VERSION = version

		print('Setup carregando...')
		self.setup()

		with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
			self.TOKEN = tf.read()

		print('Bot carregando...')
		super().run(self.TOKEN, reconnect=True)

	'''async def process_commands(self, message):
		return super().process_commands(message)'''

	async def process_commands(self, message):
		ctx = await self.get_context(message, cls=Context)

		if ctx.command is not None and ctx.guild is not None:
			if self.ready:
				await self.invoke(ctx)

			else:
				await ctx.send("Não estou pronto para receber comandos por agora. Por favor, espere um pouco.")

	async def rules_reminder(self):
		channel = self.get_channel(821837723655471125)
		await channel.send("Lembrar de mexer aqui depois kappa kappa. rules_reminder btw")

	async def on_connect(self):
		print(' bot conectado')
	
	async def on_disconnect(self):
		print(' bot disconnected')

	async def on_error(self, err, *args, **kwargs):
		if err == "on_command_error":
			await args[0].send("Algo deu errado.")

		else:
			channel = self.get_channel(821837723655471125)
			await self.stdout.send("Oops, algo deu errado com o código.")

	async def on_command_error(self, cts, exc):
		if any([isinstance(exc, error) for error in IGNORED_EXCEPTIONS]):
			pass
		elif isinstance(exc, MissingRequiredArgument):
			await self.stdout.send("Um ou mais argumentos necessários faltando.")
		elif isinstance(exc.original, HTTPException):
			await self.stdout.send("Coloco algo aqui depois e.e'")
		elif isinstance(exc.original, Forbidden):
			await self.stfout.send("Não tenho permissão para fazer isso.")
		elif hasattr(exc, "original"):
			raise exc.original
		else:
			raise exc

	async def on_ready(self):
		if not self.ready:
			self.guild = self.get_guild(821023837437165571)
			self.stdout = self.get_channel(821837723655471125)
			self.scheduler.start()
			self.scheduler.add_job(self.rules_reminder, CronTrigger(hour=12, minute=0, second=0))

			"""embed = Embed(title="Online agora!", description="Sim, fiquei online mesmo.", colour=0xff6b99,
						  Timestamp=datetime.utcnow())
			fields = [("Aham", "Espero que esteja tudo bem contigo.", True),
					  ("Outro", "Sim, isto é outro field que está aqui apenas para ocupar um espaço.", True),
					  ("Sim", "Esse daqui também e.e'", True),
					  ("Te amo", "tipo mesmo mesmo", False)]
			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)
			embed.set_footer(text="muito muito muito c:")
			embed.set_author(name="Buuhzerah", icon_url=self.guild.icon_url)
			await self.stdout.send(embed=embed)"""

			while not self.cogs_ready.all_ready():
				await sleep(.5)

			# await self.stdout.send("Online agora!")
			self.ready = True
			print('\nBot está pronto! c:')
		else:
			print('bot reconnected')
	async def on_message(self, message):
		if not message.author.bot:
			await self.process_commands(message)


bot = Bot()

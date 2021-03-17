from sqlite3.dbapi2 import Timestamp
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Intents, Embed
from datetime import datetime


PREFIX = "+"
OWNER_IDS = [208388659634765825]


class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.ready = False
		self.guild = None
		self.scheduler = AsyncIOScheduler()

		super().__init__(	
			command_prefix=PREFIX,
			owner_ids=OWNER_IDS,
			intents=Intents.all()
		)
		
	def run(self, version):
		self.VERSION = version

		with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
			self.TOKEN = tf.read()

		print('bot running...')
		super().run(self.TOKEN, reconnect=True)

	async def on_connect(self):
		print('bot connected')

	async def on_disconnect(self):
		print('bot disconnected')

	async def on_error(self, err, *args, **kwargs):
		if err == "on_command_error":
			await args[0].send("Algo deu errado.")

		else:
			channel = self.get_channel(821837723655471125)
			await channel.send("Oops, algo deu errado.")

	async def on_command_error(self, cts, exc):
		if isinstance(exc, CommandNotFound):
			pass
		elif hasattr(exc, "original"):
			raise exc.original
		else:
			raise exc

	async def on_ready(self):
		if not self.ready:
			self.ready = True
			self.guild = self.get_guild(821023837437165571)
			print('Bot ready')

			channel = self.get_channel(821044674701557811)
			#await channel.send("Online agora!")

			embed = Embed(title="Online agora!", description="Sim, é isso mesmo.", colour=0xff6b99,
						  Timestamp=datetime.utcnow())
			fields = [("Aham", "Espero que esteja tudo bem contigo.", True),
					  ("Outro", "Sim, isto é outro field que está aqui apenas para ocupar um espaço.", True),
					  ("Sim", "Esse daqui também e.e'", True),
					  ("Te amo", "tipo mesmo mesmo", False)]
			for name, value, inline in fields:
				embed.add_field(name=nname, value=value, inline=inline)
			embed.set_footer(text="muito muito muito c:")
			embed.set_author(name="Buuhzerah", icon_url=self.guild.icon_url)
			await channel.send(embed=embed)
		else:
			print('bot reconnected')
	async def on_message(self, message):
		pass


bot = Bot()

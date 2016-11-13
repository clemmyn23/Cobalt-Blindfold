from .libbopae.main import *
from .libbopae.utils.chat_formatting import *


BOPAE_DATA_DIR = 'data/bopae/'

class bnsbopae:

	def __init__(self, bot, message):
		self.bot = bot
		self.message = message
        self.Bopae = Bopae(BOPAE_DATA_DIR)

    async def bopae(self):
        result = self.Bopae.search(self.message.content)
        for page in pagify(result, ['\n']):
            await self.bot.send_message(self.message.channel, page)

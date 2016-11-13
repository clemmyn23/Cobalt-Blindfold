import os, re, asyncio
import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from __main__ import send_cmd_help


from libbopae.main import *
from libbopae.utils.chat_formatting import *
# from .utils.chat_formatting import *

"""
##########################################
    THIS FILE IS FOR RED-DISCORDBOT
##########################################
"""


BOPAE_DATA_DIR = 'data/bopae/'

def setup(bot):
    bot.add_cog(BopaeRED(bot))


class BopaeRED:
    """BNS soul shield utils"""

    def __init__(self, bot):
        self.bot = bot
        self.Bopae = Bopae(BOPAE_DATA_DIR)


    @commands.group(name="bopae", pass_context=True)
    async def bopae(self, ctx):
        """BNS soul-shield search.
        FORMAT:
            !bopae ([set name] [slot num/all]...)...
        EXAMPLES:
            !bopae tomb 1
            !bopae yeti 2 4 ebon all asura 1 3 5
        """

        if ctx.invoked_subcommand is None:
            if len(ctx.message.content.split()) > 1:
                search_result = self.Bopae.search(ctx.message.content)

                for page in pagify(search_result, ['\n']):
                    await self.bot.say(box(page))
            else:
                await send_cmd_help(ctx)


    @bopae.command(name="list")
    async def list(self):
        """Show SS sets in the database"""

        await self.bot.say(self.Bopae.list())

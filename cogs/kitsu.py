import discord
import re
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from cogs.utils import checks
from __main__ import send_cmd_help
try:
    from bs4 import BeautifulSoup
    isSoupAvail = True
except:
    isSoupAvail = False
import aiohttp
import asyncio
from urllib.parse import quote



class Kitsu:
    """Kitsu\'s BNS and bot dev utilities"""

    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    @commands.group(pass_context=True, hidden=True)
    async def kitsu(self, ctx):
        """Kitsu\'s BNS and bot dev utilities"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            return

    @kitsu.command(name="encode", pass_context=True)
    @checks.is_owner()
    async def kitsu_debug_encode(self, ctx, *text):
        if text == ():
            await send_cmd_help(ctx)
        else:
            await self.bot.say(text)
            await self.bot.say(quote(" ".join(map(str, text)), safe=''))
        return

    @kitsu.command(name="user")
        async def kitsu_user(self, *text):
        """BNS character details docstring"""
        await self.bot.say("TODO: char details parser. [{}]".format(text))
        return

    @kitsu.command(name="alts", pass_context=True)
    async def kitsu_alts(self, ctx, *text):
        """BNS account alts docstring"""
        await self.bot.say("TODO: account alts parser. [{}]".format(text))

        if text ==():
            await send_cmd_help(ctx)
            return

        name = quote(" ".join(map(str, text)), safe='')
        url = "http://na-bns.ncsoft.com/ingame/bs/character/search/info?c=" + name
        # url = "http://na-bns.ncsoft.com/ingame/bs/character/profile?c=" + name

        async with aiohttp.get(url) as resp:
            if resp.status != 200:
                multiline = "{}\nBNS server potato (http resp status {})".format(url, resp.status)
                await self.bot.say(multiline)
                return

            soup = BeautifulSoup(await resp.text(), 'html.parser')

        try:
            wall = soup.body.find(id="container").find(id="contents")
            numresults = wall.find(id="header")
            await self.bot.say(str(numresults))

            wall = wall.find(class_="searchList").find(class_="user")
            # for


            # wall = soup.body.find(id="container").find(id="contents").find(class_="characterInfo")
            # wall = wall.find(class_="itemArea").find(class_="wrapGem").find(class_="gemIcon").find("map")
            # for piece in wall.find_all("area"):
            #     # TODO
            #     pass
        except:
            pass

        return

    @kitsu.command(name = "bopae")
    async def kitsu_bopae(self, *text):
        if text == ():
            return self.kitsu_help()

        name = quote(" ".join(map(str, text)), safe='')
        url = "http://na-bns.ncsoft.com/ingame/bs/character/profile?c=" + name

        async with aiohttp.get(url) as resp:
            if resp.status != 200:
                multiline = "{}\n".format(url)
                multiline += "BNS server potato (http resp status {})".format(resp.status)
                # await self.bot.say(multiline)
                return multiline
            soup = BeautifulSoup(await resp.text(), 'html.parser')

        try:
            wall = soup.body.find(id="container").find(id="contents").find(class_="characterInfo")
            wall = wall.find(class_="itemArea").find(class_="wrapGem").find(class_="gemIcon").find("map")
            multiline = "Requested name [{}]\n".format(name)
            multiline += "{}\n".format(url)
            slot = 1
            for piece in wall.find_all("area"):
                try:
                    multiline += "slot #{}: {}, \titem-ID {}\n".format(slot, piece["alt"], piece["item-data"])
                except:
                    multiline += "slot #{}: empty\n".format(slot)
                slot += 1
            return multiline
        except:
            return "Unable to find character [{}]".format(name)


    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    # = = = = = = = = = = = = = COMMAND HANDLERS  = = = = = = = = = = = = = = = = = = = =





    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    # = = = = = = = = = = = = = UTILITIES = = = = = = = = = = = = = = = = = = = = = = = =
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


def setup(bot):
    if isSoupAvail:
        bot.add_cog(Kitsu(bot))
    else:
        raise RuntimeError("You need to run `pip3 install beautifulsoup4`")

import discord
import re
from discord.ext import commands
from cogs.utils.dataIO import dataIO
try:
    from bs4 import BeautifulSoup
    isSoupAvail = True
except:
    isSoupAvail = False
import aiohttp


class Bopae:
    """BNS soul shield utils"""

    def __init__(self, bot):
        self.bot = bot
        self.bopaeData = dataIO.load_json("data/bopae/bopae.json")


    def bopae_search(self, query):
        query = query.lower()

        if query in self.bopaeData:
            return query

        if len(query) < 3:
            # print("DEBUG: search request too short")
            return ""

        for i in self.bopaeData:
            # print("DEBUG: matching query [{}] in tags {}".format(query, self.bopaeData[i]["tags"]))
            for tag in self.bopaeData[i]["tags"]:
                # if tag == query:
                #     return i
                if re.search(query, tag) != None:
                    return i

        for i in self.bopaeData:
            # print("DEBUG: query: [{}], searching: [{}]".format(query, self.bopaeData[i]["setName"].lower()))
            if re.search(query, self.bopaeData[i]["setName"].lower()) != None:
                return i

        return ""


    @commands.command()
    async def bopae(self, *text):
        ("BNS soul shield utils\n"
        "Usage: !bopae list\n"
        "       !bopae [name]\n"
        "       !bopae [name] [1-8]")


        if text == () or len(text) > 2:
            await self.bot.say("```"
                               "Usage: !bopae list\n"
                               "       !bopae [name]\n"
                               "       !bopae [name] [1-8]```")

        if text[0] == "list":
            multiline = "Available SS sets: " + ", ".join(map(str, self.bopaeData))
            await self.bot.say(multiline)

        elif text[0] == "search":
            if len(text) != 2:
                await self.bot.say("Usage: !bopae search [query]")
                return
            await self.bot.say("DEBUG: bopae search result: " + self.bopae_search(text[1]))

        elif text[0] == "user":
            await self.bot.say("feature unimplemented")

            name = " ".join(map(str, text[1::]))
            await self.bot.say("requested name [{}]".format(name))

            url = "http://na-bns.ncsoft.com/ingame/bs/character/profile?c="+name+"&s=101"
            await self.bot.say("url: "+url)

            async with aiohttp.get(url) as response:
                wall = response.status
                await self.bot.say("http response: "+str(wall))
                soupObject = BeautifulSoup(await response.text(), 'html.parser')

            # try:
            # data = soupObject.find_all(class_="gemIcon")
            # print(str(soupObject))
            # await self.bot.say("test here")
            # await self.bot.say(stuffing)
            # except:
            #     await self.bot.say("parsing error")
            #



            #Your code will go here
            # url = "https://steamdb.info/app/570/graphs/" #build the web adress
            # async with aiohttp.get(url) as response:
            #     soupObject = BeautifulSoup(await response.text(), "html.parser")
            # try:
            #     online = soupObject.find(class_='home-stats').find('li').find('strong').get_text()
            #     await self.bot.say(online + ' players are playing this game at the moment')
            # except:
            #     await self.bot.say("Couldn't load amount of players. No one is playing this game anymore or there's an error.")



        elif len(text) == 1:
            """bopae set stats"""

            if len(text[0]) < 3:
                await self.bot.say("Search request too short (must be at least 3 characters long)")
                return

            query = self.bopae_search(text[0])
            if query == "":
                await self.bot.say("Unable to find requested set [{}]".format(text[0]))
                return

            reqBopae = self.bopaeData[query]
            multiline = ("```"
                "REQUESTED SOUL SHIELD SET [{}]\n"
                "set name: {}\n"
                "set notes: {}\n"
                ).format(query, reqBopae["setName"], reqBopae["setNotes"])

            for i in reqBopae["setBonus"]:
                multiline += "set bonus {}: {}\n".format(i, reqBopae["setBonus"][i])

            multiline += "```"
            await self.bot.say(multiline)

        elif len(text) == 2:
            """specific bopae stat"""

            if len(text[0]) < 3:
                await self.bot.say("Search request too short (must be at least 3 characters long)")
                return

            query = self.bopae_search(text[0])
            if query == "":
                await self.bot.say("Unable to find requested set [{}]".format(text[0]))
                return

            try:
                reqBopae = self.bopaeData[query]["slot"+text[1]]
            except:
                await self.bot.say("Invalid bopae slot requested [{}]".format(text[1]))
                return

            multiline = ("```"
                "REQUESTED SOUL SHIELD PIECE [{}] slot{}\n"
                "set name: {}\n"
                "notes: {}\n"
                "HP1: {}\n"
                "fusionmax: {}\n"
                "primary stat: {} {}\n"
                "secondary stats: {} {}\n"
                "```").format(query, text[1],
                self.bopaeData[query]["setName"],
                self.bopaeData[query]["setNotes"],
                reqBopae["HP1"], reqBopae["fusionmax"],
                reqBopae["stat1"], reqBopae["data1"],
                reqBopae["stat2"], reqBopae["data2"]
                )

            await self.bot.say(multiline)



def setup(bot):
    if isSoupAvail:
        bot.add_cog(Bopae(bot))
    else:
        raise RuntimeError("You need to run `pip3 install beautifulsoup4`")

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
import asyncio
from urllib.parse import quote



class Bopae:
    """BNS soul shield utils"""

    def __init__(self, bot):
        self.bot = bot
        self.bopaeData = dataIO.load_json("data/bopae/bopae.json")


    def bopae_namesearch(self, query):
        """Searches the corresponding object key given query"""
        query = query.lower()

        if query in self.bopaeData:
            return query

        if len(query) < 3:
            # print("DEBUG: search request too short")
            return ""

        query = re.compile(query)
        for i in self.bopaeData:
            for tag in self.bopaeData[i]["tags"]:
                # if tag == query:
                #     return i
                if query.search(tag) != None:
                    return i

        for i in self.bopaeData:
            if query.search(self.bopaeData[i]["setName"].lower()) != None:
                return i

        return ""


    def bopae_math(self, mathType, *text):
        """This does math stuff. TODO"""
        mathType = mathType.lower()
        for i in text:
            try:
                text[i] = int(i)
            except:
                text.remove(i)
                # invalids.add(i)

        if mathType = "sum":
            return sum(text)

        elif re.search(mathType, "^average") != None:
            if len(text) == 0:
                return 0        # possible div by zero
            return sum(text)/len(text)

        return 0


    # name should be valid key
    # slot integer in range 1..8
    # stat should be valid stat key
    def bopae_getdata(self, name, slot, stat):
        """Returns integer given valid request"""
        " AP cRate cDmg PEN aDmg Ele CCdmg ACC HP1 HP2 DEF cDef VIT REG EVA BLK rDmg fusionmax "

        try:
            return self.bopaeData[name]["slot"+slot][stat]
        except:
            return 0

    def bopae_statsearch(self, query):
        name = name.lower()
        quert = query.lower()
        key = ""
        if query in ["ap", "attkpwr", "attackpwr", "attkpower", "attackpower"]:
            key = "AP"
        elif query in ["crate", "crit", "critical", "critrate", "criticalrate"]:
            key = "cRate"
        return ""


    @commands.command()
    async def bopae(self, *text):
        ("BNS soul shield utils\n"
        "Usage: !bopae list\n"
        "       !bopae [name]\n"
        "       !bopae [name] [1-8 / all]...\n"
        "       !bopae user [username]")

        if text == ():
            await self.bot.say("```"
                            "Usage: !bopae list\n"
                            "       !bopae [name]\n"
                            "       !bopae [name] [1-8 / all]...\n"
                            "       !bopae user [username]```")


        elif text[0] == "list":
            multiline = "Available SS sets: " + ", ".join(map(str, self.bopaeData))
            await self.bot.say(multiline)


        # elif text[0] == "search":
        #     if len(text) != 2:
        #         await self.bot.say("Usage: !bopae search [query]")
        #         return
        #     await self.bot.say("DEBUG: bopae search result: " + self.bopae_namesearch(text[1]))


        elif text[0] == "user":
            name = " ".join(map(str, text[1::]))
            url = "http://na-bns.ncsoft.com/ingame/bs/character/profile?c="+quote(name, safe='')

            async with aiohttp.get(url) as resp:
                if resp.status != 200:
                    multiline = "```url: {}\n".format(url)
                    multiline += "BNS server potato (http resp status {})```".format(resp.status)
                    await self.bot.say(multiline)
                    return
                soup = BeautifulSoup(await resp.text(), 'html.parser')

            try:
                wall = soup.body.find(id="container").find(id="contents")
                wall = wall.find(class_="characterInfo").find(class_="itemArea")
                wall = wall.find(class_="wrapGem").find(class_="gemIcon").find("map")
                multiline = "```Requested name [{}]\n".format(name)
                multiline += "url: {}\n".format(url)
                slot = 1
                for piece in wall.find_all("area"):
                    try:
                        multiline += "slot #{}: {}, \titem-ID {}\n".format(slot, piece["alt"], piece["item-data"])
                    except:
                        multiline += "slot #{}: empty\n".format(slot)
                    slot += 1
                multiline += "```"
                await self.bot.say(multiline)
            except:
                await self.bot.say("Unable to find [{}]".format(name))


        else :
            """specific bopae stat"""

            if len(text[0]) < 3:
                await self.bot.say("Search request too short (must be at least 3 characters long)")
                return

            query = self.bopae_namesearch(text[0])
            if query == "":
                await self.bot.say("Unable to find requested set [{}]".format(text[0]))
                return

            multiline = "```"
            multiline += ("Set name: {} [{}]\n"
                            "Notes: {}\n"
                            "\n").format(self.bopaeData[query]["setName"],
                            query, self.bopaeData[query]["setNotes"])

            multiline += "Set bonus:\n"
            for i in self.bopaeData[query]["setBonus"]:
                multiline += "{} set: {}\n".format(i, self.bopaeData[query]["setBonus"][i])
            multiline += "\n"

            if "all" in text[1::]:
                querySet = [1, 2, 3, 4, 5, 6, 7, 8]
            else:
                querySet = text[1::]
            for reqSlot in querySet:
                try:
                    reqBopae = self.bopaeData[query]["slot"+str(reqSlot)]
                    multiline += (
                        "Slot {}\n"
                        "HP1: {}\n"
                        "Fusion max: {}\n"
                        "Primary stat: {} {}\n"
                        "Secondary stats: {} {}\n"
                        "\n"
                        ).format(reqSlot,
                        reqBopae["HP1"], reqBopae["fusionmax"],
                        reqBopae["stat1"], reqBopae["data1"],
                        reqBopae["stat2"], reqBopae["data2"]
                        )

                except:
                    multiline += "Invalid bopae slot requested [{}]\n\n".format(reqSlot)

            multiline += "```"
            await self.bot.say(multiline)



def setup(bot):
    if isSoupAvail:
        bot.add_cog(Bopae(bot))
    else:
        raise RuntimeError("You need to run `pip3 install beautifulsoup4`")

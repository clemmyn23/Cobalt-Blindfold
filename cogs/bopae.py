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
        self.allcmds = ["list", "user", "search", "debug"]

    @commands.command()
    async def bopae(self, *text):
        ("BNS soul shield utils\n"
        "Usage: !bopae list\n"
        "       !bopae user [username]\n"
        "       !bopae [name]\n"
        "       !bopae search(optional) [name] [1-8 / all]...\n")

        if text == ():
            await self.bot.say("```{}```".format(self.bopaecmd_help()))

        elif text[0] == "debug":
            if len(text[1]) >= 2:
                # query = " ".join(map(str, text[1::]))
                # await self.bot.say("DEBUG: bopae search result: " + self.bopae_statsearch(query))
                query = self.bopae_parser(text[1::])
                await self.bot.say("DEBUG: bopae parser: {}".format(query))
            else:
                await self.bot.say("Usage: !bopae debug [query]")

        elif text[0] == "help":
            await self.bot.say("```{}```".format(self.bopaecmd_help()))

        elif text[0] == "list":
            await self.bot.say(self.bopaecmd_list())

        elif text[0] == "user":
            resp = await self.bopaecmd_user(text[1::])
            await self.bot.say("```{}```".format(resp))

        elif text[0] == "useradv":
            resp = await self.bopaecmd_useradv(text[1::])
            await self.bot.say("```{}```".format(resp))

        elif text[0] == "math":
            resp = self.bopaecmd_math(text[1::])
            await self.bot.say("```{}```".format(resp))

        elif text[0] == "search":
            await self.bot.say("```{}```".format(self.bopaecmd_search(text[1::])))
        else:
            await self.bot.say("```{}```".format(self.bopaecmd_search(text)))


    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    # = = = = = = = = = = = = = COMMAND HANDLERS  = = = = = = = = = = = = = = = = = = = =

    def bopaecmd_help(self):
        return ("BNS soul shield utils\n"
            "Usage: !bopae list\n"
            "       !bopae user [username]\n"
            "       !bopae [name]\n"
            "       !bopae search(optional) [name] [1-8 / all]... [name] [1-8]...\n")


    def bopaecmd_list(self):
        multiline = "Available SS sets: {}\n".format(", ".join(map(str, self.bopaeData)))
        multiline += "Available stats: AP cRate cDmg PEN aDmg Ele CCdmg ACC "
        multiline += "HP1 HP2 DEF cDef VIT REG EVA BLK rDmg fusionmax"
        return multiline


    def bopaecmd_search(self, text):
        query = self.bopae_parser(text)
        multiline = query["multiline"] + "\n"
        del query["multiline"]

        for bopaeset in query:
            # try:
                multiline += ("# # # # # # # # # #\n"
                            "Set name: {} [{}]\n"
                            "Notes: {}\n"
                            "\n").format(self.bopaeData[bopaeset]["setName"],
                            bopaeset, self.bopaeData[bopaeset]["setNotes"])

                multiline += "Set bonus:\n"
                for i in self.bopaeData[bopaeset]["setBonus"]:
                    multiline += "{} set: {}\n".format(i, self.bopaeData[bopaeset]["setBonus"][i])
                multiline += "\n"

                for reqSlot in query[bopaeset]:
                    reqBopae = self.bopaeData[bopaeset]["slot"+str(reqSlot)]
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

                multiline += "\n"
            # except:
            #     multiline += "Internal error\n"
        return multiline


    async def bopaecmd_user(self, text):
        if text == ():
            return self.bopaecmd_help()

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


    async def bopaecmd_useradv(self, text):
        return "TODO"


    def bopaecmd_math(self, text):
        if text == () or len(text) < 2:
            return "See usage"
        if text[0] == "sum":
            reqstat = self.bopae_statsearch(text[1])
            if reqstat == "" or reqstat == "fusionmax":
                return "invalid request or fusionmax TODO [{}]\n".format(text[1])

            query = self.bopae_parser(text[2::])
            del query["multiline"]

            result = 0
            for bopaeset in query:
                for i in query[bopaeset]:
                    result += self.bopae_getdata(bopaeset, i, reqstat)

            return "result: {}, requested sets: {}".format(str(result), query)

        return "TODO"


    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    # = = = = = = = = = = = = = UTILITIES = = = = = = = = = = = = = = = = = = = = = = = =
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


    # name should be valid key
    # slot integer in range 1..8
    # stat should be valid stat key
    def bopae_getdata(self, name, slot, stat):
        """Returns integer given valid request"""
        try:
            return self.bopaeData[name]["slot"+str(slot)][stat]
        except:
            return 0


    # TODO better exception handling
    # takes in text:list. returns dictionary key:setname, value:list integer slots
    # multiline in dict: multiline string of errors. "" on empty
    def bopae_parser(self, text):
        currset = ()
        query = {"multiline": ""}
        for i in text:
            name = self.bopae_namesearch(i)
            if name == "":
                if i == "all" and currset != ():
                    query[currset] = [1, 2, 3, 4, 5, 6, 7, 8]
                else:
                    try:
                        i = int(i)

                        if currset == ():
                            raise Exception('Attempted to assign soulshield slot to empty set')
                        if i < 1 or i > 8:
                            raise Exception('Invalid soul shield slot')

                        if currset not in query:
                            query[currset] = list()
                            query[currset].append(i)
                        elif i not in query[currset]:
                            query[currset].append(i)
                    except:
                        if currset == ():
                            query["multiline"] += "Invalid set name [{}]\n".format(i)
                        else:
                            query["multiline"] += "Invalid slot num [{}] for set [{}]\n".format(i, currset)
            else:
                if name not in query:
                    query[name] = list()
                currset = name

        return query


    def bopae_namesearch(self, query):
        """Searches the corresponding object key given query"""
        query = query.lower()
        if query in self.bopaeData:
            return query

        if len(query) < 3:
            return ""

        query = re.compile(query)
        for i in self.bopaeData:
            if query.search(self.bopaeData[i]["setName"]) != None:
                return i
            for tag in self.bopaeData[i]["tags"]:
                if query.search(tag) != None:
                    return i

        return ""


    def bopae_statsearch(self, query):
        # TODO optimise
        # " AP cRate cDmg PEN aDmg Ele CCdmg ACC HP1 HP2 DEF cDef VIT REG EVA BLK rDmg fusionmax "
        if len(query) < 2:
            return ""

        query = re.compile(query.lower())
        for i in ["AP", "cRate", "cDmg", "PEN", "aDmg", "Ele", "CCdmg", "ACC", "HP1", "HP2", "DEF", "cDef", "VIT", "REG", "EVA", "BLK", "rDmg", "fusionmax"]:
            if query.search(i.lower()) != None:
                return i

        return ""

        # for i in ["ap", "attkpwr", "attackpwr", "attkpower", "attackpower", "attack power"]:
        #     if query.search(i) != None:
        #         return "AP"
        # for i in ["crate", "critical", "critrate", "criticalrate", "critical rate"]:
        #     if query.search(i) != None:
        #         return "cRate"
        # for i in ["cdmg", "critdamage", "criticaldmg", "criticaldamage", "critical damage"]:
        #     if query.search(i) != None:
        #         return "cDmg"
        # for i in ["pen"]:
        #     if query.search(i) != None:
        #         return "PEN"
        # for i in ["admg"]:
        #     if query.search(i) != None:
        #         return "aDmg"
        # for i in ["ele"]:
        #     if query.search(i) != None:
        #         return "Ele"
        # for i in ["ccdmg"]:
        #     if query.search(i) != None:
        #         return "CCdmg"
        # for i in ["acc", "accuracy"]:
        #     if query.search(i) != None:
        #         return "ACC"
        #
        # for i in ["hp1"]:
        #     if query.search(i) != None:
        #         return "HP1"
        # for i in ["hp2"]:
        #     if query.search(i) != None:
        #         return "HP2"
        # for i in []:
        #     if query.search(i) !- None:
        #         return "DEF"
        # for i in []:
        #     if query.search(i) !- None:
        #         return "cDef"
        # for i in []:
        #     if query.search(i) !- None:
        #         return "VIT"
        # for i in []:
        #     if query.search(i) !- None:
        #         return "REG"
        # for i in []:
        #     if query.search(i) !- None:
        #         return "EVA"
        # for i in []:
        #     if query.search(i) !- None:
        #         return "BLK"
        # for i in []:
        #     if query.search(i) !- None:
        #         return "rDmg"
        # for i in []:
        #     if query.search(i) !- None:
        #         return "fusionmax"
        # return ""



def setup(bot):
    if isSoupAvail:
        bot.add_cog(Bopae(bot))
    else:
        raise RuntimeError("You need to run `pip3 install beautifulsoup4`")

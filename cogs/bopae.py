import discord
import re
from discord.ext import commands
from cogs.utils.dataIO import dataIO
import asyncio


# BOPAE_STATS = False
# BOPAE_USERPARSE = False

def setup(bot):
    bot.add_cog(Bopae2(bot))

    # if BOPAE_STATS:
    #     try:
    #         from cogs.bopae.parser import *
    #     except:
    #         pass
    # if BOPAE_USERPARSE:
    #     try:
    #         from cogs.bopae.statistics import *
    #     except:
    #         pass



class Bopae2:
    """BNS soul shield utils"""

    def __init__(self, bot):
        self.bot = bot
        self.bopaeData = dataIO.load_json("data/bopae/bopae.json")
        self.allcmds = ["list", "user", "search", "debug"]

    @commands.command()
    async def bopae2(self, *text):
        ("BNS soul shield utils\n\n"
        "Commands:\n"
        "  (search) [name] [1-8 / all]..  Soul Shield search\n"
        "  list                           List all available sets\n")

        if not text or text[0] == "help":
            await self.bot.say("```{}```".format(self.bopaecmd_help()))

        elif text[0] == "list":
            await self.bot.say(self.bopaecmd_list())

        else:
            await self.bot.say("```{}```".format(self.bopaecmd_search(text)))


    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    # = = = = = = = = = = = = = COMMAND HANDLERS  = = = = = = = = = = = = = = = = = = = =

    def bopaecmd_help(self):
        return ("BNS soul shield utils\n\n"
        "Commands:\n"
        "  [name] [1-8 / all]..  Soul Shield search\n"
        "  list                  List all available sets")

    def bopaecmd_list(self):
        multiline = "Available SS sets:\n{}\n".format(", ".join(map(str, self.bopaeData)))
        # multiline += "Available stats: AP cRate cDmg PEN aDmg Ele CCdmg ACC "
        # multiline += "HP1 HP2 DEF cDef VIT REG EVA BLK rDmg fusionmax"
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



    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    # = = = = = = = = = = = = = UTILITIES = = = = = = = = = = = = = = = = = = = = = = = =

    # # name should be valid key
    # # slot integer in range 1..8
    # # stat should be valid stat key
    # def bopae_getdata(self, name, slot, stat):
    #     """Returns integer given valid request"""
    #     try:
    #         return self.bopaeData[name]["slot"+str(slot)][stat]
    #     except:
    #         return 0


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
        if query == ():
            return ""

        query = query.lower()
        if query in self.bopaeData:
            return query

        if len(query) < 3 or query == "all":
            return ""

        query = re.compile(query)
        for i in self.bopaeData:
            if query.search(self.bopaeData[i]["setName"].lower()) != None:
                return i
            for tag in self.bopaeData[i]["tags"]:
                if query.search(tag) != None:
                    return i

        return ""

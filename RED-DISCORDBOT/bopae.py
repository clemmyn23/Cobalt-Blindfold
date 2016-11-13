import os, re, asyncio
import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from __main__ import send_cmd_help
from .utils.chat_formatting import *

from libbopae.main import *



BOPAE_DATA_DIR = 'data/bopae/'

def setup(bot):
    bot.add_cog(Bopae(bot))


class Bopae:
    """BNS soul shield utils"""

    def __init__(self, bot):
        self.bot = bot

        self.bopaeData = {}
        for f in os.listdir(BOPAE_DATA_DIR):
            self.bopaeData.update(dataIO.load_json(BOPAE_DATA_DIR + f))


    @commands.group(name="bopae", pass_context=True)
    async def bopae(self, ctx):
        """BNS soul-shield search and utilities
        search format: ([set name] [slot num/all]...)...
        example: !bopae yeti 2 4 ebon all asura 1 3 5
        """

        if ctx.invoked_subcommand is None:
            text = ctx.message.content.split()
            if len(text) > 1:
                search_result = self.bopaecmd_search(text[1::])
                for page in pagify(search_result, ['\n']):
                    await self.bot.say(box(page))
            else:
                await send_cmd_help(ctx)


    @bopae.command(name="list")
    async def bopaecmd_list(self):
        """Show SS sets in the database"""

        multiline = "Available SS sets:\n{}\n".format(", ".join(map(str, self.bopaeData)))
        # multiline += "Available stats: AP cRate cDmg PEN aDmg Ele CCdmg ACC "
        # multiline += "HP1 HP2 DEF cDef VIT REG EVA BLK rDmg fusionmax"
        await self.bot.say(multiline)



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

import asyncio
import discord
from discord.ext import commands
from __main__ import send_cmd_help
from cogs.utils import checks

import re, json


BOPAE_DATA_DIR = 'data/bopae/'

def setup(bot):
    bot.add_cog(BopaeRED(bot))


class Bopae:
    """BNS soul shield utils"""

    def __init__(self, bot):
        self.bot = bot

        self.bopaeData = {}
        self.data_dir = BOPAE_DATA_DIR
        self.reload()

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



    # Reloads soul-shield data
    @bopae.command(name="reload")
    @checks.is_owner()
    def reload(self):
        """Reload database."""
        self.bopaeData = {}
        for file in os.listdir(self.data_dir):
            with open(self.data_dir + file) as f:
                self.bopaeData.update(json.load(f))
        await self.bot.say("bopae db reloaded")


    @bopae.group(name="config", pass_context=True)
    async def config(self, ctx):
        return


    @bopae.command(name="reload")
    @checks.is_owner()
    async def reload(self):
        """Reload database."""
        try:
            self.Bopae.reload()
            await self.bot.say("bopae db reloaded")
        except Exception as e:
            await self.bot.say("{}".format(e))

    @bopae.command(name="list")
    async def list(self):
        """Show SS sets in the database"""
        multiline = "Available SS sets:\n{}\n".format(", ".join(map(str, self.bopaeData)))
        # multiline += "Available stats: AP cRate cDmg PEN aDmg Ele CCdmg ACC "
        # multiline += "HP1 HP2 DEF cDef VIT REG EVA BLK rDmg fusionmax"
        return multiline

    @bopae.command(name="search", pass_context=True)
    async def search(self, ctx):
        """BNS soul-shield search."""

        # TODO use embed
        # title setName
        # inline piece stats
        # - title: primary stat
        # - content1: secondary stats
        # - content2: fusionmax
        # inline image


        if len(ctx.message.content.split()) > 2:
            query = message.split()
            if query[0].lower() == "search":
                query = query[1::]
            query = self._parser(message.split()[1::])

            multiline = query["multiline"] + "\n"
            del query["multiline"]

            for bopaeset in query:
                multiline += ("# # # # # # # # # #\n"
                            "Set name: {} [{}]\n"
                            "Notes: {}\n"
                            "\n").format(self.bopaeData[bopaeset]["setName"],
                            bopaeset, self.bopaeData[bopaeset]["setNotes"])

                multiline += "Set bonus:\n"
                for i in sorted(self.bopaeData[bopaeset]["setBonus"]):
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

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            search_result = multiline

            for page in pagify(search_result, ['\n']):
                await self.bot.say(box(page))
        else:
            await send_cmd_help(ctx)

    @bopae.command(name="compare", aliases=["cmp"], pass_context=True)
    async def compare(self, ctx):
        """BNS soul-shield compare.
        FORMAT: !bopae compare/cmp [name1] [name2] [slot#]
        """
        await self.bot.say("bopae compare temporarily disabled")
        return

        # if len(ctx.message.content.split()) > 2:
        #     search_result = self.Bopae.compare(ctx.message.content)
        #     for page in pagify(search_result, ['\n']):
        #         await self.bot.say(box(page))
        # else:
        #     await send_cmd_help(ctx)




    # TODO better exception handling
    # takes in text:list. returns dictionary key:setName, value:list integer slots
    # multiline in dict: multiline string of errors. "" on empty
    def _parser(self, text):
        currset = ()
        query = {"multiline": ""}
        for i in text:
            name = self._namesearch(i)
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


    def _namesearch(self, query):
        """Searches the corresponding object key given query"""
        if query == ():
            return ""

        query = query.lower()
        if query in [setnames.lower() for setnames in self.bopaeData]:
            return query

        if len(query) < 3 or query == "all":
            return ""

        query = re.compile(query, flags=re.IGNORECASE)
        for i in self.bopaeData:
            if query.search(self.bopaeData[i]["setName"].lower()) != None:
                return i
            for tag in self.bopaeData[i]["tags"]:
                if query.search(tag) != None:
                    return i

        return ""

import asyncio
import discord
import re, json, os
from discord.ext import commands
from __main__ import send_cmd_help
from cogs.utils import checks


BOPAE_DATA_DIR = 'data/bopae/'

def setup(bot):
    bot.add_cog(Bopae(bot))


class Bopae:
    """BNS soul shield utils"""

    def __init__(self, bot):
        self.bot = bot
        self.data_dir = BOPAE_DATA_DIR
        self.bopaeData = {}
        for file in os.listdir(self.data_dir):
            with open(self.data_dir + file) as f:
                self.bopaeData.update(json.load(f))


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
                await self._search(ctx)
            else:
                await send_cmd_help(ctx)


    @bopae.command(name="list")
    async def list(self):
        await self._list()
    async def _list(self):
        """Show SS sets in the database"""
        multiline = "Available SS sets:\n{}\n".format(", ".join(map(str, self.bopaeData)))
        # multiline += "Available stats: AP cRate cDmg PEN aDmg Ele CCdmg ACC "
        # multiline += "HP1 HP2 DEF cDef VIT REG EVA BLK rDmg fusionmax"
        await self.bot.say(multiline)


    @bopae.command(name="search", pass_context=True)
    async def search(self, ctx):
        await self._search(ctx)
    async def _search(self, ctx:discord.ext.commands.Context):
        """BNS soul-shield search."""

        # passes params into _parser() for parsing
        # returns dictionary
        # e.g.:
        # { "errormsg": "some error messages",
        #   "yeti": [ 1, 2, 3 ],
        #   "asura": [ 4, 5 ]
        # }
        #


        query = ctx.message.content.split()
        if len(query) <= 1:     # TODO better input handling
            await send_cmd_help(ctx)
            return
        query = query[1::]                  # chops the "!bopae"
        if query[0].lower() == "search":    # chops the "!bopae search"
            query = query[1::]

        if len(query) <= 1:
            await send_cmd_help(ctx)
            return

        query = self._parser(query)         # parse the query

        if query["errormsg"]:
            await self.bot.say("{}\n".format(query["errormsg"]))
        del query["errormsg"]


        for bopaeset in query:
            if len(query[bopaeset]) == 0:
                # TODO print set stats and bonuses
                await self.bot.say('TODO: set bonuses and shield info goes here')
                continue

            for slotNum in query[bopaeset]:
                reqBopae = self.bopaeData[bopaeset]
                reqPiece = self.bopaeData[bopaeset]["slot"+str(slotNum)]

                embed = discord.Embed()
                try:
                    if reqBopae['rarity'].lower() == 'purple':
                        embed.colour = discord.Colour(value=123)
                    elif reqBopae['rarity'].lower() == 'gold':
                        embed.colour = discord.Colour(value=456)
                    else:
                        embed.colour = discord.Colour(value=789)
                except KeyError:
                    await self.bot.say("DEBUG: no rarity field in json")
                    embed.colour = discord.Colour(value=678)

                # embed.title = "{} - Slot {}".format(reqBopae['setName'], slotNum)
                embed.description = 'piece description here'
                embed.add_field(name='HP1_stat', value=reqPiece['HP1'])
                embed.add_field(name='primary_stat_name {}'.format(reqPiece['stat1']), value='{}'.format(reqPiece['data1']))
                embed.add_field(name='secondary_stat_names', value='valueshere')
                embed.add_field(name='fusionmax', value='valueshere')
                try:
                    embed.set_author(name="{} - Slot {}".format(reqBopae['setName'], slotNum))
                    imageUrl = reqBopae['imageUrl'][:-5] + str(slotNum) + '.png'
                    embed.set_thumbnail(url=imageUrl)
                except KeyError:
                    await self.bot.say('DEBUG: no imageUrl field in json')
                    embed.set_author(name="{} - Slot {}".format(reqBopae['setName'], slotNum))

                await self.bot.say(embed=embed)




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
    # errormsg in dict: errormsg string of errors. "" on empty
    def _parser(self, text):
        currset = ()
        query = {"errormsg": ""}
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
                            raise ValueError('Invalid soul shield slot')

                        if currset not in query:
                            query[currset] = list()
                            query[currset].append(i)
                        elif i not in query[currset]:
                            query[currset].append(i)
                    except:
                        if currset == ():
                            query["errormsg"] += "Invalid set name [{}]\n".format(i)
                        else:
                            query["errormsg"] += "Invalid slot num [{}] for set [{}]\n".format(i, currset)
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

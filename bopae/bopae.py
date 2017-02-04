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
        """Show SS sets in the database"""
        await self._list()
    async def _list(self):
        multiline = "Available SS sets:\n{}"\
                    .format(", ".join(map(str, self.bopaeData)))
        # multiline += "Available stats: AP cRate cDmg PEN aDmg Ele CCdmg ACC "
        # multiline += "HP1 HP2 DEF cDef VIT REG EVA BLK rDmg fusionmax"
        await self.bot.say(multiline)


    @bopae.command(name="search", pass_context=True)
    async def search(self, ctx):
        """BNS soul-shield search."""
        await self._search(ctx)
    async def _search(self, ctx:discord.ext.commands.Context):

        # passes params into _parser() for parsing
        # returns dictionary
        # e.g.:
        # { "errormsg": "some error messages",
        #   "yeti": [ 1, 2, 3 ],
        #   "asura": [ 4, 5 ]
        # }
        #

        # pre: '!bopae ' is guaranteed by discord.ext.commands method decorator
        query = ctx.message.content.split()
        query = query[1::]                  # chops the "!bopae"
        if len(query) == 0:                 # no bopae set specified. send help
            await send_cmd_help(ctx)
            return
        if query[0].lower() == "search":    # chops the "!bopae search"
            query = query[1::]
        if len(query) == 0:                 # no bopae set specified. send help
            await send_cmd_help(ctx)
            return

        query = self._parser(query)         # parse the query

        if query["errormsg"]:
            await self.bot.say("{}\n".format(query["errormsg"]))
        del query["errormsg"]

        for bopaeset in query:

            if len(query[bopaeset]) == 0:
                reqBopae = self.bopaeData[bopaeset]
                embed = discord.Embed()

                # Title
                try:
                    embed.set_author(name=reqBopae['setName'])
                    imageUrl = reqBopae['imageUrl']         # use default image
                    print(imageUrl)
                    embed.set_thumbnail(url=imageUrl)
                except KeyError:
                    await self.bot.say('DEBUG: no imageUrl field in json')
                    embed.set_author(name=reqBopae['setName'])

                # Description and Set Bonuses
                embed.description = reqBopae['setNotes']
                embed.add_field(name='3-Set Bonuses',
                                value='{}'.format(reqBopae['setBonus']['3']),
                                inline=False)
                embed.add_field(name='5-Set Bonuses',
                                value='{}'.format(reqBopae['setBonus']['5']),
                                inline=False)
                embed.add_field(name='Full-set Bonuses',
                                value='{}'.format(reqBopae['setBonus']['8']),
                                inline=False)

                # Embed Colour
                try:
                    if reqBopae['rarity'].lower() == 'purple':
                        embed.colour = discord.Colour.purple()
                    elif reqBopae['rarity'].lower() == 'gold':
                        embed.colour = discord.Colour.gold()
                    else:
                        await self.bot.say("DEBUG: unknown rarity value on json")
                        embed.colour = discord.Colour.blue()
                except KeyError:
                    await self.bot.say("DEBUG: no rarity field in json")
                    embed.colour = discord.Colour.blue()

                await self.bot.say(embed=embed)
                continue


            for slotNum in query[bopaeset]:
                reqBopae = self.bopaeData[bopaeset]
                reqPiece = self.bopaeData[bopaeset]["slot"+str(slotNum)]
                embed = discord.Embed()

                # Title
                try:
                    embed.set_author(name="{} - Slot {}".format(reqBopae['setName'], slotNum))
                    imageUrl = '{}{}.png'.format(reqBopae['imageUrl'][:-5], str(slotNum))
                    embed.set_thumbnail(url=imageUrl)
                except KeyError:
                    await self.bot.say('DEBUG: no imageUrl field in json')
                    embed.set_author(name="{} - Slot {}".format(reqBopae['setName'], slotNum))

                # Notes and description
                embed.description = reqBopae['setNotes']

                embed.add_field(name='HP',
                                value=', '.join([str(i) for i in reqPiece['HP1']]),
                                inline=True)

                embed.add_field(name='Fusion Maximum',
                                value='{}'.format(reqPiece['fusionmax']),
                                inline=True)

                embed.add_field(name='Primary - {}'.format(Bopae.getstatname(reqPiece['stat1'])),
                                value=', '.join([str(i) for i in reqPiece['data1']]),
                                inline=False)

                stat2names = ', '.join([Bopae.getstatname(i) for i in reqPiece['stat2']])
                embed.add_field(name='{}'.format(stat2names),
                                value=', '.join([str(i) for i in reqPiece['data2']]),
                                inline=False)

                # Embed colour (bopae rarity)
                try:
                    if reqBopae['rarity'].lower() == 'purple':
                        embed.colour = discord.Colour.purple()
                    elif reqBopae['rarity'].lower() == 'gold':
                        embed.colour = discord.Colour.gold()
                    else:
                        await self.bot.say("DEBUG: unknown rarity value on json")
                        embed.colour = discord.Colour.blue()
                except KeyError:
                    await self.bot.say("DEBUG: no rarity field in json")
                    embed.colour = discord.Colour.blue()

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


    # TODO: ongoing
    @staticmethod
    def getstatname(abbrev):
        abbrev = abbrev.lower()

        if abbrev == 'hp1':
            return 'HP'
        elif abbrev == 'hp2':
            return 'HP'

        elif abbrev == 'ap':
            return 'Attack Power'
        elif abbrev == 'crate':
            return 'Critical Rate'
        elif abbrev == 'cdmg':
            return 'Critical Damage'
        elif abbrev == 'acc':
            return 'Accuracy'
        elif abbrev == 'def':
            return 'Defence'
        elif abbrev == 'eva':
            return 'Evasion'
        elif abbrev == 'pen':
            return 'Penetration'

        elif abbrev == 'cdef':
            return 'Critical Defence'
        elif abbrev == 'blk':
            return 'Block'

        elif abbrev == 'vit':
            return 'Vitality'

        elif abbrev == 'reg':
            return 'Recovery'

        elif abbrev == 'ccdmg':
            return 'ccdmg'

        elif abbrev == 'fusionmax':
            return 'Fusion maximum'

        else:
            return abbrev

import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
# try:
    # from bs4 import BeautifulSoup
    # isSoupAvail = True
# except:
    # isSoupAvail = False
# import aiohttp


class Bopae:
    """Some silly blade and soul commands for idk reasons"""
    

    def __init__(self, bot):
        self.bot = bot
        self.bopaeData = dataIO.load_json("data/bopae/bopae.json")
        # print("blade cog __init__ here")
        


    @commands.command()
    async def bopae(self, *text):
        """... because g-sheets take forever to load\n
        Usage:\n !bopae list\n !bopae [name]\n !bopae [name] [1-8]\n 
        """
        
        if text == () or len(text) > 2:
            # await self.bot.say("Usage: !bopae [setAbbrev] [slotPos (1-8) (optional)]")
        # elif text[0] == "-user":
            # await self.bot.say("FEATURE UNIMPLEMENTED.")
            
        # if text == () or len(text) != 2:
            await self.bot.say("`Usage: !bopae list\n       !bopae [name]\n       !bopae [name] [1-8]`")
        else:
            if len(text) == 1:
                """bopae set stats"""
                # await self.bot.say("Feature unimplemented")
                if text[0] == "list":
                    multiline = "Available SS sets: "
                    for set in self.bopaeData:
                        multiline += "{} ".format(set)
 
                    await self.bot.say(multiline)
                else:
                    try:
                        reqBopae = self.bopaeData[text[0]]
                        multiline = ("```REQUESTED SOUL SHIELD SET [{}]\n"
                            "set name: {}\n"
                            "set notes: {}\n").format(text[0], reqBopae["setName"], reqBopae["setNotes"])
                            
                        for i in reqBopae["setBonus"]:
                            multiline += "set bonus {}: {}\n".format(i, reqBopae["setBonus"][i])
                        
                        multiline += "```"
                        await self.bot.say(multiline)
                    except:
                        await self.bot.say("invalid bopae request [{}]".format(text[0]))
                    
                    
            elif len(text) == 2:
                """specific bopae stat"""
                try:
                    reqBopae = self.bopaeData[text[0]]["slot"+text[1]]
                    
                    multiline = ("```"
                        "REQUESTED SOUL SHIELD PIECE [{}] [{}]\n"
                        "set name: {}\n"
                        "notes: {}\n"
                        "HP1: {}\n"
                        "fusionmax: {}\n"
                        "primary stat: {} {}\n"
                        "secondary stats: {} {}\n"
                        "```").format(text[0], text[1],
                        self.bopaeData[text[0]]["setName"], self.bopaeData[text[0]]["setNotes"], 
                        reqBopae["HP1"], reqBopae["fusionmax"],
                        reqBopae["stat1"], reqBopae["data1"],
                        reqBopae["stat2"], reqBopae["data2"]
                        )
                    
                    await self.bot.say(multiline)

                except:
                    await self.bot.say("invalid bopae request [{}] [{}]".format(text[0], text[1]))


        
def setup(bot):
    bot.add_cog(Bopae(bot))

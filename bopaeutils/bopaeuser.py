try:
    from bs4 import BeautifulSoup
    isSoupAvail = True
except:
    isSoupAvail = False

import re
import aiohttp
from urllib.parse import quote



class Bopae_parser:

    # TODO:
    # - extract all data from web
    # - map data to set names
    # - calculations versus BIS


    def __init__(self):
        # TODO
        pass

    # async def bopaecmd_user(self, text):
    #     if text == ():
    #         return self.bopaecmd_help()
    #
    #     name = quote(" ".join(map(str, text)), safe='')
    #     url = "http://na-bns.ncsoft.com/ingame/bs/character/profile?c=" + name
    #
    #     async with aiohttp.get(url) as resp:
    #         if resp.status != 200:
    #             multiline = "{}\n".format(url)
    #             multiline += "BNS server potato (http resp status {})".format(resp.status)
    #             # await self.bot.say(multiline)
    #             return multiline
    #         soup = BeautifulSoup(await resp.text(), 'html.parser')
    #
    #     try:
    #         wall = soup.body.find(id="container").find(id="contents").find(class_="characterInfo")
    #         wall = wall.find(class_="itemArea").find(class_="wrapGem").find(class_="gemIcon").find("map")
    #         multiline = "Requested name [{}]\n".format(name)
    #         multiline += "{}\n".format(url)
    #         slot = 1
    #         for piece in wall.find_all("area"):
    #             try:
    #                 multiline += "slot #{}: {}, \titem-ID {}\n".format(slot, piece["alt"], piece["item-data"])
    #             except:
    #                 multiline += "slot #{}: empty\n".format(slot)
    #             slot += 1
    #         return multiline
    #     except:
    #         return "Unable to find character [{}]".format(name)
    #

    # async def bopaecmd_useradv(self, text):
    #     return "TODO"

    # def bopaecmd_math(self, text):
    #     if text == () or len(text) < 2:
    #         return "See usage"
    #     if text[0] == "sum":
    #         reqstat = self.bopae_statsearch(text[1])
    #         if reqstat == "" or reqstat == "fusionmax":
    #             return "invalid request or fusionmax TODO [{}]\n".format(text[1])
    #
    #         query = self.bopae_parser(text[2::])
    #         del query["multiline"]
    #
    #         result = 0
    #         for bopaeset in query:
    #             for i in query[bopaeset]:
    #                 result += self.bopae_getdata(bopaeset, i, reqstat)
    #
    #         return "result: {}, requested sets: {}".format(str(result), query)
    #
    #     return "TODO"

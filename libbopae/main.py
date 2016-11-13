import os, re

# from . import chat_formatting


class Bopae:
    """BNS soul shield utils"""

    def __init__(self, data_dir : str):
        self.bopaeData = {}
        self.data_dir = data_dir
        self.reload()

    # Reloads soul-shield data
    def reload(self):
        self.bopaeData = {}
        for f in os.listdir(self.data_dir):
            self.bopaeData.update(dataIO.load_json(self.data_dir + f))


    # Lists all soul-shield sets in the database
    # return : str
    def list(self):
        """Show SS sets in the database"""

        multiline = "Available SS sets:\n{}\n".format(", ".join(map(str, self.bopaeData)))
        # multiline += "Available stats: AP cRate cDmg PEN aDmg Ele CCdmg ACC "
        # multiline += "HP1 HP2 DEF cDef VIT REG EVA BLK rDmg fusionmax"
        return multiline


    # soul-shield search.
    # message : str
    # return : str
    def search(self, message : str):
        """BNS soul-shield search.
        FORMAT:
            !bopae ([set name] [slot num/all]...)...
        EXAMPLES:
            !bopae tomb 1
            !bopae yeti 2 4 ebon all asura 1 3 5
        """

        query = self._parser(message.split()[1::])
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
        if query in self.bopaeData:
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

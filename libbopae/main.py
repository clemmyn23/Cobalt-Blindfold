import os, re, json

class Bopae:
    """BNS soul shield utils"""

    def __init__(self, data_dir : str):
        self.bopaeData = {}
        self.data_dir = data_dir
        self.reload()

    # Reloads soul-shield data
    def reload(self):
        self.bopaeData = {}
        for file in os.listdir(self.data_dir):
            with open(self.data_dir + file) as f:
                self.bopaeData.update(json.load(f))


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
        if query[0].lower() == "search":
            query = query[1::]

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
            # except:
            #     multiline += "Internal error\n"
        return multiline


    # soul-shield side-by-side listing
    # format: !bopae compare [name1] [name2] [slotnum]
    # message : str
    # return : str
    def compare(self, message : str):
        # Example format
        # !bopae cmp yeti asura 1
        # ---------------------------------------------
        # [SET NAME 1]                [SET NAME 2]
        #
        # [NOTES 1]                   [NOTES 2]
        #
        # [SLOT #]
        # HP1: 123                  < HP1: 234
        # "fusionmax": 234          > "fusionmax": 230
        # Primary:
        # "ACC": 123                < "ACC": 234
        #
        # Secondary:
        # "cRate": 234              = "cRate": 234
        # "DEF": 234                > "DEF": 123
        # "EVA": 234
        #                             "BLK": 345
        #

        multiline = ''
        message = message.split()[2::]
        key1 = self._namesearch(message[0])
        key2 = self._namesearch(message[1])
        slot = message[2]

        # INPUT CHECKS AND EXIT
        if key1 == '':
            multiline += "invalid set name [{}]\n".format(message[0])
        if key2 == '':
            multiline += "invalid set name [{}]\n".format(message[1])
        try:
            slot = int(slot)
            if slot < 0 or slot > 8:
                raise
        except:
            multiline += "invalid slot num [{}] {}\n".format(message[2])
        if multiline != '':
            return multiline

        # SET NAMES
        multiline = "# # # # # # # # # #\n"
        name1 = "{} [{}]".format(self.bopaeData[key1]['setName'], key1)
        name1 = [name1[i:i+25] for i in range(0, len(name1), 25)]
        name2 = "{} [{}]".format(self.bopaeData[key2]['setName'], key2)
        name2 = [name2[i:i+25] for i in range(0, len(name2), 25)]
        numlines = len(name1) if len(name1) > len(name2) else len(name2)
        for i in range(0, numlines):
            try:
                multiline += name1[i].ljust(26)
            except:
                multiline += ' ' * 26
            finally:
                multiline += '   '

            try:
                multiline += name2[i]
            except:
                pass
            finally:
                multiline += '\n'
        multiline += '\n'

        # SET NOTES
        bonus1 = self.bopaeData[key1]['setNotes']
        bonus1 = [bonus1[i:i+25] for i in range(0, len(bonus1), 25)]
        bonus2 = self.bopaeData[key2]['setNotes']
        bonus2 = [bonus2[i:i+25] for i in range(0, len(bonus2), 25)]
        numlines = len(bonus1) if len(bonus1) > len(bonus2) else len(bonus2)
        for i in range(0, numlines):
            try:
                multiline += bonus1[i].ljust(26)
            except:
                multiline += ' ' * 26
            finally:
                multiline += '   '

            try:
                multiline += bonus2[i]
            except:
                pass
            finally:
                multiline += '\n'
        multiline += '\n'

        multiline += '# SLOT {} #\n'.format(slot)
        slot = 'slot' + str(slot)
        piece1 = self.bopaeData[key1][slot]
        piece2 = self.bopaeData[key2][slot]

        # HP1, fusionmax
        hp1_cmp = ' = ' if piece1['HP1'][-1] == piece2['HP1'][-1] else \
                (' > ' if piece1['HP1'][-1] > piece2['HP1'][-1] else ' < ')
        multiline += "HP1: {}".format(piece1['HP1']).ljust(26)
        multiline += "{}HP1: {}\n".format(hp1_cmp, piece2['HP1'])

        fusionmax_cmp = ' = ' if piece1['fusionmax'] == piece2['fusionmax'] else \
                (' > ' if piece1['fusionmax'] > piece2['fusionmax'] else ' < ')
        multiline += "fusionmax: {}".format(piece1['fusionmax']).ljust(26)
        multiline += "{}fusionmax: {}\n".format(fusionmax_cmp, piece2['fusionmax'])
        multiline += '\n'

        # PRIMARY
        multiline += '# PRIMARY STAT:\n'
        stat1_cmp = ' = ' if piece1['data1'][1] == piece2['data1'][1] else \
                (' > ' if piece1['data1'][1] > piece2['data1'][1] else ' < ')
        if piece1['stat1'] == piece2['stat1']:
            multiline += '{}: {}'.format(piece1['stat1'], piece1['data1']).ljust(26)
            multiline += "{}{}: {}\n".format(stat1_cmp, piece2['stat1'], piece2['data1'])
        else:
            multiline += '{}: {}\n'.format(piece1['stat1'], piece1['data1'])
            multiline += '{}{}: {}\n'.format(' '*29, piece2['stat1'], piece2['data1'])
        multiline += '\n'

        # SECONDARY
        multiline += '# SECONDARY STATS:\n'
        stat2_cmp = ' = ' if piece1['data2'][1] == piece2['data2'][1] else \
                (' > ' if piece1['data2'][1] > piece2['data2'][1] else ' < ')
        for i in piece1['stat2']:
            if i in piece2['stat2']:
                if i == 'HP2':
                    multiline += '{}: {}'.format(i, piece1['data2'][2:4]).ljust(26)
                    multiline += "{}{}: {}\n".format(stat2_cmp, i, piece2['data2'][2:4])
                else:
                    multiline += '{}: {}'.format(i, piece1['data2'][0:2]).ljust(26)
                    multiline += "{}{}: {}\n".format(stat2_cmp, i, piece2['data2'][0:2])
            else:
                if i == 'HP2':
                    multiline += '{}: {}\n'.format(i, piece1['data2'][2:4])
                else:
                    multiline += '{}: {}\n'.format(i, piece1['data2'][0:2])
        for i in piece2['stat2']:
            if i not in piece1['stat2']:
                if i == 'HP2':
                    multiline += '{}{}: {}'.format(' '*29, i, piece2['data2'][2:4])
                else:
                    multiline += '{}{}: {}'.format(' '*29, i, piece2['data2'][0:2])

        return multiline


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

from bs4 import BeautifulSoup

if __name__ == '__main__':

    soup = BeautifulSoup(open('charsearch2.html'), 'html.parser')


    numresults = 0
    try:
        a = soup.body.find('div', id="container").find('div', id="contents").find('p', class_="schResult")
        a.strong.unwrap()    # there are two <strong> tags
        numresults = int(a.strong.string)
        a.strong.unwrap()
        schResult = ''.join(a.contents)
    except Exception as e:
        print(e)

    print("numresults. {}".format(numresults))
    # exit()

    if numresults == 0:
        print("no result exiting now")
        exit()

    # ==STRUCTURE==
    # accountname   (parsed from alts)
    # user          (abstract)
    # - mainchar
    # - - mainchar_name
    # - - mainchar_stats
    # - alts

    # print("** parsing main")
    user = soup.body.find('div', id='container').find('div', class_='searchList')

    mainchar = user.ul.li.dl
    mainchar_name = mainchar.dt.a
    mainchar_stats = mainchar.find('dd', class_='desc').ul.contents
    for i in mainchar_stats:
        if i == "\n":
            mainchar_stats.remove(i)

    # print("** parsing alts")
    accountname = user.find('dd', class_='other').dl.dt.strong
    alts = user.find('dd', class_='other').dl.find('dd', class_='desc2').ul.find_all('a')

    # print("*************** info")
    multiline = ""
    multiline += ("{}\n".format(schResult))
    multiline += ("Account:\n  {}\n".format(accountname.string))
    multiline += ("Main:\n  {}\n".format(mainchar_name.string))
    multiline += ("    {}\n".format(mainchar_name.get("href")))
    for i in mainchar_stats:
        multiline += ("  {}\n".format(i.string))
    multiline += ("Other characters:\n")
    for i in alts:
        multiline += ("  {}\n".format(i.string))
        multiline += ("    {}\n".format(i.get("href")))

    print(multiline)
    # await self.bot.say("```{}```".format(multiline))
    #
    # await self.bot.say("parsing error. {}".format(e))

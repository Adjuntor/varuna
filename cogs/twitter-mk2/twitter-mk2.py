#Allows to import config.py from the directory above
import os
import os.path
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.config as config
import time
import re
import json

#Discord lib
import discord
from discord.ext import commands, tasks

# Selenium shit
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class TwitterMK2(commands.Cog, name="TwitterMK2"):
    """Twitter stuff"""

    __chrome_options = Options()
    __chrome_options.add_argument("--headless")
    __chrome_options.add_argument("--remote-debugging-port=9222")
    __twitterUrl = "https://twitter.com"
    __cache = {}
    __jsonPath = config.PATH_TO_STORAGE + "/scrapper.json"
    __driver = None
    __jsonFile = None

    @commands.Cog.listener()
    async def on_ready(self):
        print('TwitterMK2 Cog initialized')
        self.main_process.start()

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.__loadJson()
        self.__driver = webdriver.Chrome(options = self.__chrome_options, service = Service(config.CHROME_DRIVER))

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def register(self, interaction: discord.Interaction, url: str = None):
        if url is None:
            await interaction.response.send_message("tweet <url>. Register twitter user to listen to")
        # ignore previous registration. Always destroy
        cache[url] = {"pinned": [], "lastId": None}
        await channel.send(f"Successfully registered")

    def __getId(self, url):
        regStr = ".*\/status\/(\d+)"
        reRes = re.search(regStr, url)
        return reRes[1]

    def __signOnKiller(self):
        self.__driver.execute_script("document.querySelector('div[data-testid=\"BottomBar\"]').remove()")

    # to kill notification popup
    def __notificationKiller(self):
        notificationPopup = self.__driver.find_elements(By.CSS_SELECTOR, 'div[data-testid=\"sheetDialog\"]')

        if len(notificationPopup) > 0:
            notificationPopup[0].find_element(By.CSS_SELECTOR, 'div > div > div:first-child > div > div > svg').click()
            time.sleep(1)

    def __exists(self, arr, valToCheck):
        try:
            arr.index(valToCheck)
            return True
        except ValueError:
            return False
        except:
            print("Some other error lol")
        
        return False

    def __loadJson(self):
        jsonPath = self.__jsonPath
        jsonFile = None
        if not os.path.isfile(jsonPath):
            jsonFile = open(jsonPath, "w")
            jsonFile.write("")
            jsonFile.close()
            
        jsonFile = open(jsonPath, "r+")
        jsonContent = jsonFile.read()
        jsonFile.close()
        if jsonContent:
            self.__cache = json.loads(jsonContent)

        for url in config.FOLLOWING:
            if self.__cache.get(url) is None:
                self.__cache[url] = {"pinned": [], "lastId": None}
            
        self.__jsonFile = jsonFile

    @tasks.loop(seconds = 60)
    async def main_process(self):
        try:
            for url in config.FOLLOWING:
                self.__driver.get(url)
                time.sleep(config.TIME_TO_WAIT_IN_SECONDS)

                # main page loaded
                self.__notificationKiller()
                self.__signOnKiller()

                foundTheId = False

                visitedArticles = []

                # main process
                while not foundTheId:
                    articles = self.__driver.find_elements(By.TAG_NAME, "article")
                    for article in articles:

                        if self.__exists(visitedArticles, article.id):
                            continue
                        
                        innertxt = article.get_attribute("innerText")
                        if innertxt.startswith("Pinned Tweet"):
                            # check pinned tweet storage instead
                            self.__notificationKiller()
                            ActionChains(self.__driver).move_to_element(article).perform()
                            
                            artUrl = article.find_element(By.CSS_SELECTOR, "a[href*=\"status\"]").get_attribute("href")
                            artUrl = self.__twitterUrl + artUrl

                            id = self.__getId(artUrl)

                            if not self.__exists(self.__cache[url]["pinned"], id):
                                self.__cache[url]["pinned"].append(id)
                                # discord stuff

                            continue
                        else:                    
                            artUrl = article.find_element(By.CSS_SELECTOR, "a[href*=\"status\"]").get_attribute("href")
                            artUrl = self.__twitterUrl + artUrl

                            id = self.__getId(artUrl)

                            if not self.__cache[url]["lastId"] == id:
                                self.__cache[url]["lastId"] = id
                                # discord stuff
                            
                            foundTheId = True

            self.__jsonFile = open(self.__jsonPath, "w")
            self.__jsonFile.write(json.dumps(self.__cache))
            self.__jsonFile.close()
        except Exception as e:
            print("Error in twitterMK2")
            print(e)
                    

async def setup(bot: commands.Bot):
  await bot.add_cog(TwitterMK2(bot))

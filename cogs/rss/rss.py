#Allows to import config.py from the directory above
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.config as config

#Discord lib
import discord
from discord.ext import commands, tasks

#RSS Parser
import feedparser
from datetime import datetime, timedelta, timezone
import aiosqlite
from aiosqlitepool import SQLiteConnectionPool

async def start_db():
    return await aiosqlite.connect("config/articles.db")  

async def parse_date(articledate):
    posttime = articledate.split('GMT')
    beautiful_date = datetime.strptime(posttime[0].strip(), "%a, %d %b %Y %H:%M:%S").replace(tzinfo=timezone.utc)
    return beautiful_date
      
async def record_article_in_db(article):
    pool = SQLiteConnectionPool(start_db,pool_size=5,acquisition_timeout=60)
    async with pool.connection() as db:
        post_date = await parse_date(article.published)
        await db.execute("INSERT INTO articles (link, date) VALUES (?, ?)", (article.link, post_date))
        await db.commit()
    await pool.close()

async def article_in_db(entry):
    pool = SQLiteConnectionPool(start_db,pool_size=20,acquisition_timeout=15)
    async with pool.connection() as db:
        is_on_database = await db.execute("SELECT link FROM articles WHERE link = ?", (entry.link,))
        await db.commit()
        if  await is_on_database.fetchone() is None:
            await pool.close()
            return False          
        else:
            await pool.close()
            return True      

async def get_new_articles():
    new_articles = []
    for rss_feed in config.RSS_FEEDS:
        entries = feedparser.parse(rss_feed["url"]).entries
        for entry in entries:
            if not await article_in_db(entry):
                pub_date = await parse_date(entry.published)
                if datetime.now(timezone.utc) - pub_date <= timedelta(days=config.RSS_LAST_ARTICLE_RANGE):
                    new_articles.append({"article": entry, "channel": rss_feed["channel"], "feedTitle": feedparser.parse(rss_feed["url"]).feed.title})
    return new_articles

async def format_to_message(article):
    article_link = article["article"].link
    if "https://x.com" in article_link:
        article_link = article_link.replace("https://x.com","https://fxtwitter.com")
    if "https://twitter.com" in article_link:
        article_link = article_link.replace("https://twitter.com","https://fxtwitter.com")
    if "http://x.com" in article_link:
        article_link = article_link.replace("http://x.com","https://fxtwitter.com")
    if "http://twitter.com" in article_link:
        article_link = article_link.replace("http://twitter.com","https://fxtwitter.com")
    message = f"{article_link}"
    return message
    

class RSS(commands.Cog, name="RSS"):
    """RSS cog"""
    @commands.Cog.listener()
    async def on_ready(self):
        print('RSS Cog initialized')
        pool = SQLiteConnectionPool(start_db)
        async with pool.connection() as db:
            await db.execute("CREATE TABLE IF NOT EXISTS articles (link TEXT, date TEXT)")
            await db.commit()
        await pool.close()
        self.cleandb.start()
        self.rss.start()
        
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @tasks.loop(hours = 24)
    async def cleandb(self):
        date_cutout = datetime.now(timezone.utc) - timedelta(days=config.RSS_LAST_ARTICLE_RANGE + 1)
        pool = SQLiteConnectionPool(start_db,pool_size=20,acquisition_timeout=15)
        async with pool.connection() as db:
            await db.execute("DELETE FROM articles WHERE DATE < ?", (date_cutout,))
            await db.commit()
        await pool.close()

    @tasks.loop(seconds = config.RSS_UPDATE_INTERVAL)
    async def rss(self):
        new_articles = await get_new_articles()
        for article in new_articles:
            message = await format_to_message(article)
            await self.bot.get_channel(int(article["channel"])).send(message)
            await record_article_in_db(article["article"])
 
async def setup(bot: commands.Bot):
    await bot.add_cog(RSS(bot))

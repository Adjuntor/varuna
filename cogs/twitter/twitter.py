#Allows to import config.py from the directory above
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.config as config

#User array
following = config.TWITTER_FOLLOWING

#Discord lib
from discord.ext import commands, tasks

#Tweepy lib
import tweepy.asynchronous

class MyAsyncStreamingClient(tweepy.asynchronous.AsyncStreamingClient):
    def __init__(self, bot, bearer_token, **kwargs):
        super().__init__(bearer_token, **kwargs)
        self.bot = bot

    async def on_response(self, response: tweepy.StreamResponse):
        tweet = response.data
        username = response.includes['users'][0].username

        if tweet.in_reply_to_user_id is not None:
            return
        #Find the twitter id and the channel from the config file array
        for x in range(len(following)):
                if tweet.author_id == following[x][0]:
                    channel_id = following[x][1]
                    await self.bot.get_channel(channel_id).send(content=f"https://twitter.com/{username}/status/{tweet.id}")
    
    async def on_exception(self, exception):
        print(f"Exception while running Tweeter streamer V2:\n"
              f"{exception.__class__.__name__}")
        print(exception)
        exit(exception)
    
    async def on_disconnect(self):
        print(f'Disconnected from Twitter Stream')   
    async def on_connect(self):
        print(f'Connected to Twitter Stream')

    async def initiate_stream(self):
        print("Starting Twitter Stream")
        rules = await self.get_rules()
        #Delete old rules
        if rules[0] is not None:
            for r in rules[0]:
                await self.delete_rules(r.id) 
        #Add rules from config file  
        new_rules = tweepy.StreamRule(' OR '.join([f"from:{following[x][0]} -is:retweet -is:reply -is:nullcast" for x in range(len(following))]))
        await self.add_rules(new_rules)
        #With this you only get original tweet and not reply
        self.filter(
            expansions='author_id',
            tweet_fields=[
                'author_id',
                'in_reply_to_user_id'
            ],
            user_fields=[
                'created_at'
            ]
        )

async def new_stream(bot: commands.Bot):
    print("Creating Twitter stream")
    tStream = MyAsyncStreamingClient(bot, config.TWITTER_BEARER, wait_on_rate_limit=True)
    await tStream.initiate_stream()

class Twitter(commands.Cog, name="Twitter"):
    """Twitter cog"""
    def __init__(self, bot):
        self.bot = bot
        self.tStream = None

    @commands.Cog.listener()
    async def on_ready(self):
        print('Twitter Cog initialized')
        self.start_stream.start()

    @tasks.loop(count=1)
    async def start_stream(self):
        await new_stream(self.bot)

async def setup(bot: commands.Bot):
  await bot.add_cog(Twitter(bot))



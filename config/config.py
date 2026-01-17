################################----DISCORD TOKENS----###############################
TOKEN = "AJigbsFALKNFN*#Q&FNOAEfn8yqw3tgo309ot789123456AFDUIOHBFSIUojks_AFSJKNSF0"
OWNER_ID = 12345678901234567890
PREFIX = "."
EMBEDCOLOR=0x408020
#####################################################################################

################################----COGS TO LOAD----#################################
ACTIVECOGS = ["activity.py", "rss.py", "twitter.py", "twitter-mk2.py"]
#####################################################################################

###################################----TWITTER----###################################
#Set the array as [twitter_user_id, discord_channel_id]
#twitter_user_id: the id of the person you want to follow, ex: 44196397
#discord_channel_id: the id of the discord channel you want to post all tweets
TWITTER_FOLLOWING = [
    [44196397,4059123452180252830],  # Elon Musk
    [11348282,9959194743629204856],  # Nasa
    [11348282,5493859438512378459],  # Nasa again but in another channel
    [1072404907230060544, 8937832461213380938] # Genshin Impact
]

# URL(s) to scrape
FOLLOWING = ["https://twitter.com/NIKKE_en", "https://twitter.com/honkaiimpact3rd"]

# Path to chrome driver to be used by selenium
CHROME_DRIVER = ""

# Path to storage/cache
PATH_TO_STORAGE = ""

# Time to wait for page to load
TIME_TO_WAIT_IN_SECONDS = 8

#Twitter tokens, need ELEVATED priviledge
TWITTER_BEARER=r"AAAAAAAAAAAAAAAAAAAAAE1234567890LKnfikaujFJANSKJfbakhsbfakhsnfoF#*(NFOQOGFN"
#######################################################################################

####################################----ACTIVITY----####################################
#Activity status list, it will randomly change every hour. Use a "," to separate the strings
PLAY_STAT = ["on the web", "videogames"]# Playing ...
WATCH_STAT = ["over the web"]# Watching ...
LISTEN_STAT = ["the web"]#Listening to ...
########################################################################################

####################################----RSS----####################################
# Update interval for how often the bot is supposed to check if a new entry in the RSS feed exists (in Seconds)
RSS_UPDATE_INTERVAL = 60

# How far a new entry in the RSS feed can can be published in the past before being ignored (in Days)
RSS_LAST_ARTICLE_RANGE = 5

# Add the RSS feeds here. Each object consists of the RSS feed URL and the channel ID you want to post on
RSS_FEEDS = [
    {
        "url": "http://rss.feed",
        "channel": "1460912367289625245"
    },
    {
        "url": "http://website.feed",
        "channel": "14123673739089625245"
    }
]
#######################################################################################

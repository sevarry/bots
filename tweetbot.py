import tweepy, time, sys

tweetfile = str(sys.argv[1])

CONSUMER_KEY = 'YOUR CONSUMER KEY'
CONSUMER_SECRET = 'YOUR CONSUMER SECRET KEY'
ACCESS_KEY = 'YOUR ACCESS KEY'
ACCESS_SECRET = 'YOUR ACCESS SECRET KEY'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

filename=open(tweetfile,'r')
f=filename.readlines()
filename.close()

for line in f:
    api.update_status(status=line)
    time.sleep(900)#Tweet every 15 minutes

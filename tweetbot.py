#!/usr/bin/env python

import tweepy
import time
import sys
import sqlite3

tweetfile = str(sys.argv[1])
sqlite_db = 'bots.db'
conn = sqlite3.connect(sqlite_db)
cursor = conn.cursor()

def tweet(bot):
    acct = (bot[0])
    ckey = (bot[2])
    csecret = (bot[3])
    akey = (bot[4])
    asecret = (bot[5])
    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(akey, asecret)
    api = tweepy.API(auth)
    filename=open(tweetfile,'r')
    f=filename.readlines()
    filename.close()
    for line in f:
        api.update_status(status=line)
        print '\nTweeting', line, 'from bot', acct
    time.sleep(2)

def main():
    cursor.execute('''SELECT * from bot_list''')
    for bot in cursor:
        tweet(bot)
        time.sleep(2)

main()

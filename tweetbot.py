#!/usr/bin/env python

import getopt
import tweepy
import time
import sys
import sqlite3

sqlite_db = 'bots.db'
conn = sqlite3.connect(sqlite_db)
cursor = conn.cursor()

def tweet(bot):
    tweetmsg = str(sys.argv[2])
    acct = (bot[0])
    ckey = (bot[2])
    csecret = (bot[3])
    akey = (bot[4])
    asecret = (bot[5])
    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(akey, asecret)
    api = tweepy.API(auth)
    try:
        api.update_status(status=tweetmsg)
        print '\nTweeting', tweetmsg, 'from bot', acct
    except tweepy.TweepError as e:
        print(e.reason)
    time.sleep(2)

def retweet(bot):
    acct = (bot[0])
    ckey = (bot[2])
    csecret = (bot[3])
    akey = (bot[4])
    asecret = (bot[5])
    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(akey, asecret)
    api = tweepy.API(auth)
    query = str(sys.argv[2])
    max_tweets = 5
    found = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]
    try:
        for i in found:
            print '\nRetweeting "',i.text,'" from bot--->', acct
            api.retweet(i.id)
    except tweepy.TweepError as e:
        print(e.reason)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:r:", ["tweet","retweet"])
    except getopt.GetoptError as err:
        print str(err)
        return
    for o,a in opts:
        if o in ("-t","--tweet"):
            cursor.execute('''SELECT * from bot_list''')
            for bot in cursor:
                tweet(bot)
                time.sleep(2)
        elif o in ("-r","--retweet"):
            cursor.execute('''SELECT * from bot_list''')
            for bot in cursor:
                retweet(bot)
                time.sleep(2)

main()

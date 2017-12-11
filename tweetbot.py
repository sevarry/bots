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
    acct = (bot[0])
    ckey = (bot[2])
    csecret = (bot[3])
    akey = (bot[4])
    asecret = (bot[5])
    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(akey, asecret)
    api = tweepy.API(auth)
    try:
        api.update_status(status=tweet_msg)
        print '\nTweeting', tweet_msg, 'from bot', acct
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
    max_tweets = 5
    found = [status for status in tweepy.Cursor(api.search, q=rt_query).items(max_tweets)]
    try:
        for i in found:
            print '\nRetweeting "',i.text,'" from bot--->', acct
            api.retweet(i.id)
    except tweepy.TweepError as e:
        print(e.reason)

def like(bot):
    acct = (bot[0])
    ckey = (bot[2])
    csecret = (bot[3])
    akey = (bot[4])
    asecret = (bot[5])
    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(akey, asecret)
    api = tweepy.API(auth)
    max_tweets = 25
    found = [status for status in tweepy.Cursor(api.search, q=like_query).items(max_tweets)]
    try:
        for i in found:
            print '\nLiking "',i.text,'" by bot--->', acct
            api.create_favorite(i.id)
    except tweepy.TweepError as e:
        print(e.reason)

def usage():
    print
    print "TwitterBot Control Console"
    print
    print "Usage: tweetbot.py"
    print "-t 'Hello World!'"
    print
    print "-r '#helloworld'"
    print
    print "-l '#helloworld'"
    print
    sys.exit(0)

def main():
    global tweet_msg
    global rt_query
    global like_query

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht:r:l:")
    except getopt.GetoptError as err:
        print str(err)
        return
    for o,a in opts:
        if o in ("-h"):
            usage()
        elif o in ("-t"):
            tweet_msg = a
            cursor.execute('''SELECT * from bot_list''')
            for bot in cursor:
                tweet(bot)
                time.sleep(2)
        elif o in ("-r"):
            rt_query = a
            cursor.execute('''SELECT * from bot_list''')
            for bot in cursor:
                retweet(bot)
                time.sleep(2)
        elif o in ("-l"):
            like_query = a
            cursor.execute('''SELECT * from bot_list''')
            for bot in cursor:
                like(bot)
                time.sleep(2)
        else:
            assert False,"Unhandled Option"
main()

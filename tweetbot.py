#!/usr/bin/env python

#created by Ted Eckerman, 2017

import getopt
import getpass
import os
import requests
import tweepy
import time
import sys
import sqlite3

sqlite_db = 'bots.db'
conn = sqlite3.connect(sqlite_db)
cursor = conn.cursor()

class bcolors:
    green = '\033[92m'
    endc = '\033[0m'

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

def image(bot,filename):
    acct = (bot[0])
    ckey = (bot[2])
    csecret = (bot[3])
    akey = (bot[4])
    asecret = (bot[5])
    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(akey, asecret)
    api = tweepy.API(auth)
    try:
        api.update_with_media(filename)
        print '\nSharing',url,'by bot--->', acct
    except tweepy.TweepError as e:
        print(e.reason)

def follow(bot):
    acct = (bot[0])
    ckey = (bot[2])
    csecret = (bot[3])
    akey = (bot[4])
    asecret = (bot[5])
    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(akey, asecret)
    api = tweepy.API(auth)
    max_tweets = 10
    found = [status for status in tweepy.Cursor(api.search, q=follow_query).items(max_tweets)]
    try:
        for i in found:
            api.create_friendship(i.author._json['screen_name'])
            print acct,'Following',i.author._json['screen_name']
    except tweepy.TweepError as e:
        print(e.reason)

def newbot():
    acct = raw_input("\nEnter the new twitter account's name, i.e. @twitter:\n")
    email = raw_input("\nEnter the twitter account email address:\n")
    ckey = getpass.getpass("\nEnter the twitter account's CONSUMER KEY:\n")
    csecret = getpass.getpass("\nEnter the twitter account's CONSUMER SECRET:\n")
    akey = getpass.getpass("\nEnter the twitter account's ACCESS KEY:\n")
    asecret = getpass.getpass("\nEnter the twitter account's ACCESS TOKEN:\n")

    cursor.execute("""INSERT INTO bot_list ('account', 'email', 'consumer_key', 'consumer_secret', 'access_key', 'access_secret') VALUES (?, ?, ?, ?, ?, ?)""", (acct, email, ckey, csecret, akey, asecret))
    user_confirm = raw_input("Thank you, commit the new account to the database? Y/N:\n")
    if user_confirm == 'Y':
        conn.commit()
        print "\n",acct,"successfully added to the database!"
    else:
        print "\nExiting without committing new account"
        sys.exit()

def usage():
    print
    print 'TwitterBot Control Console'
    print
    print 'Usage: tweetbot.py'
    print
    print '-a to add a new Twitter account to the database:'
    print bcolors.green + 'python tweetbot.py -a' + bcolors.endc
    print
    print '-t to tweet a status update from all bots:'
    print bcolors.green + 'python tweetbot.py -t "Hello World!"' + bcolors.endc
    print
    print '-r to retweet from all bots based on a search query:'
    print bcolors.green + 'python tweetbot.py -r "#helloworld"' + bcolors.endc
    print
    print '-l to like from all bots based on a search query:'
    print bcolors.green + 'python tweetbot.py -l "#helloworld"' + bcolors.endc
    print
    print '-i to tweet an image from all bots:'
    print bcolors.green + 'python tweetbot.py -i https://example.io/hello.png' + bcolors.endc
    print
    print '-f to follow users based on a search query:'
    print  bcolors.green + 'python tweetbot.py -f "#helloworld"' + bcolors.endc
    print
    sys.exit(0)

def main():
    global tweet_msg
    global rt_query
    global like_query
    global follow_query
    global url

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hat:r:l:i:f:')
    except getopt.GetoptError as err:
        print str(err)
        return
    for o,a in opts:
        if o in ('-h'):
            usage()
        elif o in ('-t'):
            tweet_msg = a
            cursor.execute('''SELECT * from bot_list''')
            for bot in cursor:
                tweet(bot)
                time.sleep(2)
        elif o in ('-r'):
            rt_query = a
            cursor.execute('''SELECT * from bot_list''')
            for bot in cursor:
                retweet(bot)
                time.sleep(2)
        elif o in ('-l'):
            like_query = a
            cursor.execute('''SELECT * from bot_list''')
            for bot in cursor:
                like(bot)
                time.sleep(2)
        elif o in ('-i'):
            url = a
            filename = 'temp.jpg'
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                with open(filename, 'wb') as chunk:
                    for pic in r:
                        chunk.write(pic)
            cursor.execute('''SELECT * from bot_list''')
            for bot in cursor:
                image(bot,filename)
                time.sleep(2)
            os.remove(filename)
        elif o in ('-f'):
            follow_query = a
            cursor.execute('''SELECT * from bot_list''')
            for bot in cursor:
                follow(bot)
                time.sleep(2)
        elif o in ('-a'):
            newbot()
        else:
            assert False,'Unhandled Option'
            print
            usage()
main()

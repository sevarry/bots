#!/usr/bin/env python

import tweepy
import time
import sys
import sqlite3

tweetfile = str(sys.argv[1])
sqlite_db = 'bots.db'
conn = sqlite3.connect(sqlite_db)
cursor = conn.cursor()

def tweet():
    cursor.execute('''SELECT * FROM bot_list''')
    creds = cursor.fetchone()
    acct = (creds[0])
    ckey = (creds[2])
    csecret = (creds[3])
    akey = (creds[4])
    asecret = (creds[5])
    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(akey, asecret)
    api = tweepy.API(auth)
    filename=open(tweetfile,'r')
    f=filename.readlines()
    filename.close()

    for line in f:
        api.update_status(status=line)
        print '\nTweeting', line, 'from bot', acct
        time.sleep(5)

def main():
    cursor.execute('''SELECT * from bot_list''')
    for row in cursor:
        tweet()

main()

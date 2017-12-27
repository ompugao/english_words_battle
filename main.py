#!/usr/bin/python
import twitter
import time
import os
import urllib
import logging
log = logging.getLogger('english_battle_bot')
stream_handle = logging.StreamHandler()
stream_handle.setLevel(logging.DEBUG)
log.addHandler(stream_handle)
log.setLevel(logging.DEBUG)
from pyshorteners import Shortener
from io import StringIO
from dotenv import load_dotenv
import re

#from polyglot.text import Text
# def extract_words(msg)
#     tokens = Text(msg)
#     words = []
#     for w, t in tokens.pos_tags:
#         if t in [':
# 
#         words.append(w)


def shrink_url(url):
    shortener = Shortener('Bitly', bitly_token=os.environ["BITLY_ACCESS_TOKEN"])
    return shortener.short(url)

def get_dictionary_url(word):
    return shrink_url("https://eow.alc.co.jp/search?q="+urllib.parse.quote(word))

def get_google_image_url(word):
    return shrink_url("https://www.google.co.jp/search?tbm=isch&q="+urllib.parse.quote(word))

def main():
    load_dotenv(os.path.join(os.path.dirname(__file__), 'config'))
    botname = "wordsbattle"
    target_twitterers = ["iw_tatsu", "hamko_intel", "ompugao", "D_Plius"]

    sleep_time = 1

    api = twitter.Api(access_token_key = os.environ["ACCESS_KEY"],
            access_token_secret = os.environ["ACCESS_SECRET"],
            consumer_key = os.environ["CONSUMER_KEY"],
            consumer_secret = os.environ["CONSUMER_SECRET"])


    log.info("start!")
    for tweet in api.GetUserStream():
        # validate a tweet
        if "entities" not in tweet:
            continue

        mentions = tweet["entities"]["user_mentions"]
        mentioned_users = [ mention["screen_name"] for mention in mentions ]

        log.info("got message: %s"%(tweet['text'],))

        if botname in mentioned_users:
            log.info("got a mention tweet from @%s" % tweet["user"]["screen_name"])
            #from IPython.terminal import embed; ipshell=embed.InteractiveShellEmbed(config=embed.load_default_config())(local_ns=locals())

            text = tweet['text']
            phrases = [line.lstrip().rstrip() for line in re.sub(r'#\w+', '', re.sub(r'@\w+', '', text)).split('\n')]
            phrases = [s for s in filter(lambda x: x is not '', phrases)]
            log.info("extracted phrases: %s"%(phrases,))
            for w in phrases:
                msg = StringIO()
                for tw in target_twitterers:
                    msg.write('@')
                    msg.write(tw)
                    msg.write(' ')

                msg.write(w)
                msg.write('\n')
                msg.write(get_dictionary_url(w))
                msg.write('\n')
                msg.write(get_google_image_url(w))
                msg.write(' ')

                msg.write("from @{}".format(tweet["user"]["screen_name"]))
                tweet_msg = msg.getvalue()
                log.info("tweet: " + tweet_msg)
                try:
                    api.PostUpdate(tweet_msg)
                except Exception as e:
                    log.warning("failed to tweet: %s" % e)
                time.sleep(sleep_time)

        time.sleep(sleep_time)

if __name__ == '__main__':
    main()

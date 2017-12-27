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
    botname = "words_battle"
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

        log.info("got message: {}".format(tweet.text))
        if botname in mentioned_users:
            log.info("thanking @%s for the mention" % tweet["user"]["screen_name"])
            #words = extract_words(tweet.text)
            words = tweet.text.split('\n')
            msg = StringIO()
            for w in words:
                msg.write(w)
                msg.write('\n')
                msg.write(get_dictionary_url(w))
                msg.write('\n')
                msg.write(get_google_image_url(w))
                msg.write('\n')

            msg.write("from @{}".format(tweet["user"]["screen_name"]))
            try:
                api.PostUpdate(msg.getvalue())
            except Exception as e:
                log.warning(" - failed (maybe a duplicate?): %s" % e)

        time.sleep(sleep_time)

if __name__ == '__main__':
    main()

#!/usr/bin/python
from dotenv import load_dotenv
from io import StringIO
import logging
import os
from pyshorteners import Shortener
import re
import time
import twitter
import urllib
from pyquery import PyQuery

# Constants
# TODO(tiwanari): make them configurable by a file
LOG = logging.getLogger('english_battle_bot')
BOTNAME = "wordsbattle"
TARGET_TWITTERERS = ["iw_tatsu", "hamko_intel", "ompugao", "D_Plius"]
SLEEP_TIME = 5


def init_logging():
    stream_handle = logging.StreamHandler()
    stream_handle.setLevel(logging.DEBUG)
    LOG.addHandler(stream_handle)
    LOG.setLevel(logging.DEBUG)


def read_config():
    load_dotenv(os.path.join(os.path.dirname(__file__), 'config'))


def is_valid_tweet(tweet):
    if "entities" not in tweet:
        return False

    LOG.info("got message: %s" % (tweet['text'],))

    # confirm that the tweet is a reply to this bot
    mentions = tweet["entities"]["user_mentions"]
    mentioned_users = [mention["screen_name"] for mention in mentions]
    if BOTNAME not in mentioned_users:
        return False

    LOG.info("got a mention tweet from @%s" % tweet["user"]["screen_name"])

    return True

def extract_phrases(tweet):
    text = tweet['text']

    # remove spaces in both ends, hashtags('#\w+'), and mentions('@\w+') and split by '\n' to make a word list (phrases)
    phrases = [line.lstrip().rstrip() for line in re.sub(r'#\w+', '', re.sub(r'@\w+', '', text)).split('\n')]
    return [s for s in filter(lambda x: x is not '', phrases)]


def populate_mentions(msg, base_user):
    for user in TARGET_TWITTERERS:
        # skip the user posted this tweet
        if user == base_user:
            continue
        msg.write('@')
        msg.write(user)
        msg.write(' ')


def shrink_url(url):
    shortener = Shortener('Bitly', bitly_token=os.environ["BITLY_ACCESS_TOKEN"])
    return shortener.short(url)


def get_dictionary_url(word):
    return shrink_url("https://eow.alc.co.jp/search?q=" + urllib.parse.quote(word))


def get_google_image_url(word):
    return shrink_url("https://www.google.co.jp/search?tbm=isch&q=" + urllib.parse.quote(word))


def is_ascii(word):
    return all(ord(c) < 128 for c in word)


def get_gogen_url(word):
    return shrink_url("http://eigogen.com/word/" + word + "/")

def get_gogen(word, timeout=3):
    pq = PyQuery(url=("http://eigogen.com/word/" + word), timeout=timeout)
    try:
        text = pq.find('article')[0].find('section').find('p').text
    finally:
        # FIXME
        text = 'gogen timeout'
    return text

def is_likely_an_english_word(word):
    # make sure this phrase is just one word (someone can tweet an idiom made of some words)
    if len(word.split(" ")) != 1:
        return False
    if not is_ascii(word):
        return False
    return True


def create_message(base_user, phrase, is_first_tweet):
    msg = StringIO()

    # the first tweet should include all the users
    if is_first_tweet:
        populate_mentions(msg, base_user)

    msg.write(phrase)
    msg.write('\n')
    msg.write(get_dictionary_url(phrase))
    msg.write('\n')
    msg.write(get_google_image_url(phrase))
    if is_likely_an_english_word(phrase):
        msg.write('\n')
        msg.write(get_gogen(phrase))
    msg.write(' ')
    msg.write("from @{}".format(base_user))
    return msg.getvalue()


def main():
    init_logging()
    read_config()

    api = twitter.Api(access_token_key=os.environ["ACCESS_KEY"],
                      access_token_secret=os.environ["ACCESS_SECRET"],
                      consumer_key=os.environ["CONSUMER_KEY"],
                      consumer_secret=os.environ["CONSUMER_SECRET"])

    LOG.info("start!")
    for tweet in api.GetUserStream():
        if not is_valid_tweet(tweet):
            continue

        phrases = extract_phrases(tweet)
        LOG.info("extracted phrases: %s" % (phrases,))

        base_user = tweet["user"]["screen_name"]

        prev_tweet_id, is_first_tweet = tweet["id"], True
        for phrase in phrases:
            message = create_message(base_user, phrase, is_first_tweet)

            LOG.info("posting a tweet: " + message)
            try:
                status = api.PostUpdate(
                    message,
                    in_reply_to_status_id=prev_tweet_id,
                    auto_populate_reply_metadata=True)
                prev_tweet_id, is_first_tweet = status.id, False
            except Exception as e:
                LOG.warning("failed to tweet: %s" % e)
            time.sleep(SLEEP_TIME)

        time.sleep(SLEEP_TIME)

if __name__ == '__main__':
    main()

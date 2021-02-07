import praw
from praw.exceptions import APIException
import configparser


config = configparser.ConfigParser()
config.read('conf.ini')
reddit_user = config['REDDIT']['reddit_user']
reddit_pass = config['REDDIT']['reddit_pass']
reddit_client_id = config['REDDIT']['reddit_client_id']
reddit_client_secret = config['REDDIT']['reddit_client_secret']
source_subreddit = config['SETTINGS']['source_subreddit']
target_subreddits = [i.strip() for i in config['SETTINGS']['target_subreddits'].split(',')]
crosspost_text_posts = config['SETTINGS'].getboolean('crosspost_text_posts')
crosspost_link_posts = config['SETTINGS'].getboolean('crosspost_link_posts')
test_mode = config['SETTINGS'].getboolean('test_mode')

reddit = praw.Reddit(
    username=reddit_user,
    password=reddit_pass,
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    user_agent='Crosspost Bot (by u/impshum)'
)

try:
    for submission in reddit.subreddit(source_subreddit).stream.submissions():
        for target_subreddit in target_subreddits:
            if not test_mode:
                post_allowed = False
                if submission.is_self and crosspost_text_posts:
                    post_allowed = True
                elif not submission.is_self and crosspost_link_posts:
                    post_allowed = True
                if post_allowed:
                    new_post_id = submission.crosspost(subreddit=target_subreddit, send_replies=False)
                    print(f'posted: {new_post_id}')
            else:
                print(f'TEST MODE - {submission.id}')

except APIException as e:
    print(f'Something broke with PRAW: {e}')
except Exception as e:
    print(f'Something else broke: {e}')

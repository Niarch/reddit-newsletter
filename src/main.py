import praw
import json
import logging
logging.basicConfig(level=logging.INFO, filename="logs/execution.log", filemode='w', format="%(levelname)s :: %(asctime)s :: %(message)s")

DATA_DUMP_FILEPATH="data/dump.json"

def fetch_posts_from_reddit():
    reddit = praw.Reddit('WeeklyNewsletter', config_interpolation="basic")
    logging.info("Initialized Reddit instance.")

    weekly_posts = list()

    def fetch_user_subscribed_subreddits():
        logging.info("Fetching Subreddits for the user mentioned in praw.ini...")
        user_subreddits = [subreddit.display_name for subreddit in reddit.user.subreddits(limit=None)]
        logging.info(f"Fetched {len(user_subreddits)} subreddits")

        return user_subreddits

    def fetch_top_post_json_for_subreddit(subreddit_name):
        post = dict()
        logging.info(f"Fetching info from subreddit: '{subreddit_name}'...")
        subreddit = reddit.subreddit(subreddit_name)
        for submission in subreddit.top("week", limit=1):
            post['title'] = submission.title
            post['url'] = submission.url
            post['subreddit'] = subreddit_name
            #TODO Add description text if exists
            #TODO Add image link for previewing on MD
            #TODO Add gif link for previewing on MD
            #TODO Add video link if exists for MD
            #TODO Add video thumbnail if exists for MD
        logging.info(f"Fetched post: {post.get('title')}")

        return post

    user_subreddits = fetch_user_subscribed_subreddits()
    for subreddit_name in user_subreddits:
        post = fetch_top_post_json_for_subreddit(subreddit_name)
        weekly_posts.append(post)

    return weekly_posts

def main():
    weekly_posts = fetch_posts_from_reddit()
    logging.info(f"Fetched all posts dumping data to json file: {DATA_DUMP_FILEPATH}")
    with open(DATA_DUMP_FILEPATH, "w") as json_obj:
        json.dump(weekly_posts, json_obj, indent=4)
    logging.info("Dumped data.")

    logging.info("Exiting...")

if __name__ == "__main__":
    main()
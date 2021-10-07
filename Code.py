import os
import praw
import time
import tweepy
import urllib.request
from datetime import datetime
from Credentials import reddit_info, api

reddit = praw.Reddit(client_id = reddit_info["client_id"],
                     client_secret = reddit_info["client_secret"],
                     user_agent = reddit_info["user_agent"],
                     username = reddit_info["username"],
                     password = reddit_info["password"],)

day_of_week = datetime.today().strftime('%A')
all_subreddits = {'Monday': 'animememes',
                    'Tuesday': 'dankmemes',
                    'Wednesday': 'goodanimemes',
                    'Thursday': 'AnimeFunny',
                    'Friday': 'memes',
                    'Saturday': 'anime_irl',
                    'Sunday': 'pokemonmemes'}

reddit_posts = []
reddit_titles = []
subreddit = all_subreddits[day_of_week]
scrap_subreddit = reddit.subreddit(subreddit)

for pic in scrap_subreddit.hot(limit = 100):
    if pic.url.endswith(('.png', '.jpg')):
        reddit_posts.append(pic.url)
        reddit_titles.append(pic.title)
    if len(reddit_posts) == 10:
        break

#Iterate through files and saving them to folder
os.mkdir("Meme Images")
os.chdir("Meme Images")
folder_path = os.getcwd()
image_path = os.getcwd() + "\{}"

for num, picture in enumerate(reddit_posts,1):
    with urllib.request.urlopen(picture) as image:
        with open(f"meme{num}.jpg","wb") as output:
            output.write(image.read())
            
# Getting Media-ID and Posting
ordered_names = sorted(os.listdir(folder_path), key=len)
media_ids = [api.media_upload(media).media_id_string for media in ordered_names]

for title,ids,pics in list(zip(reddit_titles,media_ids,ordered_names)):   
    time.sleep(15)
    api.update_status(title, media_ids = [ids])
    os.remove(image_path.format(pics)) 
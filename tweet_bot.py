from time import sleep
from random import randint
import random
import tweepy
import os
from os import environ
from multiprocessing import Process

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY=environ['ACCESS_KEY']
ACCESS_SECRET=environ['ACCESS_SECRET']


auth=tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

my_id=api.me().id

tags=["#photographylovers", "#hautsdefrance",
"#NaturePhotography", "#photooftheday",
"#naturelovers", "#naturephoto",
"#TwitterNatureCommunity", "#ePHOTOzine",
"#byroberteklund","#sonyalphaphotography", "#sonyalphaphotos", "#roberteklund", "#stockholm", "#sweden", "#sergelstorg", "#stockholmcity",
"#cityphotography", "#cityphoto", "#stockholmphoto", "#stockholmphotography", "#streetphotography", "#wetstreets", "#nofilter",
"#FranceMagique",  "#nature", "#sunset", "#autumncolours", "#fallcolors",
"#photoimaginart", "#photooftheday", "#stilllife","#PhotoOfTheDay", "#PicOfTheDay", "#InstaLike", "#City", "#Skyline", 
"#Skyscraper", "#Design", "#instagood", "#happy", "#travel", "#fly", "#2021","#goodmorning",
"#stilllifepainting", "#stilllifephotos", "#stilllifephotography", "#artphoto",
"#artphotography", "#fineartphotography", "#fineartphotos", "#photography", "#PHOTOS",
"#bestphoto", "#photoart", "#creativephotos", "#ArtLovers", "#photo",
"#photographie", "#landscapephotography","#BeKind", "#HOPE", "#inmygarden",  "#mondaythoughts", "#birdwatching", "#beautiful",
"#blessed", "#ThePhotoHour"]


def like_retweet():
    while True:
        random.shuffle(tags)
        for search in tags:
            for tweet in tweepy.Cursor(api.search, search).items(randint(5,15)):
                user_name=tweet.user.screen_name
                author_name=tweet.author.screen_name
                user_id=tweet.user.id
                author_id=tweet.author.id
                i_followed=api.friends_ids(api.me().id)
                if user_id != my_id:
                    if author_id not in i_followed:
                        try:
                            print(f"[INFO] -- [{user_name} / {author_name}] is not in i followd list -- ")
                            tweet.favorite()
                            print(f"[INFO] -- Tweet Liked [{user_name} / {author_name}] -- ")
                            print("[INFO] sleep for bit")
                            sleep(randint(3,7))   
                            tweet.retweet()
                            print(f"[INFO] -- Tweet retweeted [{user_name} / {author_name}] -- ")
                            print("[INFO]sleep for bit")
                            sleep(randint(3,7))
                            api.create_friendship(screen_name=tweet.author.screen_name)
                            print(f"[INFO] -- Followed [{author_name}] -- ")
                            print("[INFO] sleep for a bit")
                            sleep(randint(600,1200))
                        except tweepy.TweepError as e:
                            print(e.reason)
                            print("[WARNING] sleep for 30")
                            sleep(30)
                        except StopIteration:
                            print("[WARNING] For some reason program stoped")
                    if author_id in i_followed:
                        print("[WARNING] [ -- You follow this man already. No need to like and follow -- ]")
                if user_id == my_id:
                    print("[WARNING] [---------------------]")


def unfollow_who_dont_follow_me():
    while True:
        followers = api.followers_ids(api.me().id)
        print("[INFO] Followers", len(followers))
        friends = api.friends_ids(api.me().id)
        print("[INFO] You follow:", len(friends))

        for friend in friends[::-1]:
            if friend not in followers:
                api.destroy_friendship(friend)
                print(f"[INFO] -- Unfollow user id : {friend}")
                sleep(randint(300,1000))

def trending_now():
    while True:
        trends = api.trends_place(23424977)
        trending_hashtags = [trend['name'] for trend in trends[0]['trends'] if trend['name'].startswith('#')]
        for hashtag in trending_hashtags:
            print(hashtag)
            for tweets_in_trand in tweepy.Cursor(api.search, hashtag).items(randint(1,4)):
                trend_tweet_author_name=tweets_in_trand.author.screen_name
                trend_tweet_user_name=tweets_in_trand.user.screen_name
                trend_author_id=tweets_in_trand.author.id
                trend_user_id=tweets_in_trand.user.id
                trending_followed=api.friends_ids(api.me().id)
                if trend_user_id !=my_id:
                    if trend_author_id not in trending_followed:
                        try:
                            print(f"[INFO] -- [{trend_tweet_user_name} / {trend_tweet_author_name}] is not in followers list -- ")
                            tweets_in_trand.favorite()
                            print(f"[INFO] -- Tweet Liked [{trend_tweet_user_name} / {trend_tweet_author_name}] -- ")
                            sleep(randint(2,5))
                            tweets_in_trand.retweet()
                            print(f"[INFO] -- Tweet retweeted [{trend_tweet_user_name} / {trend_tweet_author_name}] -- ")
                            #sleep(randint(2,5))
                            #api.create_friendship(screen_name=tweets_in_trand.author.screen_name)
                            #print(f"[INFO] -- Followed [{trend_tweet_author_name}] -- ")
                            sleep(randint(2000,3600))
                            print("[INFO] -- sleep for bit -- ]")
                        except tweepy.TweepError as e:
                            print(e.reason)
                            print("[WARNING] -- [ sleep for 30 ] --")
                            sleep(30)
                        except StopIteration:
                            print("[WARNING] ---- For some reason [ trending now ] function stoped ----")
                    if trend_author_id in trending_followed:
                        print(f"oo -- [WARNING] [{trend_tweet_user_name}/{trend_tweet_author_name}] already followed. No need to like and follow -- oo")
                if trend_user_id == my_id:
                    print("[WARNING] [---------------------]")


if __name__ == "__main__":
    t1=Process(target=like_retweet)
    t2=Process(target=unfollow_who_dont_follow_me)
    t3=Process(target=trending_now)
    t1.start()
    t2.start()
    t3.start()

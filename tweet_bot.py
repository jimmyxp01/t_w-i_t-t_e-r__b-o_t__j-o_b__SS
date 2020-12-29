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
        n_tweet=randint(20,50)
        for search in tags:
            for tweet in tweepy.Cursor(api.search, search).items(n_tweet):
                try:
                    user_id=tweet.user.id
                    author_id=tweet.author.id
                    i_followed=api.followers_ids(api.me().id)
                    if user_id or author_id not in i_followed:
                        print("this peson not in I Followed list")
                        tweet.favorite()
                        print(">>>>>==== Tweet Liked ====<<<<<<")
                        print("sleep for bit")
                        sleep(randint(3,7))   
                        tweet.retweet()
                        print(">>>>==== ReTweet ====<<<<<")
                        print("sleep for bit")
                        sleep(randint(3,7))
                        api.create_friendship(screen_name=tweet.author.screen_name)
                        print(">>>>==== Followed ====<<<<")
                        print("sleep for a bit")
                        sleep(randint(200,500))
                    else:
                        print("you follow this man already. No need to like and follow")
                except tweepy.TweepError as e:
                    print(e.reason)
                    print("sleep for 30")
                    sleep(30)
                except StopIteration:
                    print("For some reason program stoped")
                    break

def unfollow_who_dont_follow_me():
    while True:
        followers = api.followers_ids(api.me().id)
        print("Followers", len(followers))
        friends = api.friends_ids(api.me().id)
        print("You follow:", len(friends))

        for friend in friends[::-1]:
            if friend not in followers:
                api.destroy_friendship(friend)
                print(f"Unfollow user id : {friend}")
                sleep(randint(100,300))


if __name__ == "__main__":
    t1=Process(target=like_retweet)
    t2=Process(target=unfollow_who_dont_follow_me)
    t1.start()
    t2.start()

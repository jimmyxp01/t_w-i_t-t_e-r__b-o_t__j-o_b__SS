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
"#FranceMagique",  "#nature", "#jobs",
"#photoimaginart", "#photooftheday", "#stilllife",
"#stilllifepainting", "#stilllifephotos", "#stilllifephotography", "#artphoto",
"#artphotography", "#fineartphotography", "#fineartphotos", "#photography", "#PHOTOS",
"#bestphoto", "#photoart", "#creativephotos", "#ArtLovers", "#photo",
"#photographie", "#landscapephotography"]


def like_retweet():
    while True:
        random.shuffle(tags)
        n_tweet=randint(50,205)
        for search in tags:
            for tweet in tweepy.Cursor(api.search, search).items(n_tweet):
                try:
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
                    sleep(randint(150,600))

                except tweepy.TweepError as e:
                    print(e.reason)
                    print("sleep for 10")
                    sleep(10)
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
                sleep(randint(900,2600))


if __name__ == "__main__":
    t1=Process(target=like_retweet)
    t2=Process(target=unfollow_who_dont_follow_me)
    t1.start()
    t2.start()

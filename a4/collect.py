"""
FILE DESCRIPTION:
-----------------

This file contains all methods that are used to collect my raw data for clustering and classification , i use the twitter
streaming api to collect tweets  occuring instantly ( i use the term "trump" to filter and pick tweets that are only
related to Donald Trump for my sentiment analysis using a Support Vector Machine) and i use my twitter rest api to
collect the followers of Ellon musk and the corresponding followers of each follower of Ellon Musk for my graph Clustering
/Community Detection.
I also clean the tweets of any URL using regex before i save it to a csv file, to try and improve my classification results

Module Requirements for this File:
1) csv
2) json
3) TwitterApi
4) sys
5) time
6) re
7) twitter (Streaming api)
8) os

You can install the twitter Streaming api by using the command
-- pip install twitter

"""
from TwitterAPI import TwitterAPI
from collections import defaultdict
import csv
import json
import sys
import time
import re
import twitter as twitter_streamer
import os

consumer_key = 'XOpcDRPwTAnpVBOZtsHZrlgxF'
# consumer_key = "Sk5T9l3xBQY76jfeMb8NjYELR"
consumer_secret = 'rXITfXsDxlQlTpWcETnUT09zcwVQhquQ1BBy3wQ2aevBhf6DTD'
# consumer_secret ="bP0UtWeDonF3iOHgnA6kyFzyrdXHIpulClNFFHgV0BoAGOz5b6"
access_token = '1389546229-2ZPMSkYlxLue2sWPtX2km4izxJSRKfWRtnoHibo'
# access_token ="800857502879514624-PUBSiZaBOjjYoXVEvAd4FACsJ8ykl97"
access_token_secret = 'XNUr0jl1eNuHfGvfX96tjdrddrgwHr9AvBp8lKUDrANXR'
# access_token_secret ="A6vD3brwdsUcBFqjLtMx0KtvXU7jXYnwYkejoA8Mn5jne"


def get_twitter():
    """ Construct an instance of TwitterAPI using the tokens you entered above.
    Returns:
      An instance of TwitterAPI.
    """
    return TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)

def robust_request(twitter, resource, params, max_tries=1):
    """ If a Twitter request fails, sleep for 15 minutes.
    Do this at most max_tries times before quitting.
    Args:
      twitter .... A TwitterAPI object.
      resource ... A resource string to request; e.g., "friends/ids"
      params ..... A parameter dict for the request, e.g., to specify
                   parameters like screen_name or count.
      max_tries .. The maximum number of tries to attempt.
    Returns:
      A TwitterResponse object, or None if failed.
    """
    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        elif request.status_code != 401:
            print(request.status_code)
            print('Got error %s \nsleeping for 15 minutes.' % request.text)
            sys.stderr.flush()
            time.sleep(61 * 15)

def get_followers(twitter, screen_name, key, count_twit = 5):
    """ Return a list of Twitter IDs for user that this person follows, up to iter.

    Note, because of rate limits, it's best to test this method for one candidate before trying
    on all candidates.

    Args:
        twitter.......The TwitterAPI object
        screen_name... a string of a Twitter screen name
        key .......... The key to use in robust_request(screen_name/id)
        iter ......... The no of request to fetch
    Returns:
        A set of ints, one per friend ID, sorted in ascending order.
    """
    ID = {}
    # count = 0
    # while(count<=iter):
    # firstlen = len(ID)
    response = robust_request(twitter,'followers/ids',{key : screen_name,"stringify_ids": "true","count": count_twit})
    if(response != None):
        for item in response.get_iterator():
                # print(item)
                ID[item] = 0
                # if(firstlen <= len(ID)):
                #     count=len(ID)
    # print(len(ID))
    return (sorted(ID.keys()))

def followers_map(screen_name,user_count):
    """
    This method creates a dictionary of user to the list of followers that follow the user. And we write this data to
    the file.

    :param          screen_name : The name of the user who's followers we want
    :param          user_count  : The number of followers you want to get , who follow the user we search for.

    :return:        The no of Users id's we have collected
    """
    twitter = get_twitter()
    map_dict =defaultdict(list)
    no_of_users = 0
    main_s = get_followers(twitter,screen_name,'screen_name',count_twit = user_count)
    map_dict[screen_name] = main_s
    # print(len(main_s))
    # print(main_s)
    for follower in main_s:
        # print(follower)
        temp_s = get_followers(twitter,follower,'user_id',count_twit = user_count)
        if  len(temp_s) > 0:
            no_of_users += len(temp_s)
            map_dict[follower] = temp_s
        elif len(temp_s) == 0:
            map_dict[follower] = []
    # print(map_dict)
    with open("Collect_Folder"+os.path.sep+screen_name+'.json', 'w') as f:
        json.dump(map_dict, f)

    print("\nCollected " + " user_ids of followers of " + screen_name + " and his follower's followers")

    print("\nNo of Users collected --> " + str(no_of_users))
    return no_of_users


def tweet_cleaner(unclean_tweet):
    """

    :param unclean_tweet:
    :return:
    """
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', unclean_tweet,
                  flags=re.MULTILINE)
    text_stage2 = re.sub(r'@\w+','',text,flags=re.MULTILINE)
    return text_stage2

def load_tweet_json(filename):
    """
    This  method loads tweets from a file in form of a list of jsons and then creates a dictionary for every tweet and then
    writes it to a .csv file for easier processing.(of the form tweet_id,tweet)

    :param      filename: Name of the file to read JSON data from

    :return:    Nothing
    """
    with open("Collect_Folder"+os.path.sep+'data.txt', 'r') as fp:
        data = json.load(fp)
        # print(type(data))
    fp.close()

    filename_without_exten = filename.split(".")

    with open("Collect_Folder"+os.path.sep+filename_without_exten[0]+".csv",'w') as wp:
        csv_writer = csv.writer(wp)
        for tweet_dict in data:
            if("id_str" in tweet_dict and "text" in tweet_dict):
                clean_tweet = tweet_cleaner(tweet_dict["text"])
                csv_writer.writerow([tweet_dict["id_str"],clean_tweet])
    wp.close()
    print("\nFinished cleaning the tweets and they have been added to data.csv")


def streaming_tweets(search_term, No_of_tweets = 20):
    """
    This method uses the twitter streaming api to collect tweets that contains the given search term , then cleans the
    tweet for url's and then saves it with it's id in a .csv file.

    :param      search_term  : The term used to search tweets with
    :param      No_of_tweets : The amount of tweets to collect which contain the search_term

    :return:    No of tweets collected
    """
    tweet_list = []
    oauth = twitter_streamer.OAuth(access_token,access_token_secret,consumer_key,consumer_secret)
    twitter_stream = twitter_streamer.TwitterStream(auth=oauth)
    iterator = twitter_stream.statuses.filter(track=search_term, language="en",retweeted=False)
    with open("Collect_Folder"+os.path.sep+'data.txt', 'w') as outfile:
        tweet_count = No_of_tweets
        for tweet in iterator:
            if( "text" in tweet ):
                if(tweet["text"].strip().startswith("RT") == False):
                    tweet_count -= 1
                    tweet_list.append(tweet)
            if(tweet_count == 0):
                break
        json.dump(tweet_list, outfile)
    outfile.close()
    print("\nCollected " + str(len(tweet_list)) + " using the term " + str(search_term))
    print("\nTweets saved to --> data.txt in Collect_Folder ")
    return len(tweet_list)

def collector_details(No_of_users,No_of_tweets):
    """
    This method saves details of the collection process employed here that is used for tweet and user collection. This
    detail that is saved is later used by Summarize.py

    :param      No_of_users  : The no of user_ids collected that follow ellon musk and ellon musk's followers
    :param      No_of_tweets : The no of tweets collected using the term "trump" for our classification task
    :return:
    """
    with open("Collect_Folder"+os.path.sep +"collector_details.txt",'w') as fp:
        fp.write("No of Users Collected : " + str(No_of_users) +"\n")
        fp.write("No of messages Collected : " + str(No_of_tweets)+"\n")

    fp.close()

def main():
    """
    This method executes all the related methods in this file, thereby performing data collection and saving them to
    Collect_Folder.

    :return: Nothing
    """
    print("\t\t************************ - Starting collect.py - ************************ ")

    No_of_tweets = streaming_tweets(search_term = "Trump",No_of_tweets=1000)
    load_tweet_json(filename="data.txt")
    No_of_users = followers_map(screen_name="elonmusk",user_count=200)
    collector_details(No_of_users=No_of_users,No_of_tweets=No_of_tweets)

    print("\n\t\t************************ - Finished Data Collection - ************************")


if __name__ == main():
    main()


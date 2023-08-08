from __future__ import print_function
import datetime
from datetime import timedelta
from distutils.command.clean import clean
import os, ast
from dotenv import load_dotenv
import numpy, time
from sklearn import preprocessing
load_dotenv()

from urllib import response
from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.urls import reverse
from .models import *

import nltk, json, re, pickle, numpy
# nltk.download('wordnet')
# nltk.download('omw-1.4')
import tweepy as tw
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import ToktokTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize

tokenizer = ToktokTokenizer()
stopword_list=nltk.corpus.stopwords.words('english')

with open('./files/contractions.json','r') as f:
    contractions_dict = json.load(f)
contractions = contractions_dict['contractions']

with open('./files/negations.json','r') as f:
    neg_dict = json.load(f)
negations = neg_dict['negations']

# Create your views here.
# app to perform model operation tasks
@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def index(request):
    return JsonResponse({
        "data":"Hello from app"
    })


def lower_case(text):
    return text.lower()

def remove_square_brackets(text):
    return re.sub('\[[^]]*\]', '', text)

def remove_username(text):
    return re.sub('@[^\s]+','',text)

def remove_urls(text):
    return re.sub(r"((http\S+)|(www\.))",'',text)

def remove_special_characters(text):
    pattern = r'[^a-zA-Z\s]'
    text = re.sub(pattern,'',text)
    return text

def remove_single_char(text):
    return re.sub(r'\b[a-zA-Z]\b','',text)

def remove_multiple(text):
    return re.sub("(.)\\1{2,}","\\1",text)

def replace_contractions(text):
    for word in text.split():
        if word.lower()  in contractions:
            text = text.replace(word,contractions[word.lower()])
    return text


class AntonymReplacer(object):
    def replace(self,word):
        antonyms = set()
        for syn in wordnet.synsets(word):
            if syn.pos() in ['a' ,'s']:
                for lemma in syn.lemmas():
                    for antonym in lemma.antonyms():
                        antonyms.add(antonym.name())
        if(len(antonyms) == 1):
            return antonyms.pop()
        else:
            if word in negations:
                word = word.replace(word,negations[word])
                return word
        
    #Negation Replacer
    def negReplacer(self, string):
        i=0
        finalSent = ""
        sent = word_tokenize(string)
        length_sent = len(sent)
        words = []
        while i < length_sent:
            word = sent[i]
            if word == 'not' and i+1 < length_sent:
                antonymWord = self.replace(sent[i+1])
                if antonymWord:
                    words.append(antonymWord)
                    finalSent += antonymWord + " "
                    i += 2
                    continue
            words.append(word)
            finalSent += word + " "
            i += 1
        return finalSent
    
def replace_negation(text):
    
    replacer = AntonymReplacer()
    oppWord = replacer.negReplacer(text)
    return oppWord


def remove_stopwords(text):
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    tokens = [token.lower() for token in tokens]
    filtered_tokens = [token for token in tokens if token not in stopword_list]
    filtered_tokens = ' '.join(filtered_tokens)
    return filtered_tokens

def fetch_tweets(product, company, keywords):
    while True:
        try:
            # credentials req for twitter API
            Consumer_API_Key = str(os.getenv('Consumer_API_Key'))
            Consumer_API_Secret_Key =  str(os.getenv('Consumer_API_Secret_Key'))
            access_token = str(os.getenv('access_token'))
            access_token_secret = str(os.getenv('access_token_secret'))

            auth = tw.OAuthHandler(consumer_key=Consumer_API_Key, consumer_secret=Consumer_API_Secret_Key)
            auth.set_access_token(access_token, access_token_secret)
            api = tw.API(auth, wait_on_rate_limit=True)

            keywordsArr = keywords.split(',')
            print(keywordsArr)
            keywordStr = ''.join(keywordsArr)
            print(keywordStr)
            # keywordLength = len(keywordsArr)
            # print('lngth', keywordLength)
            # keyword_search = ""

            # for i in range(0, keywordLength):
            #     keyword_search=keyword_search + str(keywordsArr[i]) + " OR " + str(keywordsArr[i]) + "+review OR"      

            # search query
            # new_search = product + " OR " + product +"+review OR "+ keywords + " OR " + keywords +"+review OR "  + company + " OR " + company + "+review -sale -available -want -filter:retweets AND -filter:replies AND -filter:links AND -filter:media AND -filter:images AND -filter:twimg"
            new_search = product + " OR " + keywords + " OR " + company +" -sale -available -want -filter:retweets AND -filter:replies AND -filter:links AND -filter:media AND -filter:images AND -filter:twimg"
            print(new_search)
            # contains fetched tweets
            tweets = tw.Cursor(api.search_tweets,q=new_search,
                            lang="en",tweet_mode='extended',
                            ).items(500)

            # print("tweets", tweets)

            # extracting required fields from fetched tweets
            all_tweets = [[tweet.full_text, tweet.created_at.year, tweet.created_at.month, tweet.created_at.day, tweet.created_at.time().hour, tweet.created_at.time().minute, tweet.created_at.time().second] for tweet in tweets]

            print("all", all_tweets)
            
            if(len(all_tweets) == 0):
                return []
    
            # print("all fetched tweets", all_tweets)

            # making a new dataframe
            pd.set_option('display.max_colwidth', None)
            tweet_text = pd.DataFrame(data=all_tweets, 
                                columns=['tweet','year','month','day','hour','minute','second'])

            # print("tweets", tweet_text)


            # pre-processing
            tweet_text['tweet'] =tweet_text['tweet'].apply(lower_case)
            tweet_text['tweet'] =tweet_text['tweet'].apply(remove_multiple)
            tweet_text['tweet'] =tweet_text['tweet'].apply(remove_single_char)
            tweet_text['tweet'] =tweet_text['tweet'].apply(remove_special_characters)
            tweet_text['tweet'] =tweet_text['tweet'].apply(remove_square_brackets)
            tweet_text['tweet'] =tweet_text['tweet'].apply(remove_urls)
            tweet_text['tweet'] =tweet_text['tweet'].apply(remove_username)
            tweet_text['tweet'] =tweet_text['tweet'].apply(replace_contractions)
            tweet_text['tweet'] =tweet_text['tweet'].apply(replace_negation)
            tweet_text['tweet'] =tweet_text['tweet'].apply(remove_stopwords)

            return tweet_text
        except Exception as e:
            print(e)
            time.sleep(60)
            continue

def find_sentiment(cleaned_tweets):

    # load MNB model
    loaded_model = pickle.load(open('./model/model.sav','rb'))

    # load tfidfVectorizer
    vectorizer = pickle.load(open('./model/tfidfVectorizer.pickle','rb'))

    # print('cleaned',cleaned_tweets)
    # transform the cleaned fetched tweets into numeric form
    tweet = vectorizer.transform(cleaned_tweets['tweet'])

    # perform prediction -> positive, negative, neutral
    prediction = loaded_model.predict(tweet)
    
    # print(prediction)

    return prediction


def get_counts(values):
    content, count = numpy.unique(values, return_counts=True)
    data = dict(zip(content, count))

    return data

def hour_counts(hourCount):
    receivedKeys = []
    for k in hourCount:
        receivedKeys.append(k)
    print('recived_key', receivedKeys)

    missingKeys = list({0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23} - set(receivedKeys))
    print('missed_keys',missingKeys)

    for k in missingKeys:
        hourCount[k] = 0
    
    return hourCount



# api is called when user enters search keywords
@api_view(["POST",])
@permission_classes([IsAuthenticated])
def search_keywords(request):
    print("starting search...")
    # print('user in search', request.headers.keys())
    user = request.user
    # user.is_registered = True
    # user.save()

   
    data ={}
    data["product_name"] = request.data['product_name']
    data["company_name"] = request.data['company_name']
    data["keywords"] = request.data['keywords']

    print("data.....",data)
    product_name = data["product_name"] 

   
    # calling fetch_tweets to get real time cleaned tweets
    cleaned_tweets = fetch_tweets(data["product_name"], data["company_name"], data["keywords"])

    if(len(cleaned_tweets) == 0):
        print("no tweets.........")
        return Response({
            "msg":"Error in fetching data. Try some other keywords.",
        }, status=500)
    else:
        graphDataAvailable = False
   
        # output sentiments
        prediction = find_sentiment(cleaned_tweets)

        # new DF containing sentiments instead of tweets
        lists = list(zip(prediction,cleaned_tweets["year"],cleaned_tweets["month"],cleaned_tweets["day"],cleaned_tweets["hour"],cleaned_tweets["minute"],cleaned_tweets["second"]))
        finalDf = pd.DataFrame(lists, columns=["sentiment","year","month","day","hour","minute","second"])

        print("final..", finalDf)
        enddate = datetime.datetime(int(finalDf["year"].iloc[0]), int(finalDf["month"].iloc[0]), int(finalDf["day"].iloc[0]), int(finalDf["hour"].iloc[0]) ,int(finalDf["minute"].iloc[0]) ,int(finalDf["second"].iloc[0]))
        startdate = datetime.datetime(int(finalDf["year"].iloc[-1]), int(finalDf["month"].iloc[-1]), int(finalDf["day"].iloc[-1]), int(finalDf["hour"].iloc[-1]) ,int(finalDf["minute"].iloc[-1]) ,int(finalDf["second"].iloc[-1]))
        print("starting..",startdate)
        print("ending...", enddate)

        # separate DFs for each sentiments
        positiveDf = finalDf[finalDf["sentiment"] == "Positive"]
        negativeDf = finalDf[finalDf["sentiment"] == "Negative"]
        neutralDf = finalDf[finalDf["sentiment"] == "Neutral"]

        # showing data in graph  (1 day before)
        dayYesterday = datetime.date.today() - datetime.timedelta(days=1)
        date = dayYesterday
        dayYesterday = dayYesterday.day
        
        # print('yesterday', dayYesterday, date)


        positiveDfmonth = positiveDf[positiveDf["month"] == datetime.date.today().month]
        negativeDfmonth = negativeDf[negativeDf["month"] == datetime.date.today().month]
        neutralDfmonth = neutralDf[neutralDf["month"] == datetime.date.today().month]

        positiveDfday = positiveDfmonth[positiveDfmonth["day"] == dayYesterday]
        negativeDfday = negativeDfmonth[negativeDfmonth["day"] == dayYesterday]
        neutralDfday = neutralDfmonth[neutralDfmonth["day"] == dayYesterday]

        # print('p', positiveDfday, len(positiveDfday))
        # print('n', negativeDfday, len(negativeDfday))
        # print('neu', neutralDfday, len(negativeDfday))

        # showing data in graph of the same day
        if(len(positiveDfday) == 0 or len(negativeDfday) == [] or len(neutralDfday) == []):
            dayToday = datetime.date.today()
            date = dayToday
            dayToday = dayToday.day
            print('today', dayToday, date)

            positiveDfday = positiveDfmonth[positiveDfmonth["day"] == dayToday]
            negativeDfday = negativeDfmonth[negativeDfmonth["day"] == dayToday]
            neutralDfday = neutralDfmonth[neutralDfmonth["day"] == dayToday]

        # print('p', positiveDfday)
        # print('n', negativeDfday)
        # print('neu', neutralDfday)

 
        if(len(positiveDfday) == 0 and len(negativeDfday) == 0 and len(neutralDfday) == 0):
            graphDataAvailable = False
        else:
            graphDataAvailable = True


        
        sentimentData = get_counts(prediction)
        # yearCount = get_counts(cleaned_tweets["year"])
        # monthCount = get_counts(cleaned_tweets["month"])
        # dayCount = get_counts(cleaned_tweets["day"])
        hourCountPositive = get_counts(positiveDfday["hour"])
        hourCountNegative = get_counts(negativeDfday["hour"])
        hourCountNeutral = get_counts(neutralDfday["hour"])


        hourCountPositive = hour_counts(hourCountPositive)
        hourCountNegative = hour_counts(hourCountNegative)
        hourCountNeutral = hour_counts(hourCountNeutral)

        # print('pos', hourCountPositive, 'neg', hourCountNegative, 'neutral', hourCountNeutral)
    
        hourCountPosUpdated = {}
        hourCountNegUpdated = {}
        hourCountNeutralUpdated = {}

        for i in range(0,23,2):
            hourCountPosUpdated[i] = hourCountPositive[i] + hourCountPositive[i+1]
            hourCountNegUpdated[i] = hourCountNegative[i] + hourCountNegative[i+1]
            hourCountNeutralUpdated[i] = hourCountNeutral[i] + hourCountNeutral[i+1]
        
        # print('pos..', hourCountPosUpdated, 'neg..', hourCountNegUpdated, 'neutral..', hourCountNeutralUpdated)

        hour_key = [0,2,4,6,8,10,12,14,16,18,20,22]
        # hour_key = ["0:00 A.M","2:00 A.M","4:00 A.M.","6:00 A.M","8:00 A.M","10:00 A.M","12:00 P.M","2:00 P.M","4:00 P.M","6:00 P.M","8:00 P.M","10:00 P.M"]
        hourData = []

        for key in hour_key:
            # print(key)
            if(key <= 10):
                keyHour = str(key) + ":00 A.M."
            elif(key == 12):
                keyHour = str(key) + ":00 P.M."
                # print("Here", keyHour)
            elif(key > 12):
        
                keyHour = int(key) - int(12)
                keyHour = str(keyHour) + ":00 P.M."
            hourData.append({"time":keyHour,"positive":hourCountPosUpdated[key],"negative":hourCountNegUpdated[key], "neutral":hourCountNeutralUpdated[key]})
                
        # print('hourData',hourData)
        

        requiredKeys = ["Positive", "Negative", "Neutral"]
        receivedKeys = []
        for key in sentimentData:
            receivedKeys.append(key)
            
        # print(receivedKeys)
        missingKeys = list(set(requiredKeys)-set(receivedKeys))
        # print(len(missingKeys))

        if(missingKeys):
            # print("there are missing keys")
            for i in range(len(missingKeys)):
                sentimentData[missingKeys[i]] = 0
        
        sentimentData = dict(sorted(sentimentData.items()))

        tweetData = TweetAnalysis(
            user = request.user,
            sentiment_data = sentimentData,
            hour_data = hourData,
            product_name = data["product_name"],
            fetched_date = date,
            graph_data_available = graphDataAvailable,
            start_date = startdate,
            end_date = enddate
        )

        # print('data saved', sentimentData)

        tweetData.save()

        return Response({
            "msg": "From search",
            "is_registered": user.is_registered,
            "data": data,
            "predicted_data":prediction,
            "sentiment_data": sentimentData,
            "hour_data": hourData,
            "product_name": product_name,
            "graphDataAvailable": graphDataAvailable
        })

@api_view(["GET",])
@permission_classes([IsAuthenticated])
def getSentimentData(request):
    user = request.user
    try:
        tweetData = TweetAnalysis.objects.filter(user=user).order_by('-id')[0]
        print('tweet', user, tweetData)
    except TweetAnalysis.DoesNotExist:
        tweetData = None
   
    if(tweetData):
        json_data = ast.literal_eval(tweetData.sentiment_data)
        print('json data',(json_data))
        outputSentiment = []

        for key in json_data:
            print(key, json_data[key])
            outputSentiment.append({"sentiment":key,"value":json_data[key]})
        
        print(outputSentiment)

        hour_data_json = ast.literal_eval(tweetData.hour_data)

        data = {
            "user" : tweetData.user.id,
            "sentiment_data": (json_data),
            "output_sentiment": outputSentiment,
            "hour_data": hour_data_json,
            "product_name": tweetData.product_name,
            "fetched_date": tweetData.fetched_date,
            "graph_data_available": tweetData.graph_data_available,
            "start_date": tweetData.start_date,
            "end_date": tweetData.end_date
        }
        
        # print('data.....', data)
        return Response({
            "data":data,
            "msg":"Sentiment analysis Data"
        })
    else:
        return Response({
            "message":"Has not searched yet"
        }, status = 404)
    

@api_view(["POST","GET",])
def model_operation(request):
    return Response({
        "data":"done"
    })


import praw
import string
import nltk
#nltk.download('stopwords')
#import stopwords
import pandas as pd
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import emoji
pd.set_option('display.max_colwidth', None)

#input url

def urllink(url):
    reddit = praw.Reddit(client_id='', client_secret='',    user_agent='yolo app')
    url = str(url)
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=0)
    return submission


#put all comments in a dataframe
def pdallcomments(submission):
    df_allcomments=pd.DataFrame(data=[allcomments.body for allcomments in submission.comments.list()])
    df_allcomments=df_allcomments.rename(columns={0:'content'})

    list1=[str(i).lower() for i in df_allcomments['content']]
    tokenizer = RegexpTokenizer(r"\w+")
    stop_words = set(stopwords.words('english'))
    score_list1=[]
    for k in range(len(list1)):
        new_words = tokenizer.tokenize(list1[k])
        #filtered_sentence = [w for w in new_words if not w in stop_words]
        #filtered_sentence=' '.join(filtered_sentence)
        #analyzer = SentimentIntensityAnalyzer()
        #score_list.append(analyzer.polarity_scores(filtered_sentence))
        new_words2 = ' '.join(new_words)
        analyzer = SentimentIntensityAnalyzer()
        score_list=analyzer.polarity_scores(new_words2)
        score_list1.append(score_list)
    df_allcomments['score']=score_list1
    return df_allcomments

submission=urllink(input('please input an url:'))
pdallcomments(submission).to_csv('reddit_comments_sentiment.csv')
print('exported csv file')

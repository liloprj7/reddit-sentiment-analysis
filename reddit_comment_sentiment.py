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

# step0: download hot posts
def urlsubreddit(subreddit_search):
    reddit = praw.Reddit(client_id='', client_secret='', user_agent='')
    top_list=[]
    for submission in reddit.subreddit(subreddit_search).hot(limit=20):
        top_list.append([submission.title,submission.id])
    df_subreddit_top=pd.DataFrame(data=top_list)
    df_subreddit_top=df_subreddit_top.rename(columns={0:'PostTitle',1:'PostID'})
    #return df_subreddit_top
    return df_subreddit_top['PostID']


# step1: get comments by inputting single post ID
# step2: put all comments in a dataframe
# step3: run sentiment analysis
def urllink(postid):
    reddit = praw.Reddit(client_id='', client_secret='', user_agent='')
    submission_postid = reddit.submission(id=postid)
    submission_postid.comments.replace_more(limit=0)
    df_allcomments=pd.DataFrame(data=[allcomments.body for allcomments in submission_postid.comments.list()])
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

submission=urlsubreddit(input('please input name of a subreddit:'))
print('top hot posts are shown below: ')
print(submission)

for i in range(len(submission)):
    try:
        result=urllink(submission[i])
        result.to_csv('result'+str(i)+'.csv')
        print(str(i)+' is ready!')
    except:
        print("something wrong")
        pass


import twitter
import json, io
# XXX: Go to http://dev.twitter.com/apps/new to create an app and get values
# for these credentials, which you'll need to provide in place of these
# empty string values that are defined as placeholders.
# See https://dev.twitter.com/docs/auth/oauth for more information
# on Twitter's OAuth implementation.
CONSUMER_KEY = '21QS3az7FnS6hLQNbImgw1YkI'
CONSUMER_SECRET = 'VZ2dF0TiOjClAYirMfvMegXOyXS3uC966ivqhMIKpq2khghU01'
OAUTH_TOKEN = '2792072203-URihh1e0eOxf8UYTDkfKsTLC5QQtknqOZ54tdvi'
OAUTH_TOKEN_SECRET = 'NvjxqtWCMIPAMSTQfpmE9o4L1Gw54BdjM4FsCDG9Ui8YQ'
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)
# Nothing to see by displaying twitter_api except that it's now a
# defined variable
print twitter_api


#----------------------------------------------
# select "Alibaba" as interested topic, sample a collection of tweets about this
# topic in real time

q = '#Alibaba'
count = 500
search_results = twitter_api.search.tweets(q=q, count=count)

# save the results to json file 
def save_json(filename, data):
    with io.open('data/{0}.json'.format(filename),'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(data, ensure_ascii=False)))
save_json(q, search_results)


#----------------------------------------------
# frequencies of the words being used in these tweets
statuses = search_results['statuses']
status_texts = [ status['text'] for status in statuses ]

words = [ w for t in status_texts 
                for w in t.split() ]

from collections import Counter

c = Counter(words)
print c.most_common()

# Plot a table of the top 30 words with their counts
from prettytable import PrettyTable
pt = PrettyTable(field_names=['Word', 'Count'])
c = Counter(words)
[ pt.add_row(kv) for kv in c.most_common()[:30] ]
pt.align['Word'], pt.align['Count'] = 'l', 'r' # Set column alignment
print pt


#----------------------------------------------
# plot a table of the top 10 tweets that are the most popular among the collection
# (the tweets with the largest number of retweet counts).
screen_names = [ user_mention['screen_name'] 
                 for status in statuses
                     for user_mention in status['entities']['user_mentions'] ]

hashtags = [ hashtag['text'] 
             for status in statuses
                 for hashtag in status['entities']['hashtags'] ]

words = [ w 
          for t in status_texts 
              for w in t.split() ]

retweets = [
# Store out a tuple of these three values ...
           (status['retweet_count'],
            status['retweeted_status']['user']['screen_name'],
            status['text'])
# ... for each status ...
           for status in statuses
# ... so long as the status meets this condition.
               if status.has_key('retweeted_status')
]
pt = PrettyTable(field_names=['Count', 'Screen Name', 'Text'])
[ pt.add_row(row) for row in sorted(retweets, reverse=True)[:10] ]
pt.max_width['Text'] = 50
pt.align= 'l'
print pt


#----------------------------------------------
#  plot a table of the top 10 hashtags, top 10 user mentions that are 
#  the most popular in the collection of tweets.
for label, data in (('Screen Name', screen_names),('Hashtag', hashtags)):
    pt = PrettyTable(field_names=[label, 'Count'])
    c = Counter(data)
    [ pt.add_row(kv) for kv in c.most_common()[:10] ]
    pt.align[label], pt.align['Count'] = 'l', 'r' # Set column alignment
    print pt
    
    

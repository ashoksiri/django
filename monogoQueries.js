db.getCollection('video').aggregate([
{$match:{searchKey:'narendramodi'}},
{$project:{'id':'$searchKey',
    'statistics':'$statistics',
    'contentDetails':'$contentDetails',
    live: {$cond: { if: { $gt: [ "$liveStreamingDetails", {} ] }, then: 1, else: 0 }}
}},   
{$group:{'_id':'$id','viewCount':{$sum:'$statistics.viewCount'},
'likeCount':{$sum:'$statistics.likeCount'},
'dislikeCount':{$sum:'$statistics.dislikeCount'},
'commentCount':{$sum:'$statistics.commentCount'},
'totalDuration':{$sum:'$contentDetails.duration'},
'liveVideos' : {$sum:'$live'}
}}
])

-- category wise

db.getCollection('video').aggregate([
{$match:{searchKey:'narendramodi'}},
{$group:{'_id':'$snippet.categoryId','count':{$sum:1}}},
])

--channel wise

db.getCollection('video').aggregate([
{$match:{searchKey:'Fox News Live'}},
{$group:{'_id':'$channelId','count':{$sum:1}}},
])

-- sentiment for comments

db.getCollection('video').aggregate([
    { "$match":{ "comments.0": { "$exists": true }}}, 
    {"$project": {'searchKey':'$searchKey','comment':'$comments' }}, 
    {"$unwind": "$comment" },
    {'$group':{'_id':'$comment.polarity.key','count':{$sum:1}}}  
] )

--- sentiment for videos

db.getCollection('video').aggregate([
    {'$group':{'_id':'$polarity.key','count':{$sum:1}}}  
] )

--------Video Scores

db.getCollection('video').aggregate([
{$match:{
    'searchKey':'narendramodi',
    'snippet.publishedAt':{'$lte': ISODate('2017-10-13'),'$gte': ISODate('2017-10-01')}}
 },
 {'$project':{
     'searchKey':'$searchKey',
     'fair':{'$cond':[{'$and':[{'$gt':[ "$polarity.value", 0]},{'$lt': [ "$polarity.value",0.25]}]},1,0]},
     'good':{'$cond':[{'$and':[{'$gt':[ "$polarity.value", 0.25]},{'$lt': [ "$polarity.value",0.5]}]},1,0]},
     'excellent':{'$cond':[{'$and':[{'$gt':[ "$polarity.value", 0.5]},{'$lt': [ "$polarity.value",1]}]},1,0]},
     'bad':{'$cond':[{'$and':[{'$gt':[ "$polarity.value", -0.5]},{'$lt': [ "$polarity.value",0]}]},1,0]},
     'verybad':{'$cond':[{'$and':[{'$gt':[ "$polarity.value", -1]},{'$lt': [ "$polarity.value",-0.5]}]},1,0]},
     'other':{'$cond': [ { '$eq': [ "$polarity.value", 0 ] }, 1, 0 ]},
     }},
     {'$group':{
         '_id':'$searchKey',
         'faircount':{'$sum':'$fair'},
         'goodcount':{'$sum':'$good'},
         'excellentcount':{'$sum':'$excellent'},
         'badcount':{'$sum':'$bad'},
         'verybadcount':{'$sum':'$verybad'},
         'othercount':{'$sum':'$other'}}}
])

/* Country wise count */


db.getCollection('tweet').aggregate([
    {$match:{'place.country':{$exists:true}}},
    {$project:{'country':'$place.country'}},
    {$group:{_id:'$country',count:{$sum:1}}}
    ])
	
/* Sentiment wise count */

db.getCollection('tweet').aggregate([
     {'$group':{'_id':'$polarity.key','count':{$sum:1}}}  
] )

/* Tweets by user mentions */

db.getCollection('tweet').aggregate([
    {$match:{'searchKey':'narendramodi','entities.user_mentions':{$exists:true,$elemMatch:{'name':'Loneranger'}}}}
    
])

/* Tweets by hash Tags */

db.getCollection('tweet').aggregate([
    {$match:{'searchKey':'narendramodi','entities.hashtags':{$exists:true,$elemMatch:{'text':'DigitalIndia'}}}}
    
])

/* trending Hash Tags */


db.getCollection('tweet').aggregate([
    {$match:{'searchKey':'narendramodi',
        'entities.hashtags.0':{$exists:true},
        'created_at':{'$lte': ISODate('2017-10-05'),'$gte': ISODate('2017-10-04')}}},
    {$unwind:'$entities.hashtags'},
    {$group:{_id:'$entities.hashtags.text','count':{$sum:1}}},
    {$sort:{'count':-1}},
    {$limit:15}
])

/** Trending Retweets **/


db.getCollection('tweet').aggregate([
    {$match:{'searchKey':'narendramodi',
     'retweet_count':{$ne:0},
    'created_at':{'$lte': ISODate('2017-10-05'),'$gte': ISODate('2017-10-04')}}},
    {$sort:{'retweet_count':-1}},
    {$limit:15}
])

/* tweet Statistics */

db.tweet.aggregate([   
        {
         '$match':{'searchKey':'narendramodi',
         'created_at':{'$lte': ISODate('2017-10-05'),'$gte': ISODate('2017-10-04')}}
        },
        {'$group':{'_id':'tweets',
            "tweetCount": {"$sum": {'$cond': [ { '$eq': [ "$retweet_count", 0 ] }, 1, 0 ]}},
            "retweetCount": {"$sum": {'$cond': [ { '$ne': [ "$retweet_count", 0 ] }, 1, 0 ]}},
            "mentionsCount": {"$sum": {'$cond': [ { '$ne': [ {'$size':'$entities.user_mentions'}, 0 ] }, 1, 0 ]}},
            'hashTagsCount': {"$sum": {'$cond': [ { '$ne': [ {'$size':'$entities.hashtags'}, 0 ] }, 1, 0 ]}},
            'users':{'$addToSet':'$user.screen_name'},
        }},
        {'$project':{
            'tweets':'$tweetCount',
            'retweets':'$retweetCount',
            'mentions':'$mentionsCount',
            'hashTags': '$hashTagsCount',
            'authors':{$size:'$users'}
            }}
    ]
)

/** Unique Users **/

db.getCollection('tweet').aggregate([
    {$match:{'searchKey':'narendramodi',
     'created_at':{'$lte': ISODate('2017-10-05'),'$gte': ISODate('2017-10-04')}}},
     {$group: {_id: null, uniqueValues: {$addToSet: "$user.screen_name"}}},
     {$project:{uniqueCustomerCount:{$size:"$uniqueValues"}} } 
  
])
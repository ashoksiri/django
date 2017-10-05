from mongoengine import Document, EmbeddedDocument, fields


class Localized(EmbeddedDocument):
    title = fields.StringField(null=True)
    description = fields.StringField(null=True)


class Polarity(EmbeddedDocument):
    key = fields.StringField(null=True)
    value = fields.FloatField(null=True)

    def __dict__(self):
        return {'key': self.key, 'value': self.value}


class DefaultThumbnail(EmbeddedDocument):
    url = fields.StringField(null=True)
    width = fields.IntField(null=True)
    height = fields.IntField(null=True)


class Thumbnail(EmbeddedDocument):
    default = fields.EmbeddedDocumentField(DefaultThumbnail, null=True)


class TopicDetails(EmbeddedDocument):
    topicIds = fields.ListField(null=True)
    relevantTopicIds = fields.ListField(null=True)
    topicCategories = fields.ListField(null=True)


class TopLevelCommentSnippet(EmbeddedDocument):
    authorDisplayName = fields.StringField(null=True)
    authorProfileImageUrl = fields.StringField(null=True)
    authorChannelUrl = fields.StringField(null=True)
    authorChannelId = fields.DictField(null=True)
    channelId = fields.StringField(null=True)
    videoId = fields.StringField(null=True)
    textDisplay = fields.StringField(null=True)
    textOriginal = fields.StringField(null=True)
    textOriginalParsed = fields.StringField(null=True)
    parentId = fields.StringField(null=True)
    canRate = fields.BooleanField(null=True)
    viewerRating = fields.StringField(null=True)
    likeCount = fields.LongField(null=True)
    moderationStatus = fields.StringField(null=True)
    publishedAt = fields.DateTimeField(null=True)
    updatedAt = fields.DateTimeField(null=True)

    def __dict__(self):
        return {
            'authorDisplayName': self.authorDisplayName,
            'authorProfileImageUrl': self.authorProfileImageUrl,
            'authorChannelUrl': self.authorChannelUrl,
            'authorChannelId': self.authorChannelId,
            'channelId': self.channelId,
            'videoId': self.videoId,
            'textDisplay': self.textDisplay,
            'textOriginal': self.textOriginal,
            'textOriginalParsed': self.textOriginalParsed,
            'parentId': self.parentId,
            'canRate': self.canRate,
            'viewerRating': self.viewerRating,
            'likeCount': self.likeCount,
            'moderationStatus': self.moderationStatus,
            'publishedAt': self.publishedAt,
            'updatedAt': self.updatedAt
        }


class TopLevelComment(EmbeddedDocument):
    id = fields.StringField()
    snippet = fields.EmbeddedDocumentField(TopLevelCommentSnippet, null=True)

    def __dict__(self):
        return {'id': self.id,
                'snippet': self.snippet.__dict__()}


class CommentSnippet(EmbeddedDocument):
    channelId = fields.StringField()
    videoId = fields.StringField()
    topLevelComment = fields.EmbeddedDocumentField(TopLevelComment)
    canReply = fields.BooleanField(null=True)
    totalReplyCount = fields.LongField(null=True)
    isPublic = fields.BooleanField(null=True)

    def __dict__(self):
        return {'channelId': self.channelId,
                'videoId': self.videoId,
                'topLevelComment': self.topLevelComment.__dict__(),
                'canReply': self.canReply,
                'totalReplyCount': self.totalReplyCount,
                'isPublic': self.isPublic}


class CommentReplay(EmbeddedDocument):
    id = fields.StringField(null=True)
    snippet = fields.EmbeddedDocumentField(CommentSnippet, null=True)

    def __dict__(self):
        return {'id': self.id,
                'snippet': self.snippet.__dict__()}


class Replies(EmbeddedDocument):
    comments = fields.EmbeddedDocumentListField(CommentReplay, null=True)


class Comment(EmbeddedDocument):
    commentId = fields.StringField()
    snippet = fields.EmbeddedDocumentField(CommentSnippet)
    # replies = fields.EmbeddedDocumentField(CommentReplay,null=True)
    polarity = fields.EmbeddedDocumentField(Polarity)

    def __dict__(self):
        return {'commentId': self.commentId,
                'snippet': self.snippet.__dict__(),
                # 'replies':self.replies.__dict__(),
                'polarity': self.polarity.__dict__()}


class ContentOwnerDetails(EmbeddedDocument):
    contentOwner = fields.StringField(null=True)
    timeLinked = fields.DateTimeField(null=True)


class RelatedPlayLists(EmbeddedDocument):
    likes = fields.StringField(null=True)
    favorites = fields.StringField(null=True)
    uploads = fields.StringField(null=True)
    watchHistory = fields.StringField(null=True)
    watchLater = fields.StringField(null=True)


class ChannelContentDetails(EmbeddedDocument):
    relatedPlaylists = fields.EmbeddedDocumentField(RelatedPlayLists, null=True)


class BrandingChannel(EmbeddedDocument):
    title = fields.StringField(null=True)
    description = fields.StringField(null=True)
    keywords = fields.StringField(null=True)
    defaultTab = fields.StringField(null=True)
    trackingAnalyticsAccountId = fields.StringField(null=True)
    moderateComments = fields.BooleanField(null=True)
    showRelatedChannels = fields.BooleanField(null=True)
    showBrowseView = fields.BooleanField(null=True)
    featuredChannelsTitle = fields.StringField(null=True)
    featuredChannelsUrls = fields.ListField(null=True)
    unsubscribedTrailer = fields.StringField(null=True)
    profileColor = fields.StringField(null=True)
    defaultLanguage = fields.StringField(null=True)
    country = fields.StringField()


class BrandingSettings(EmbeddedDocument):
    channel = fields.EmbeddedDocumentField(BrandingChannel, null=True)


class ChannelStatus(EmbeddedDocument):
    privacyStatus = fields.StringField(null=True)
    isLinked = fields.BooleanField(null=True)
    longUploadsStatus = fields.StringField(null=True)


class ChannelStatistics(EmbeddedDocument):
    viewCount = fields.LongField(null=True)
    commentCount = fields.LongField(null=True)
    subscriberCount = fields.LongField(null=True)
    hiddenSubscriberCount = fields.BooleanField(null=True)
    videoCount = fields.LongField(null=True)


class ChannelSnippet(EmbeddedDocument):
    title = fields.StringField()
    description = fields.StringField(null=True)
    customUrl = fields.StringField(null=True)
    publishedAt = fields.DateTimeField()
    thumbnails = fields.EmbeddedDocumentField(Thumbnail, null=True)
    defaultLanguage = fields.StringField(null=True)
    localized = fields.EmbeddedDocumentField(Localized, null=True)
    country = fields.StringField(null=True)


class Channel(EmbeddedDocument):
    channelId = fields.StringField()
    snippet = fields.EmbeddedDocumentField(ChannelSnippet, null=True)
    contentDetails = fields.EmbeddedDocumentField(ChannelContentDetails, null=True)
    statistics = fields.EmbeddedDocumentField(ChannelStatistics, null=True)
    topicDetails = fields.EmbeddedDocumentField(TopicDetails, null=True)
    status = fields.EmbeddedDocumentField(ChannelStatus, null=True)
    brandingSettings = fields.EmbeddedDocumentField(BrandingSettings, null=True)
    contentOwnerDetails = fields.EmbeddedDocumentField(ContentOwnerDetails, null=True)


class VideoLiveStreamingDetails(EmbeddedDocument):
    actualStartTime = fields.DateTimeField(null=True)
    actualEndTime = fields.DateTimeField(null=True)
    scheduledStartTime = fields.DateTimeField(null=True)
    scheduledEndTime = fields.DateTimeField(null=True)
    concurrentViewers = fields.LongField(null=True)
    activeLiveChatId = fields.StringField(null=True)


class VideoStatistics(EmbeddedDocument):
    viewCount = fields.LongField(null=True)
    likeCount = fields.LongField(null=True)
    dislikeCount = fields.LongField(null=True)
    favoriteCount = fields.LongField(null=True)
    commentCount = fields.LongField(null=True)


class VideoStatus(EmbeddedDocument):
    uploadStatus = fields.StringField(null=True)
    failureReason = fields.StringField(null=True)
    rejectionReason = fields.StringField(null=True)
    privacyStatus = fields.StringField(null=True)
    publishAt = fields.DateTimeField(null=True)
    license = fields.StringField(null=True)
    embeddable = fields.BooleanField(null=True)
    publicStatsViewable = fields.BooleanField(null=True)


class RegionRestriction(EmbeddedDocument):
    allowed = fields.ListField(null=True)
    blocked = fields.ListField(null=True)


class ContentRating(EmbeddedDocument):
    cbfcRating = fields.StringField(null=True)
    ytRating = fields.StringField(null=True)


class VideoContentDetails(EmbeddedDocument):
    duration = fields.IntField(null=True)
    dimention = fields.StringField(null=True)
    definition = fields.StringField(null=True)
    caption = fields.StringField(null=True)
    licensedContent = fields.BooleanField(null=True)
    regionRestriction = fields.EmbeddedDocumentField(RegionRestriction, null=True)
    contentRating = fields.EmbeddedDocumentField(ContentRating, null=True)
    projection = fields.StringField(null=True)
    hasCustomThumbnail = fields.BooleanField(null=True)


class VideoSnippeet(EmbeddedDocument):
    publishedAt = fields.DateTimeField()
    channelId = fields.StringField()
    title = fields.StringField()
    description = fields.StringField(null=True)
    descriptionParsed = fields.StringField(null=True)
    thumbnails = fields.EmbeddedDocumentField(Thumbnail, null=True)
    channelTitle = fields.StringField(null=True)
    tags = fields.ListField(null=True)
    categoryId = fields.StringField(null=True)
    liveBroadcastContent = fields.StringField(null=True)
    defaultLanguage = fields.StringField(null=True)
    localized = fields.EmbeddedDocumentField(Localized, null=True)
    defaultAudioLanguage = fields.StringField(null=True)


class Video(Document):
    videoId = fields.StringField()
    channelId = fields.StringField()
    title = fields.StringField()
    snippet = fields.EmbeddedDocumentField(VideoSnippeet)
    contentDetails = fields.EmbeddedDocumentField(VideoContentDetails)
    status = fields.EmbeddedDocumentField(VideoStatus)
    statistics = fields.EmbeddedDocumentField(VideoStatistics)
    topicDetails = fields.EmbeddedDocumentField(TopicDetails, null=True)
    liveStreamingDetails = fields.EmbeddedDocumentField(VideoLiveStreamingDetails, null=True, default={})
    polarity = fields.EmbeddedDocumentField(Polarity)
    channel = fields.EmbeddedDocumentField(Channel)
    comments = fields.EmbeddedDocumentListField(Comment)
    sourceType = fields.StringField(default="youtube")
    searchKey = fields.StringField(max_length=100)
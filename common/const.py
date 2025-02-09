import re
import os
import configparser
version = '1.3.0'

# const
twtCount = 100  # 推主媒体批量爬取时, 每次api抓取的推文计数
url_args_help = \
    '''tw url to gather media, must be like:
    1. https://twitter.com/***/status/***
    2. https://twitter.com/***(/media) (user page, *** is user_id)
    # 2. will gather all media files of user's tweets'''
conf = configparser.RawConfigParser()
conf_path = os.path.expanduser('~') + '/tw_media_downloader.conf'

# api auth token
authorization = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"

# context/config
context = {
    'proxy': {},  # 可拓展支持socks代理和密码验证代理，详情看https://www.python-httpx.org/advanced/#socks 暂时没需求先不做
    'headers': {'authorization': authorization, 'Cookie': '', 'User-Agent': ''},
    'dl_path': './twitter_media_download',
    'log_path': './log',
    'updateInfo': {'LastCheckDate': '', 'tagName': '', 'name': ''},
    'concurrency': 8,
    'type': 'photo&animated_gif&video&full_text',
    'quoted': True,
    'retweeted': True
}


def setContext(key, value):
    context[key] = value


def getContext(key=None):
    if key:
        return context[key]
    else:
        return context


# api url
hostUrl = 'https://api.twitter.com/1.1/guest/activate.json'
singlePageApi = 'https://twitter.com/i/api/graphql/AkHczoaCocpQ_XO0hVM_-Q/TweetDetail'
userMediaApi = 'https://twitter.com/i/api/graphql/ngkNnhoHF01FpsMjb57TLA/UserMedia'
userHomeApi = 'https://twitter.com/i/api/graphql/edn8-AOJHq7gBM6OPpWT_g/UserTweets'
userSearchApi = 'https://api.twitter.com/2/search/adaptive.json'
userInfoApi = 'https://twitter.com/i/api/graphql/Vf8si2dfZ1zmah8ePYPjDQ/UserByScreenNameWithoutResults'
checkUpdateApi = 'https://api.github.com/repos/mengzonefire/twitter-media-downloader/releases/latest'

# api parameter
singlePageApiPar = '{{"focalTweetId":"{}","with_rux_injections":false,"includePromotedContent":false,"withCommunity":false,"withQuickPromoteEligibilityTweetFields":false,"withBirdwatchNotes":false,"withSuperFollowsUserFields":true,"withDownvotePerspective":false,"withReactionsMetadata":false,"withReactionsPerspective":false,"withSuperFollowsTweetFields":true,"withVoice":true,"withV2Timeline":true}}'
singlePageApiPar2 = '{"responsive_web_graphql_timeline_navigation_enabled":false,"unified_cards_ad_metadata_container_dynamic_card_content_query_enabled":true,"dont_mention_me_view_api_enabled":true,"responsive_web_uc_gql_enabled":false,"vibe_api_enabled":true,"responsive_web_edit_tweet_api_enabled":false,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":false,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":false,"interactive_text_enabled":true,"responsive_web_text_conversations_enabled":false,"responsive_web_enhance_cards_enabled":false}'
userMediaApiPar = '{{"userId":"{}","count":{},{}"includePromotedContent":false,"withSuperFollowsUserFields":false,"withDownvotePerspective":false,"withReactionsMetadata":false,"withReactionsPerspective":false,"withSuperFollowsTweetFields":false,"withClientEventToken":false,"withBirdwatchNotes":false,"withVoice":false,"withV2Timeline":true}}'
userMediaApiPar2 = '{"responsive_web_like_by_author_enabled":false,"dont_mention_me_view_api_enabled":false,"interactive_text_enabled":false,"responsive_web_uc_gql_enabled":false,"responsive_web_edit_tweet_api_enabled":false}'
userHomeApiPar = '{{"userId":"{}","count":{},{}"includePromotedContent":false,"withQuickPromoteEligibilityTweetFields":false,"withSuperFollowsUserFields":false,"withDownvotePerspective":false,"withReactionsMetadata":false,"withReactionsPerspective":false,"withSuperFollowsTweetFields":false,"withVoice":false,"withV2Timeline":true}}'
userHomeApiPar2 = '{"responsive_web_twitter_blue_verified_badge_is_enabled":true,"verified_phone_label_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":false,"view_counts_public_visibility_enabled":true,"view_counts_everywhere_api_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_uc_gql_enabled":false,"vibe_api_enabled":true,"responsive_web_edit_tweet_api_enabled":false,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":false,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":false,"interactive_text_enabled":true,"responsive_web_text_conversations_enabled":false,"responsive_web_enhance_cards_enabled":false,"unified_cards_ad_metadata_container_dynamic_card_content_query_enabled":true}'
userSearchApiPar = '{{"include_profile_interstitial_type":1,"include_blocking":1,"include_blocked_by":1,"include_followed_by":1,"include_want_retweets":1,"include_mute_edge":1,"include_can_dm":1,"include_can_media_tag":1,"include_ext_has_nft_avatar":1,"include_ext_is_blue_verified":1,"include_ext_verified_type":1,"skip_status":1,"cards_platform":"Web-12","include_cards":1,"include_ext_alt_text":true,"include_ext_limited_action_results":false,"include_quote_count":true,"include_reply_count":1,"tweet_mode":"extended","include_ext_collab_control":true,"include_ext_views":true,"include_entities":true,"include_user_entities":true,"include_ext_media_color":true,"include_ext_media_availability":true,"include_ext_sensitive_media_warning":true,"include_ext_trusted_friends_metadata":true,"send_error_codes":true,"simple_quoted_tweet":true,"q":"{}","tweet_search_mode":"live","count":{},"query_source":"typed_query",{}"pc":1,"spelling_corrections":1,"include_ext_edit_control":true,"ext":"mediaStats,highlightedLabel,hasNftAvatar,voiceInfo,birdwatchPivot,enrichments,superFollowMetadata,unmentionInfo,editControl,collab_control,vibe"}}'
userInfoApiPar = '{{"screen_name":"{}","withHighlightedLabel":false}}'

# re pattern
# p_tw_link_text = re.compile(r'https://t.co/[\dA-Za-z]+$')
p_csrf_token = re.compile(r'ct0=(.+?)(?:;|$)')
pProxy = re.compile(r'.+?:(\d+)$')
p_user_id = re.compile(r'"rest_id":"(\d+)"')
# p_twt_id = re.compile(r'conversation_id_str":"(\d+)')
p_user_link = re.compile(r'https://twitter.com/([^/]+?)(?:/media)?$')
p_twt_link = re.compile(r'https://twitter.com/(.+?)/status/(\d+)')
# p_pic_link = re.compile(r'''(https://pbs.twimg.com/media/(.+?))['"]''')
# p_gif_link = re.compile(r'(https://video.twimg.com/tweet_video/(.+?\.mp4))')
# p_vid_link = re.compile(
#     r'(https://video.twimg.com/ext_tw_video/(\d+)/(?:pu|pr)/vid/(\d+x\d+)/(.+?\.mp4))')
# p_text_content = re.compile(r'''full_text['"]:\s?['"](.+?)['"]''')
# p_cursor = re.compile(r'value":"(.+?)"')

# http code text warning
httpCodeText = {'403': '本机IP已被推特服务器禁止访问, 请尝试更换代理节点',
                '401': '导入的cookie无效, 请重新获取并导入'}

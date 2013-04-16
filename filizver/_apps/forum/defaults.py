# -*- coding: utf-8 -*-
from django.conf import settings

def get(key, default):
    return getattr(settings, key, default)

# FORUM Settings
FORUM_BASE_TITLE = get('FORUMS_FORUM_BASE_TITLE', 'Django Bulletin Board')
FORUM_META_DESCRIPTION = get('FORUMS_FORUM_META_DESCRIPTION', '')
FORUM_META_KEYWORDS = get('FORUMS_FORUM_META_KEYWORDS', '')
TOPIC_PAGE_SIZE = get('FORUMS_TOPIC_PAGE_SIZE', 10)
FORUM_PAGE_SIZE = get('FORUMS_FORUM_PAGE_SIZE', 20)
SEARCH_PAGE_SIZE = get('FORUMS_SEARCH_PAGE_SIZE', 20)
USERS_PAGE_SIZE = get('FORUMS_USERS_PAGE_SIZE', 20)
AVATARS_UPLOAD_TO = get('FORUMS_AVATARS_UPLOAD_TO', 'forum/avatars')
AVATAR_WIDTH = get('FORUMS_AVATAR_WIDTH', 60)
AVATAR_HEIGHT = get('FORUMS_AVATAR_HEIGHT', 60)
DEFAULT_TIME_ZONE = get('FORUMS_DEFAULT_TIME_ZONE', 3)
SIGNATURE_MAX_LENGTH = get('FORUMS_SIGNATURE_MAX_LENGTH', 1024)
SIGNATURE_MAX_LINES = get('FORUMS_SIGNATURE_MAX_LINES', 3)
HEADER = get('FORUMS_HEADER', 'DjangoBB')
TAGLINE = get('FORUMS_TAGLINE', 'Django based forum engine')
DEFAULT_MARKUP = get('FORUMS_DEFAULT_MARKUP', 'bbcode')
NOTICE = get('FORUMS_NOTICE', '')
USER_ONLINE_TIMEOUT = get('FORUMS_USER_ONLINE_TIMEOUT', 15 * 60)
EMAIL_DEBUG = get('FORUMS_FORUM_EMAIL_DEBUG', False)
POST_USER_SEARCH = get('FORUMS_POST_USER_SEARCH', 1)

# GRAVATAR Extension
GRAVATAR_SUPPORT = get('FORUMS_GRAVATAR_SUPPORT', True)
GRAVATAR_DEFAULT = get('FORUMS_GRAVATAR_DEFAULT', 'identicon')

# LOFI Extension
LOFI_SUPPORT = get('FORUMS_LOFI_SUPPORT', True)

# PM Extension
if 'django_messages' not in settings.INSTALLED_APPS:
    PM_SUPPORT = False
else:
    PM_SUPPORT = get('FORUMS_PM_SUPPORT', True)

# AUTHORITY Extension
AUTHORITY_SUPPORT = get('FORUMS_AUTHORITY_SUPPORT', True)
AUTHORITY_STEP_0 = get('FORUMS_AUTHORITY_STEP_0', 0)
AUTHORITY_STEP_1 = get('FORUMS_AUTHORITY_STEP_1', 10)
AUTHORITY_STEP_2 = get('FORUMS_AUTHORITY_STEP_2', 25)
AUTHORITY_STEP_3 = get('FORUMS_AUTHORITY_STEP_3', 50)
AUTHORITY_STEP_4 = get('FORUMS_AUTHORITY_STEP_4', 75)
AUTHORITY_STEP_5 = get('FORUMS_AUTHORITY_STEP_5', 100)
AUTHORITY_STEP_6 = get('FORUMS_AUTHORITY_STEP_6', 150)
AUTHORITY_STEP_7 = get('FORUMS_AUTHORITY_STEP_7', 200)
AUTHORITY_STEP_8 = get('FORUMS_AUTHORITY_STEP_8', 300)
AUTHORITY_STEP_9 = get('FORUMS_AUTHORITY_STEP_9', 500)
AUTHORITY_STEP_10 = get('FORUMS_AUTHORITY_STEP_10', 1000)

# REPUTATION Extension
REPUTATION_SUPPORT = get('FORUMS_REPUTATION_SUPPORT', True)

# ATTACHMENT Extension
ATTACHMENT_SUPPORT = get('FORUMS_ATTACHMENT_SUPPORT', True)
ATTACHMENT_UPLOAD_TO = get('FORUMS_ATTACHMENT_UPLOAD_TO', 'forum/attachments')
ATTACHMENT_SIZE_LIMIT = get('FORUMS_ATTACHMENT_SIZE_LIMIT', 1024 * 1024)

# SMILE Extension
SMILES_SUPPORT = get('FORUMS_SMILES_SUPPORT', True)
EMOTION_SMILE = get('FORUMS_EMOTION_SMILE', '<img src="%sforum/img/smilies/smile.png" />' % settings.STATIC_URL)
EMOTION_NEUTRAL = get('FORUMS_EMOTION_NEUTRAL', '<img src="%sforum/img/smilies/neutral.png" />' % settings.STATIC_URL)
EMOTION_SAD = get('FORUMS_EMOTION_SAD', '<img src="%sforum/img/smilies/sad.png" />' % settings.STATIC_URL)
EMOTION_BIG_SMILE = get('FORUMS_EMOTION_BIG_SMILE', '<img src="%sforum/img/smilies/big_smile.png" />' % settings.STATIC_URL)
EMOTION_YIKES = get('FORUMS_EMOTION_YIKES', '<img src="%sforum/img/smilies/yikes.png" />' % settings.STATIC_URL)
EMOTION_WINK = get('FORUMS_EMOTION_WINK', '<img src="%sforum/img/smilies/wink.png" />' % settings.STATIC_URL)
EMOTION_HMM = get('FORUMS_EMOTION_HMM', '<img src="%sforum/img/smilies/hmm.png" />' % settings.STATIC_URL)
EMOTION_TONGUE = get('FORUMS_EMOTION_TONGUE', '<img src="%sforum/img/smilies/tongue.png" />' % settings.STATIC_URL)
EMOTION_LOL = get('FORUMS_EMOTION_LOL', '<img src="%sforum/img/smilies/lol.png" />' % settings.STATIC_URL)
EMOTION_MAD = get('FORUMS_EMOTION_MAD', '<img src="%sforum/img/smilies/mad.png" />' % settings.STATIC_URL)
EMOTION_ROLL = get('FORUMS_EMOTION_ROLL', '<img src="%sforum/img/smilies/roll.png" />' % settings.STATIC_URL)
EMOTION_COOL = get('FORUMS_EMOTION_COOL', '<img src="%sforum/img/smilies/cool.png" />' % settings.STATIC_URL)
SMILES = ((r'(:|=)\)', EMOTION_SMILE), #:), =)
          (r'(:|=)\|',  EMOTION_NEUTRAL), #:|, =| 
          (r'(:|=)\(', EMOTION_SAD), #:(, =(
          (r'(:|=)D', EMOTION_BIG_SMILE), #:D, =D
          (r':o', EMOTION_YIKES), # :o, :O
          (r';\)', EMOTION_WINK), # ;\ 
          (r':/', EMOTION_HMM), #:/
          (r':P', EMOTION_TONGUE), # :P
          (r':lol:', EMOTION_LOL),
          (r':mad:', EMOTION_MAD),
          (r':rolleyes:', EMOTION_ROLL),
          (r':cool:', EMOTION_COOL)
         )
SMILES = get('FORUMS_SMILES', SMILES)
# -*- coding: utf-8 -*-
from django.conf import settings


def get(key, default):
    return getattr(settings, key, default)


DEFAULT_MARKUP = get('FILIZVER_DEFAULT_MARKUP', 'markdown')
SMILEYS_SUPPORT = get('FILIZVER_SMILEYS_SUPPORT', True)

EMOTICON_SMILE = get('FILIZVER_EMOTICON_SMILE', '<img src="%simg/smileys/smile.png" />' % settings.STATIC_URL)
EMOTICON_FROWN = get('FILIZVER_EMOTICON_FROWN', '<img src="%simg/smileys/frown.png" />' % settings.STATIC_URL)
EMOTICON_GASP = get('FILIZVER_EMOTICON_GASP', '<img src="%simg/smileys/gasp.png" />' % settings.STATIC_URL)
EMOTICON_GRIN = get('FILIZVER_EMOTICON_GRIN', '<img src="%simg/smileys/grin.png" />' % settings.STATIC_URL)
EMOTICON_TONGUE = get('FILIZVER_EMOTICON_TONGUE', '<img src="%simg/smileys/tongue.png" />' % settings.STATIC_URL)
EMOTICON_WINK = get('FILIZVER_EMOTICON_WINK', '<img src="%simg/smileys/wink.png" />' % settings.STATIC_URL)
EMOTICON_KISS = get('FILIZVER_EMOTICON_KISS', '<img src="%simg/smileys/kiss.png" />' % settings.STATIC_URL)
EMOTICON_GRUMPY = get('FILIZVER_EMOTICON_GRUMPY', '<img src="%simg/smileys/grumpy.png" />' % settings.STATIC_URL)
EMOTICON_GLASSES = get('FILIZVER_EMOTICON_GLASSES', '<img src="%simg/smileys/glasses.png" />' % settings.STATIC_URL)
EMOTICON_SUNGLASSES = get('FILIZVER_EMOTICON_SUNGLASSES', '<img src="%simg/smileys/sunglasses.png" />' % settings.STATIC_URL)
EMOTICON_UPSET = get('FILIZVER_EMOTICON_UPSET', '<img src="%simg/smileys/upset.png" />' % settings.STATIC_URL)
EMOTICON_CONFUSED = get('FILIZVER_EMOTICON_CONFUSED', '<img src="%simg/smileys/confused.png" />' % settings.STATIC_URL)
EMOTICON_SQUINT = get('FILIZVER_EMOTICON_SQUINT', '<img src="%simg/smileys/squint.png" />' % settings.STATIC_URL)
EMOTICON_ANGEL = get('FILIZVER_EMOTICON_ANGEL', '<img src="%simg/smileys/angel.png" />' % settings.STATIC_URL)
EMOTICON_DEVIL = get('FILIZVER_EMOTICON_DEVIL', '<img src="%simg/smileys/devil.png" />' % settings.STATIC_URL)
EMOTICON_UNSURE = get('FILIZVER_EMOTICON_UNSURE', '<img src="%simg/smileys/unsure.png" />' % settings.STATIC_URL)
EMOTICON_CRY = get('FILIZVER_EMOTICON_CRY', '<img src="%simg/smileys/cry.png" />' % settings.STATIC_URL)
EMOTICON_KIKI = get('FILIZVER_EMOTICON_KIKI', '<img src="%simg/smileys/kiki.png" />' % settings.STATIC_URL)
EMOTICON_HEART = get('FILIZVER_EMOTICON_HEART', '<img src="%simg/smileys/heart.png" />' % settings.STATIC_URL)

SMILEYS = (
    (r':-\)|:\)|:\]|=\)', EMOTICON_SMILE), # :-) :) :] =)
    (r':-\(|:\(|:\[|=\(',  EMOTICON_FROWN), # :-( :( :[ =(
    (r':-O|:O|:-o|:o', EMOTICON_GASP), # :-O :O :-o :o
    (r':-D|:D|=D', EMOTICON_GRIN), # :-D :D =D
    (r':-P|:P|:-p|:p|=P', EMOTICON_TONGUE), # :-P :P :-p :p =P
    (r';\-\)|;\)', EMOTICON_WINK), # ;-) ;)
    (r':\-\*|:\*', EMOTICON_KISS), # :-* :*
    (r'\>:\(|\>:\-\(', EMOTICON_GRUMPY), # >:( >:-(
    (r'8\-\)|8\)|B\-\)|B\)', EMOTICON_GLASSES), # 8-) 8) B-) B)
    (r'8\-\||8\||B\-\||B\|', EMOTICON_SUNGLASSES), # 8-| 8| B-| B|
    (r'\>:O|\>:\-O|\>:o|\>:\-o', EMOTICON_UPSET), # >:O >:-O >:o >:-o
    (r'o\.O|O\.o', EMOTICON_CONFUSED), # o.O O.o
    (r'\-\_\-', EMOTICON_SQUINT), # -_-
    (r'O:\)|O:\-\)', EMOTICON_ANGEL), # O:) O:-)
    (r'3:\)|3:\-\)', EMOTICON_DEVIL), # 3:) 3:-)
    (r':\/|:\-\/|:\\|:\-\\', EMOTICON_UNSURE), # :/ :-/ :\ :-\
    (r':\'\(', EMOTICON_CRY), # :'(
    (r'\^\_\^', EMOTICON_KIKI), # ^_^
    (r'\<3', EMOTICON_HEART) # <3
)
SMILEYS = get('FILIZVER_SMILEYS', SMILEYS)
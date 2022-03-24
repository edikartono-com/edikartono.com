from django.conf import settings

STATIC_URL = '%s' % settings.STATIC_URL

TAGCLOUD_MAX_RESULTS = 10

MAX_NUMBER_OF_RESULTS = 10

TAGCLOUD_SEARCH_ICONTAINS = True

TAGCLOUD_AUTOCOMPLETE_TAG_MODEL = getattr(
    settings, 'TAGCLOUD_AUTOCOMPLETE_TAG_MODEL',
    {"default": ('taggit', 'Tag')}
)
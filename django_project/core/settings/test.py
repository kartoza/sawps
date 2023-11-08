from .dev import *  # noqa

DISABLE_2FA=True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
    }
}

WEBPACK_LOADER['DEFAULT']['STATS_FILE'] = absolute_path(
    'frontend', 'webpack-stats.prod.json'
)

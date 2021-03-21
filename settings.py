import os

from datetime import datetime

LOG_LEVEL = os.getenv("APP_LOG_LEVEL", "INFO")
LOG_FILE_NAME_PREFIX = f"console-{datetime.today().strftime('%Y%m%d')}"

LOG_CONFIG = {
        'version': 1,
        'formatters': {
            'detailed': {
                'class': 'logging.Formatter',
                'format': '%(asctime)s %(name)-15s %(levelname)-8s %(processName)-10s %(message)s'
            },
            'simple': {
                'class': 'logging.Formatter',
                'format': '%(name)-15s %(levelname)-8s %(processName)-10s %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
                'level': 'INFO'
            },
            'file': {
                'class': 'logging.FileHandler',
                'filename': f'{LOG_FILE_NAME_PREFIX}.log',
                'mode': 'w',
                'formatter': 'detailed'
            },
            'errors': {
                'class': 'logging.FileHandler',
                'filename': f'{LOG_FILE_NAME_PREFIX}-errors.log',
                'mode': 'w',
                'formatter': 'detailed',
                'level': 'ERROR'
            }
        },
        'loggers': {
            'geneticlib': {
                'handlers': ["console", "file"],
                'level': LOG_LEVEL,
        }
        },
        'root': {
            'handlers': ['console', 'file', 'errors'],
            'level': LOG_LEVEL
        }
}


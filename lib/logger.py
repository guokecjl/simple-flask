# coding: utf-8

import logging.config

from config import DEBUG_LOG, INFO_LOG, ERROR_LOG, WARNING_LOG, DEBUG

__all__ = ['logger']

standard_format = '[%(levelname)s] - [%(asctime)s] [%(filename)s:%(funcName)s][line:%(lineno)d]: %(message)s'
server_format = '[%(levelname)s] - [%(asctime)s]: %(message)s'
server_simple_format = '[%(asctime)s]: %(message)s'
simple_format = '[%(levelname)s] - [%(asctime)s] [%(filename)s]: %(message)s'

# log配置字典
LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': standard_format,
            "datefmt": '%Y-%m-%d %H:%M:%S',
        },
        'server': {
            'format': server_format,
            "datefmt": '%Y-%m-%d %H:%M:%S',
        },
        'server_simple': {
            'format': server_simple_format,
            "datefmt": '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            "datefmt": '%Y-%m-%d %H:%M:%S',
            'format': simple_format
        },
    },
    'filters': {},
    'handlers': {
        # 打印到终端的日志
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple'
        },

        'server_console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'server_simple'
        },

        # 打印到文件的日志,收集info及以上的日志
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'formatter': 'server',

            'filename': DEBUG_LOG,  # 日志文件
            'maxBytes': 1024 * 1024 * 100,  # 日志大小100M
            'backupCount': 5,
            'encoding': 'utf-8',  # 日志文件的编码
        },

        # 打印到文件的日志,收集操作日志
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'formatter': 'standard',

            'filename': INFO_LOG,  # 日志文件
            'maxBytes': 1024 * 1024 * 10,  # 日志大小10M
            'backupCount': 5,
            'encoding': 'utf-8',  # 日志文件的编码
        },

        'warning': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'formatter': 'standard',

            'filename': WARNING_LOG,  # 日志文件
            'maxBytes': 1024 * 1024 * 10,  # 日志大小10M
            'backupCount': 5,
            'encoding': 'utf-8',  # 日志文件的编码
        },

        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'formatter': 'standard',

            'filename': ERROR_LOG,  # 日志文件
            'maxBytes': 1024 * 1024 * 10,  # 日志大小10M
            'backupCount': 5,
            'encoding': 'utf-8',  # 日志文件的编码
        }
    },
    'loggers': {
        'gt-g4-admin-info': {
            'handlers': ['console', 'info'],
            'level': 'INFO',
            'propagate': False
        },
        'gt-g4-admin-debug': {
            'handlers': ['console', 'debug'] if DEBUG else [],
            'level': 'DEBUG',
            'propagate': False
        },
        'gt-g4-admin-warning': {
            'handlers': ['console', 'warning'],
            'level': 'WARNING',
            'propagate': False
        },
        'gt-g4-admin-error': {
            'handlers': ['console', 'error'],
            'level': 'ERROR',
            'propagate': False
        }
    },
}

logging.config.dictConfig(LOGGING_DIC)  # 导入上面定义的logging配置


def get_logger():
    logger = logging.getLogger()
    setattr(logger, 'info', logging.getLogger('gt-g4-admin-info').info)
    setattr(logger, 'debug', logging.getLogger('gt-g4-admin-debug').debug)
    setattr(logger, 'warning', logging.getLogger('gt-g4-admin-warning').warning)
    setattr(logger, 'error', logging.getLogger('gt-g4-admin-error').error)
    setattr(logger, 'exception', logging.getLogger('gt-g4-admin-error').exception)
    return logger


logger = get_logger()

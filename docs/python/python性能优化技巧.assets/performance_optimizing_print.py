#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
print性能优化示例代码
@module performance_optimizing_print
@file performance_optimizing_print.py
"""

import os
import json
import datetime
import logging
import logging.config
from HiveNetLib.simple_log import Logger  # 使用HiveNetLib的日志模块处理

RANGE_NUM = 1000  # 循环次数

LOGGER_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simpleFormatter": {
            "format": "[%(asctime)s][%(levelname)s][PID:%(process)d][TID:%(thread)d][FILE:%(filename)s][FUN:%(funcName)s]%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },

    "handlers": {
        "ConsoleHandler": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simpleFormatter",
            "stream": "ext://sys.stdout"
        },

        "FileHandler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "simpleFormatter",
            "filename": "",
            "maxBytes": 10485760,
            "backupCount": 1000,
            "encoding": "utf8"
        }
    },

    "loggers": {
        "Console": {
            "level": "DEBUG",
            "handlers": ["ConsoleHandler"]
        },

        "File": {
            "level": "INFO",
            "handlers": ["FileHandler"],
            "propagate": "no"
        },

        "ConsoleAndFile": {
            "level": "DEBUG",
            "handlers": ["ConsoleHandler", "FileHandler"],
            "propagate": "no"
        }
    },

    "root": {
        "level": "DEBUG",
        "handlers": []
    }
}

SIMPLE_LOGGER_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simpleFormatter": {
            "format": "[%(asctime)s][%(levelname)s][PID:%(process)d][TID:%(thread)d][FILE:%(filename)s][FUN:%(funcName)s]%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },

    "handlers": {
        "ConsoleHandler": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simpleFormatter",
            "stream": "ext://sys.stdout"
        },

        "FileHandler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "simpleFormatter",
            "filename": "",
            "maxBytes": 10485760,
            "backupCount": 1000,
            "encoding": "utf8"
        },

        "QueueMsgHandler": {
            "class": "HiveNetLib.simple_log.QueueHandler",
            "level": "DEBUG",
            "formatter": "simpleFormatter",
            "queue": "",
            "topic_name": "",
            "is_deal_msg": True,
            "error_queue_size": 20
        }
    },

    "loggers": {
        "Console": {
            "level": "DEBUG",
            "handlers": ["ConsoleHandler"]
        },

        "File": {
            "level": "INFO",
            "handlers": ["FileHandler"],
            "propagate": "no"
        },

        "ConsoleAndFile": {
            "level": "DEBUG",
            "handlers": ["ConsoleHandler", "FileHandler"],
            "propagate": "no"
        },

        "QueueMsg": {
            "level": "DEBUG",
            "handlers": ["QueueMsgHandler"],
            "propagate": "no"
        }
    },

    "root": {
        "level": "DEBUG",
        "handlers": []
    }
}


def use_print():
    """
    使用print
    """
    _index = 0
    while _index < RANGE_NUM:
        _index += 1
        print('use print index %d !' % _index)


def unuse_print():
    """
    不打印
    """
    _index = 0
    while _index < RANGE_NUM:
        _index += 1


def use_logging_console(logger: logging.Logger):
    """
    通过日志对象输出到屏幕

    @param {logging.Logger} logger - 日志对象
    """
    _index = 0
    while _index < RANGE_NUM:
        _index += 1
        logger.info('use logging console index %d !' % _index)


def use_logging_file(logger: logging.Logger):
    """
    使用日志对象输出到文件

    @param {logging.Logger} logger - 日志对象
    """
    _index = 0
    while _index < RANGE_NUM:
        _index += 1
        logger.info('use logging file index %d !' % _index)


def use_simple_console(logger: Logger):
    """
    使用simple_log输出屏幕

    @param {HiveNetLib.simple_log.Logger} logger - 日志对象
    """
    _index = 0
    while _index < RANGE_NUM:
        _index += 1
        logger.info('use simple console index %d !' % _index)


def use_simple_file(logger: Logger):
    """
    使用simple_log输出文件

    @param {HiveNetLib.simple_log.Logger} logger - 日志对象
    """
    _index = 0
    while _index < RANGE_NUM:
        _index += 1
        logger.info('use simple file index %d !' % _index)


def use_simple_queue(logger: Logger):
    """
    使用simple_log输出内存队列

    @param {HiveNetLib.simple_log.Logger} logger - 日志对象
    """
    _index = 0
    while _index < RANGE_NUM:
        _index += 1
        logger.info('use simple queue index %d !' % _index)


if __name__ == '__main__':
    # 使用print
    _start = datetime.datetime.now()
    use_print()
    _end = datetime.datetime.now()
    _use_print_time = (_end - _start).total_seconds()

    # 不使用print
    _start = datetime.datetime.now()
    unuse_print()
    _end = datetime.datetime.now()
    _unuse_print_time = (_end - _start).total_seconds()

    # 创建日志对象
    LOGGER_CONFIG['handlers']['FileHandler']['filename'] = os.path.join(
        os.getcwd(), 'performance_optimizing_print.log')
    logging.config.dictConfig(LOGGER_CONFIG)

    # 使用日志对象输出屏幕
    _logger = logging.getLogger(name='Console')
    _start = datetime.datetime.now()
    use_logging_console(_logger)
    _end = datetime.datetime.now()
    _logging_console_time = (_end - _start).total_seconds()
    del _logger

    # 使用日志对象输出到文件
    _logger = logging.getLogger(name='File')
    _start = datetime.datetime.now()
    use_logging_file(_logger)
    _end = datetime.datetime.now()
    _logging_file_time = (_end - _start).total_seconds()
    del _logger

    # 使用simple_log日志对象输出屏幕
    SIMPLE_LOGGER_CONFIG['handlers']['FileHandler']['filename'] = LOGGER_CONFIG['handlers']['FileHandler']['filename']
    _simple_json_config = json.dumps(
        SIMPLE_LOGGER_CONFIG, ensure_ascii=False
    )
    _logger = Logger(logger_name='Console', json_str=_simple_json_config,
                     is_create_logfile_by_day=False)
    _start = datetime.datetime.now()
    use_simple_console(_logger)
    _end = datetime.datetime.now()
    _simple_console_time = (_end - _start).total_seconds()
    del _logger

    # 使用simple_log日志对象输出文件
    _logger = Logger(logger_name='File', json_str=_simple_json_config,
                     is_create_logfile_by_day=False)
    _start = datetime.datetime.now()
    use_simple_file(_logger)
    _end = datetime.datetime.now()
    _simple_file_time = (_end - _start).total_seconds()
    del _logger

    # 使用内存队列输出文件
    _file_logger = Logger(logger_name='File', json_str=_simple_json_config,
                          is_create_logfile_by_day=False)
    _logger = Logger(logger_name='QueueMsg', json_str=_simple_json_config)
    _logger.base_logger.handlers[0].start_logging(
        {'default': _file_logger}
    )
    _start = datetime.datetime.now()
    use_simple_queue(_logger)
    _end = datetime.datetime.now()
    _simple_queue_time = (_end - _start).total_seconds()
    del _logger

    print('use print time: %s' % str(_use_print_time))
    print('unuse print time: %s' % str(_unuse_print_time))
    print('logging console time: %s' % str(_logging_console_time))
    print('logging file time: %s' % str(_logging_file_time))
    print('simple console time: %s' % str(_simple_console_time))
    print('simple file time: %s' % str(_simple_file_time))
    print('simple queue time: %s' % str(_simple_queue_time))

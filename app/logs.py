'''
日志管理

# CRITICAL	50ERROR	40WARNING	30INFO	20DEBUG	10 NOTSET	0
'''

from app.main import log


def info(msg):

    log.info(msg)

def debug(msg):

    log.debug(msg)

def error(msg):

    log.error(msg)

def warm(msg):

    log.warn(msg )


from sq.config import LOG_LEVEL


def print_log(*args, level='INFO'):
    """
    print log according log level
    :param args: message to print
    :param level: log level, default is 'INFO'
    """
    log_levels = {
        'DEBUG': 10,
        'INFO': 20,
        'WARNING': 30,
        'ERROR': 40
    }
    # set current log level
    # current_log_level = log_levels['INFO']  # 默认为 INFO 级别
    #
    # # check default log level
    # if 'LOG_LEVEL' in globals():
    #     current_log_level = log_levels[globals()['LOG_LEVEL']]

    current_log_level = log_levels[LOG_LEVEL]
    # when message level > current log level, print
    if log_levels[level] >= current_log_level:
        message = ""
        for arg in args:
            message += str(arg)
        print(f"[{level}] ", message)
        # log output to file
        # with open('sq.log', 'a') as file:
        #     print(f"[{level}] ", message, file=file)

    # import logging
    # # configure log
    # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    # logger = logging.getLogger(__name__)
    # logger.info('This is a info message')
    # logger.warning('This is a warning message')
    # logger.error('This is a error message')

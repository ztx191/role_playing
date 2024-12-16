# -*- coding: utf-8 -*-
"""
@Time    : 2024/9/12 17:54
@Author  : 大伟妹
@File    : logger_setting.py
@Software: PyCharm
@description:
"""
import logging


class LoggerTemplate:
    def __init__(self, name, log_file, level=logging.ERROR, print_to_console=True, save_model='a'):
        self.name = name
        self.log_file = log_file
        self.level = level
        self.save_model = save_model
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
        self.print_to_console = print_to_console
        self._setup_handlers(self.log_file)

    def _setup_handlers(self, log_file):
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # 设置文件处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8', mode=self.save_model)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)

        # 设置控制台处理器
        if self.print_to_console:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            stream_handler.setLevel(self.level)
            self.logger.addHandler(stream_handler)

    def get_logger(self):
        return self.logger

    def get_logger_setting(self):
        return {"日志名称": self.name,
                "日志输出路径": self.log_file,
                "日志输出级别": self.level,
                "是否输出到终端": self.print_to_console,
                "保存模式": self.save_model
                }


if __name__ == "__main__":
    # 创建 LoggerTemplate 实例
    logger_template = LoggerTemplate('example_logger', 'logfile.log', print_to_console=True)

    # 获取日志记录器
    log = logger_template.get_logger()

    # 测试不同的日志信息
    log.info('This is an info message.')
    log.warning('This is a warning message.')
    log.error('This is an error message.')
    log.error('你好世界.')
    print(logger_template.get_logger_setting())

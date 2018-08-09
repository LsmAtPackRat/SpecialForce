# This is the Logger module.

import logging
import sys
import os
import time

class Logger:
	# 以下是一些Logger的类属性
 	CRITICAL = 50
 	ERROR = 40
	WARNING = 30
	INFO = 20
	DEBUG = 10
	NOTSET = 0

	DEST_FILE = 100
	DEST_TERM = 200
	DEST_BOTH = 300

	logger_map = {}   # name-logger
    # -------------------------------------------------------

	def __init__(self, name):
		self.inner_logger = logging.getLogger(name)  # self.inner_logger是内置Logger类的实例
		self.log_level = logging.NOTSET
		self.stream_handler = logging.StreamHandler()
		self.stream_handler.setLevel(logging.NOTSET)  # 输出到console的log等级的开关
		#self.stream_handler.setFormatter(self.formatter)
		self.inner_logger.addHandler(self.stream_handler)
		self.dest = Logger.DEST_TERM
		# 存到类中的name-logger的字典里
		Logger.logger_map[name] = self   

	@staticmethod
	def get_logger(name):
		logger = Logger.logger_map.get(name)
		if logger is None:
			logger = Logger(name)
		return logger


	# 设置输出级别
	def set_level(self, level):
		# level用str表示
		if level == Logger.CRITICAL:
			self.inner_logger.setLevel(logging.CRITICAL)
			self.log_level = logging.CRITICAL
		elif level == Logger.ERROR:
			self.inner_logger.setLevel(logging.ERROR)
			self.log_level = logging.ERROR
		elif level == Logger.WARNING:
			self.inner_logger.setLevel(logging.WARNING)
			self.log_level = logging.WARNING
		elif level == Logger.INFO:
			self.inner_logger.setLevel(logging.INFO)
			self.log_level = logging.INFO
		elif level == Logger.DEBUG:
			self.inner_logger.setLevel(logging.DEBUG)
			self.log_level = logging.DEBUG
		else:
			self.inner_logger.setLevel(logging.NOTSET)
			self.log_level = logging.NOTSET

	# 可以将msg包装成一个比较完整的log信息
	def _get_log_str(self, msg):
		log_str = str(time.asctime(time.localtime(time.time()))) + " - " + sys._getframe().f_back.f_back.f_code.co_filename + "[line: " + str(sys._getframe().f_back.f_back.f_lineno) +  "] - " + msg
		return log_str

	def critical(self, msg, *args, **kargs):
		self.inner_logger.critical(self._get_log_str(msg), *args, **kwargs)

	def error(self, msg, *args, **kwargs):
		self.inner_logger.error(self._get_log_str(msg), *args, **kwargs)

	def warn(self, msg, *args, **kwargs):
		self.inner_logger.warning(self._get_log_str(msg), *args, **kwargs)

	def info(self, msg, *args, **kwargs):
		self.inner_logger.info(self._get_log_str(msg), *args, **kwargs)

	def debug(self, msg, *args, **kwargs):
		self.inner_logger.debug(self._get_log_str(msg), *args, **kwargs)


	# 设置输出目标为指定文件，指定模式
	def set_destination_to_file(self, filename, filemode = "w"):
		# 先移除原stream_handler
		if self.dest == Logger.DEST_TERM:
			self.inner_logger.removeHandler(self.stream_handler)
		elif self.dest == Logger.DEST_FILE:
			self.inner_logger.removeHandler(self.file_handler)
		else:
			self.inner_logger.removeHandler(self.stream_handler)
			self.inner_logger.removeHandler(self.file_handler)
		# 安装新的file_handler
		self.file_handler = logging.FileHandler(filename, filemode)
		self.file_handler.setLevel(self.log_level)  # 输出到file的log等级的开关
		#self.file_handler.setFormatter(self.formatter)
		self.inner_logger.addHandler(self.file_handler)
		self.dest = Logger.DEST_FILE


	# 设置输出目标为终端
	def set_destination_to_term(self):
		if self.dest == Logger.DEST_TERM:
			return
		# 其他情况一定有self.file_handler，移除它
		self.inner_logger.removeHandler(self.file_handler)
		# DEST_FILE的情况需要安装新的stream_handler，DEST_BOTH本身就有。只需要改一下状态就可以了
		if self.dest == Logger.DEST_FILE:
			self.stream_handler = logging.StreamHandler()
			self.stream_handler.setLevel(self.log_level)  # 输出到console的log等级的开关
			#self.stream_handler.setFormatter(self.formatter)
			self.inner_logger.addHandler(self.stream_handler)
		self.dest = Logger.DEST_TERM

	
	# 设置输出的目标为文件和终端
	def set_destination_to_both(self, filename, filemode = 'w'):
		if self.dest == Logger.DEST_FILE or self.dest == Logger.DEST_BOTH:
			self.inner_logger.removeHandler(self.file_handler)
			if self.dest == Logger.DEST_FILE:
				self.stream_handler = logging.StreamHandler()
				self.stream_handler.setLevel(self.log_level)  # 输出到console的log等级的开关
				#self.stream_handler.setFormatter(self.formatter)
				self.inner_logger.addHandler(self.stream_handler)
		# 重新设置self.file_handler
		self.file_handler = logging.FileHandler(filename, filemode)
		self.file_handler.setLevel(self.log_level)  # 输出到file的log等级的开关
		#self.file_handler.setFormatter(self.formatter)
		self.inner_logger.addHandler(self.file_handler)
		self.dest = Logger.DEST_BOTH


if __name__ == "__main__":
	# 测试Logger类
	logger = Logger("a")
	#logger.set_level(Logger.ERROR)
	logger.set_destination_to_file("test_log_file")
	logger.warn("hello, lsm!")
	logger.set_destination_to_term()
	logger.warn("hello, lsm!")
	logger.set_destination_to_file("test_log_file", "a")
	
	logger = Logger.get_logger("a")
	logger.warn("hello, haha!")

	logger.set_destination_to_term()
	logger.warn("aha")



	

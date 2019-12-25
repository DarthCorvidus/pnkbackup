import os

from glob import glob

from include.local.BackupStats.BackupStat import BackupStat
from include.local.Config import Config


class BackupStats:
	__files = []
	__path = None

	def __init__(self, argv:list):
		self.__config = []
		self.__files = []
		self.__path = argv[1]
		if os.path.isfile(argv[1]):
			self.__files.append(argv[1])
			return
		for path in glob(argv[1]+"/*.conf"):
			self.__files.append(path)
		self.__files.sort()

	def run(self):
		for file in self.__files:
			config = Config(file)
			stat = BackupStat(config)
			stat.run()

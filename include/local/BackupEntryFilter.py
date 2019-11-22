import os
import datetime

from include.local.BackupEntry import BackupEntry


class BackupEntryFilter:
	def __init__(self):
		self.__dateFrom = None
		self.__dateTo = None
		self.__periods = None
		self.__limit = None
		self.__subdir = None

	def setFrom(self, dateFrom: datetime.date):
		self.__dateFrom = dateFrom

	def setTo(self, dateTo: datetime.date):
		self.__dateTo = dateTo

	def setPeriods(self, periods: list):
		self.__periods = periods;

	def setLimit(self, limit: int):
		self.__limit = limit

	def getLimit(self) -> int:
		return self.__limit

	def hasLimit(self) -> int:
		return self.__limit is not None

	def setSubdir(self, subdir:str):
		self.__subdir = subdir

	def filter(self, entry:BackupEntry) -> bool:
		if self.filterTo(entry) is not True:
			return False
		if self.filterFrom(entry) is not True:
			return False
		if self.filterPeriod(entry) is not True:
			return False
		if self.filterSubdir(entry) is not True:
			return False
		return True

	def filterTo(self, entry:BackupEntry) -> bool:
		if self.__dateTo is None:
			return True
		if int(self.__dateTo.strftime("%s"))>=int(entry.getDate().strftime("%s")):
			return True
		return False

	def filterFrom(self, entry:BackupEntry) -> bool:
		if self.__dateFrom is None:
			return True
		if int(self.__dateFrom.strftime("%s"))<int(entry.getDate().strftime("%s")):
			return True
		return False

	def filterPeriod(self, entry:BackupEntry) -> bool:
		if self.__periods is None:
			return True
		if entry.getPeriod() in self.__periods:
			return True
		return False

	def filterSubdir(self, entry:BackupEntry) -> bool:
		if self.__subdir is None:
			return True
		path = entry.getAbsolutePath()+"/"+self.__subdir
		return os.path.exists(path)
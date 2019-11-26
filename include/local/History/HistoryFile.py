import os
from datetime import date

from include.local.BackupEntry import BackupEntry


class HistoryFile:
	__firstDate = None
	__lastDate = None
	__name = None
	__dir = False
	def __init__(self, path:str, entry:BackupEntry):
		self.__name = os.path.basename(path)
		if os.path.isdir(path):
			self.__dir = True
		self.__firstDate = entry.getDate()
		self.__lastDate = entry.getDate()

	def onTop(self, entry:BackupEntry):
		if entry.getDate().toordinal()<self.__firstDate.toordinal():
			self.__firstDate = entry.getDate()
		if self.__lastDate.toordinal()<entry.getDate().toordinal():
			self.__lastDate = entry.getDate()

	def getFirstDate(self) -> date:
		return self.__firstDate

	def getLastDate(self) -> date:
		return self.__lastDate

	def isDir(self):
		return self.__dir

	def getName(self):
		return self.__name
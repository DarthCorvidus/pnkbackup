import os
from datetime import date

from include.lib.Typetools.Convert.ConvertDate import ConvertDate


class BackupEntry:
	#Default is "daily", which however is not reflected on the filename.
	__period = "daily"
	__fullname = ""
	__date = ""
	__basename = ""
	def __init__(self, dir):
		if not os.path.isdir(dir):
			raise Exception(dir+": is not a directory");
		self.__basename = os.path.basename(dir)
		self.__fullname = dir
		split = self.__basename.split(".")
		self.__date = ConvertDate.datefromiso(split[0])
		#If the filename is without a period,
		if len(split)==1:
			return
		if len(split)>2 or split[1] not in ["weekly", "monthly", "yearly"]:
			raise Exception(self.__basename+": no valid period")
		self.__period = split[1]

	def getPeriod(self) -> str:
		return self.__period

	def getAbsolutePath(self) -> str:
		return self.__fullname

	def getBasename(self) -> str:
		return self.__basename

	def getDate(self) -> date:
		return self.__date

	def __repr__(self):
		return self.__fullname

	def __lt__(self, other):
		return self.__fullname<other.__fullname

	def __gt__(self, other):
		return self.__fullname > other.__fullname

	def __eq__(self, other):
		return self.__fullname == other.__fullname
import os

from glob import glob

from include.lib.Argv.Argv import Argv
from include.local.BackupEntries import BackupEntries
from include.local.BackupEntry import BackupEntry
from include.local.BackupEntryFilter import BackupEntryFilter
from include.local.History.ArgvHistory import ArgvHistory
from include.local.History.HistoryFile import HistoryFile


class History:
	__argv = None
	__entries = None
	__subdir = None
	__files = None

	def __init__(self, argv:list):
		model = ArgvHistory()
		self.__argv = Argv(model, argv)
		entries = BackupEntries.fromPath(self.__argv.getPositionalValue(1))
		self.__subdir = Argv.getNamedValue(self.__argv, "subdir")
		self.__files = {}
		periods = ["daily", "weekly", "monthly", "yearly"]
		filterperiods = []
		for period in periods:
			if self.__argv.getBoolean(period):
				filterperiods.append(period)
		filter = BackupEntryFilter()
		if len(filterperiods)!=0:
			filter.setPeriods(filterperiods)
		self.__entries = entries.getFiltered(filter)
		for i in range(self.__entries.getEntryCount()):
			entry = self.__entries.getEntry(i)
			self.__scan(entry)

	def __scan(self, entry:BackupEntry):
		files = glob(entry.getAbsolutePath()+"/"+self.__subdir+"/*")
		files.sort()
		for file in files:
			basename = os.path.basename(file)
			if basename in self.__files.keys():
				self.__files[basename].onTop(entry)
				continue
			self.__files[basename] = HistoryFile(file, entry)

	def __getHistoryFile(self, file:str) -> HistoryFile:
		return self.__files[file]

	def run(self):
		dir = []
		file = []
		for name in self.__files:
			histFile = self.__getHistoryFile(name)
			if histFile.isDir():
				dir.append(histFile.getName())
			else:
				file.append(histFile.getName())
		dir.sort()
		file.sort()
		for name in dir:
			histFile = self.__getHistoryFile(name)
			print("d "+histFile.getFirstDate().isoformat() +" "+histFile.getLastDate().isoformat()+" "+histFile.getName()+"/")
		for name in file:
			histFile = self.__getHistoryFile(name)
			print("  "+histFile.getFirstDate().isoformat() +" "+histFile.getLastDate().isoformat()+" "+histFile.getName()+"/")

		pass
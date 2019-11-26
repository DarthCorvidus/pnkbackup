import os

from glob import glob

from include.lib.Argv.Argv import Argv
from include.local.BackupEntries import BackupEntries
from include.local.BackupEntry import BackupEntry
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
		self.__entries = BackupEntries.fromPath(self.__argv.getPositionalValue(1))
		self.__subdir = Argv.getNamedValue(self.__argv, "subdir")
		self.__files = {}
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
			entry = self.__getHistoryFile(name)
			if entry.isDir():
				dir.append(entry.getName())
			else:
				file.append(entry.getName())
		dir.sort()
		file.sort()
		for name in dir:
			print("d "+entry.getFirstDate().strftime("%d.%m.%Y")+" "+entry.getLastDate().strftime("%d.%m.%Y")+" "+name+"/")
		for name in file:
			print("  "+entry.getFirstDate().strftime("%d.%m.%Y")+" "+entry.getLastDate().strftime("%d.%m.%Y")+" "+name)

		pass
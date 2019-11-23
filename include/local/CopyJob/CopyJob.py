import os
import shutil
import subprocess
import time
from include.lib.Argv.Argv import Argv
from include.local.BackupEntries import BackupEntries
from include.local.BackupEntry import BackupEntry
from include.local.BackupEntryFilter import BackupEntryFilter
from include.local.CopyJob.ArgvCopy import ArgvCopy
from include.local.Rsync import Rsync


class CopyJob:
	__argv = None
	__source = None
	__target = None
	__diff = None
	__latestSource = None
	__filter = None
	__max = None
	def __init__(self, argv:list):
		argvModel = ArgvCopy()
		self.__argv = Argv(argvModel, argv)
		self.__filter = BackupEntryFilter()
		print("Source Set: "+self.__argv.getPositionalValue(1))
		print("Target Set: "+self.__argv.getPositionalValue(2))
		if self.__argv.hasNamedValue("max"):
			self.__max = int(self.__argv.getNamedValue("max"))
			self.__countdown = self.__max
		self.__load()

	def __load(self):
		self.__source = BackupEntries.fromPath(self.__argv.getPositionalValue(1)).getFiltered(self.__filter)
		self.__target = BackupEntries.fromPath(self.__argv.getPositionalValue(2)).getFiltered(self.__filter)
		self.__determineDiff()

	def __determineDiff(self):
		self.__diff = []
		source = self.__source.getBasenames()
		target = self.__target.getBasenames()
		self.__latestSource = self.__source.getEntry(0)
		added = 0;
		for i in range(self.__source.getEntryCount()):
			if self.__max is not None and added==self.__max:
				return
			item = self.__source.getEntry(i)
			if item.getBasename() in target and item.getPeriod()=="daily":
				self.__latestSource = item
			if item.getBasename() not in target:
				added = added+1
				self.__diff.append(self.__argv.getPositionalValue(2)+"/"+item.getBasename())

	def __copy(self):
		if self.__argv.getBoolean("run") is False:
			print("Use --run to copy.")
			return
		while len(self.__diff)>0:
			target = self.__diff[0]
			temp = self.__argv.getPositionalValue(2)+"/temp.copy/"
			rsync = Rsync(self.__latestSource.getAbsolutePath()+"/", temp)
			if self.__target.getEntryCount()!=0:
				targetLatest = self.__target.getEntry(self.__target.getEntryCount() - 1)
				rsync.setLink(targetLatest.getAbsolutePath())
			print(rsync.getCommand())
			time.sleep(5)
			rsync.exec()
			print("Renaming "+temp+" to "+target)
			os.rename(temp, target);
			if self.__max is not None:
				self.__max = self.__max-1
			self.__load()

	def run(self):
		if len(self.__diff)==0:
			print("No files to be copied.")
			quit()
		print("Files to be copied:")
		for item in self.__diff:
			print("\t"+item)
		self.__copy()
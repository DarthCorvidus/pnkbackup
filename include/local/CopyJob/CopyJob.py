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
	def __init__(self, argv:list):
		argvModel = ArgvCopy()
		self.__argv = Argv(argvModel, argv)
		self.__filter = BackupEntryFilter()
		self.__filter.setPeriods(["daily"])
		print("Source Set: "+self.__argv.getPositionalValue(1))
		print("Target Set: "+self.__argv.getPositionalValue(2))
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
		for i in range(self.__source.getEntryCount()):
			item = self.__source.getEntry(i)
			if item.getBasename() in target and item.getPeriod()=="daily":
				self.__latestSource = item
			if item.getBasename() not in target:
				self.__diff.append(self.__argv.getPositionalValue(2)+"/"+item.getBasename())

	def __copy(self):
		while(len(self.__diff)>0):
			target = self.__diff[0]
			temp = self.__argv.getPositionalValue(2)+"/temp.copy/"
			rsync = Rsync(self.__latestSource.getAbsolutePath()+"/", temp)
			if self.__target.getEntryCount()!=0:
				targetLatest = self.__target.getEntry(self.__target.getEntryCount() - 1)
				rsync.setLink(targetLatest.getAbsolutePath())
			print(rsync.getCommand())
			rsync.exec()
			print("Renaming "+temp+" to "+target)
			os.rename(temp, target);
			self.__replicate(BackupEntry(target))
			self.__load()

	def __replicate(self, entry:BackupEntry):
		tmp = self.__argv.getPositionalValue(2)+"/temp.period"
		if os.path.exists(tmp):
			print("Deleting temporary "+tmp)
			shutil.rmtree(tmp)
		if entry.getDate().strftime("%w")=="0":
			self.__replicateAndRename(entry.getAbsolutePath(), tmp, "weekly")
		if entry.getDate().strftime("%d")=="01":
			self.__replicateAndRename(entry.getAbsolutePath(), tmp, "monthly")
		if entry.getDate().strftime("%d-%m")=="01-01":
			self.__replicateAndRename(entry.getAbsolutePath(), tmp, "yearly")

	def __replicateAndRename(self, daily, tmp, period):
		dst = daily+"."+period
		if os.path.exists(dst):
			print("Deleting "+dst)
			shutil.rmtree(dst)
		print("Copying " + daily + " to " + tmp)
		subprocess.run(["cp", daily, tmp, "-al"])
		print("Renaming " + tmp + " "+dst)
		os.rename(tmp, dst)



	def run(self):
		if len(self.__diff)==0:
			print("No files to be copied.")
			quit()
		print("Files to be copied:")
		for item in self.__diff:
			print("\t"+item)
		self.__copy()
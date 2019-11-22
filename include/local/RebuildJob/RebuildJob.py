import os
import shutil
import subprocess

from include.lib.Argv.Argv import Argv
from include.local.BackupEntries import BackupEntries
from include.local.BackupEntry import BackupEntry
from include.local.BackupEntryFilter import BackupEntryFilter
from include.local.RebuildJob.ArgvRebuild import ArgvRebuild


class RebuildJob():
	__argv = None
	__entries = None
	__rebuild = []
	__max = None
	__count = 0

	def __init__(self, argv:list):
		self.__rebuild = []
		argvModel = ArgvRebuild()
		self.__argv = Argv(argvModel, argv)
		if self.__argv.hasNamedValue("max"):
			self.__max = int(self.__argv.getNamedValue("max"))
		entries = BackupEntries.fromPath(self.__argv.getPositionalValue(0))
		filter = BackupEntryFilter()
		filter.setPeriods(["daily"])
		self.__entries = entries.getFiltered(filter)
		for i in range(self.__entries.getEntryCount()):
			entry = self.__entries.getEntry(i)
			self.__determineRebuild(entry)

	def __determineRebuild(self, entry:BackupEntry):
		weekly = entry.getAbsolutePath() + ".weekly"
		monthly = entry.getAbsolutePath() + ".monthly"
		yearly = entry.getAbsolutePath() + ".yearly"
		periods = ["weekly", "monthly", "yearly"]
		strftime = ["%w", "%d", "%m-%d"]
		expected = ["0", "01", "01-01"]
		for i in range(len(periods)):
			self.__checkCondition(entry, periods[i], strftime[i], expected[i])

	def __checkCondition(self, entry:BackupEntry, period, strftime, expected):
		if(self.__max is not None and self.__max==self.__count):
			return
		path = entry.getAbsolutePath() + "."+period
		if self.__argv.getBoolean(period) is True and os.path.isdir(path) is False and entry.getDate().strftime(strftime)==expected:
			self.__rebuild.append(path)
			self.__count = self.__count + 1

	def __rebuildPeriods(self, path:str):
		basename = os.path.basename(path)
		datename = basename.split(".")[0]
		print(datename)
		src = os.path.dirname(path)+"/"+datename
		tmp = os.path.dirname(path)+"/temp.rebuild"
		dst = path
		print("Source:    "+src)
		print("Temporary: "+tmp)
		print("Final:     "+dst)
		if os.path.isdir(tmp):
			print("Deleting "+tmp)
			shutil.rmtree(tmp)
		print("Copying "+src+" to "+tmp)
		subprocess.run(["cp", src, tmp, "-al"])
		print("Rename "+tmp+" to "+dst+"\n\n")
		os.rename(tmp, dst)

	def run(self):
		if len(self.__rebuild)==0:
			print("No entries to rebuilt")
			quit()
		for path in self.__rebuild:
			print(path)
		if self.__argv.getBoolean("run") is not True:
			print("use --run to rebuild.")
			return
		for path in self.__rebuild:
			self.__rebuildPeriods(path)

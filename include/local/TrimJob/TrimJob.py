import os
import shutil

from datetime import date, timedelta

from include.lib.Argv.Argv import Argv
from include.lib.Typetools.Convert.ConvertDate import ConvertDate
from include.local.BackupEntries import BackupEntries
from include.local.BackupEntryFilter import BackupEntryFilter
from include.local.TrimJob.ArgvTrim import ArgvTrim


class TrimJob:
	__now = None
	__toDelete = None
	__max = None
	__count = 0

	def __init__(self, argv:list):
		model = ArgvTrim()
		self.__toDelete = []
		self.__argv = Argv(model, argv)
		self.__now = ConvertDate.datefromiso(self.__argv.getNamedValue("to"))
		if self.__argv.hasNamedValue("max"):
			self.__max = int(self.__argv.getNamedValue("max"))
		self.__entries = BackupEntries.fromPath(self.__argv.getPositionalValue(1))
		self.__selectDays()
		self.__selectWeeks()
		self.__selectMonths()
		self.__selectYears()

	def __selectDays(self):
		if self.__argv.hasNamedValue("keepDays") is False:
			return
		referenceDate = self.__now - timedelta(days=int(self.__argv.getNamedValue("keepDays")))
		self.__addGeneric(referenceDate, "daily")

	def __selectWeeks(self):
		if self.__argv.hasNamedValue("keepWeeks") is False:
			return
		referenceDate = self.__now - timedelta(weeks=int(self.__argv.getNamedValue("keepWeeks")))
		self.__addGeneric(referenceDate, "weekly")

	def __selectMonths(self):
		if self.__argv.hasNamedValue("keepMonths") is False:
			return
		fdom = ConvertDate.datefromiso(self.__now.strftime("%Y-%m-01"))
		for i in range(int(self.__argv.getNamedValue("keepMonths"))):
			fdom = date.fromordinal(fdom.toordinal()-1)
			fdom = ConvertDate.datefromiso(fdom.strftime("%Y-%m-01"))
		self.__addGeneric(fdom, "monthly")

	def __selectYears(self):
		if self.__argv.hasNamedValue("keepYears") is False:
			return
		fdoy = ConvertDate.datefromiso(self.__now.strftime("%Y-01-01"))
		for i in range(int(self.__argv.getNamedValue("keepYears"))):
			fdoy = date.fromordinal(fdoy.toordinal()-1)
			fdoy = ConvertDate.datefromiso(fdoy.strftime("%Y-01-01"))
		self.__addGeneric(fdoy, "yearly")

	def __addGeneric(self, referenceDate:date, period:str):
		filter = BackupEntryFilter()
		filter.setPeriods([period])
		if self.__argv.hasNamedValue("subdir"):
			filter.setSubdir(self.__argv.getNamedValue("subdir"));
		if self.__argv.hasNamedValue("from"):
			filter.setFrom(ConvertDate.datefromiso(self.__argv.getNamedValue("from")))
		filtered = self.__entries.getFiltered(filter)
		for i in range(filtered.getEntryCount()):
			if self.__max is not None and self.__count == self.__max:
				break
			entry = filtered.getEntry(i)
			if entry.getDate().toordinal()>referenceDate.toordinal():
				continue
			self.__toDelete.append(entry)
			self.__count = self.__count+1

	def __delete(self):
		if self.__argv.getBoolean("run") is False:
			print("Use --run to delete files.")
			return
		root = self.__argv.getPositionalValue(1);
		temp = root+"/temp.delete"
		if os.path.isdir(temp):
			print("Deleting temporary folder "+temp)
			shutil.rmtree(temp)
		for value in self.__toDelete:
			print("Renaming "+value.getAbsolutePath()+" to "+temp)
			os.rename(value.getAbsolutePath(), temp)
			print("Deleting temporary folder")
			shutil.rmtree(temp)

	def run(self):
		if len(self.__toDelete)==0:
			print("No files to be deleted.")
			quit()
		self.__toDelete.sort()
		print("Files to be deleted:")
		for value in self.__toDelete:
			print("\t"+value.getAbsolutePath())

		self.__delete()

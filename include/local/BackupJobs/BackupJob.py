import os
import shutil
import subprocess

from include.lib.Argv.Argv import Argv
from include.lib.Typetools.Convert.ConvertDate import ConvertDate
from include.local.BackupEntries import BackupEntries
from include.local.Config import Config
from include.local.Rsync import Rsync


class BackupJob:
	__config = None
	__argv = None
	__entries = None
	__date = None

	def __init__(self, config:str, argv:Argv):
		self.__date = ConvertDate.datefromiso(argv.getNamedValue("force-date"))
		self.__config = ""
		self.__argv = argv
		self.__config = Config(config)
		self.__entries = BackupEntries.fromPath(self.__config.getTarget())

	def run(self):
		tmp = self.__config.getTarget()+"/temp.backup"
		src = self.__config.getSource()
		dst = self.__config.getTarget()+"/"+self.__date.strftime("%Y-%m-%d")
		rsync = Rsync(src, tmp)
		if os.path.exists(dst):
			rsync.setTarget(dst)
		count = self.__entries.getEntryCount()

		if count==1 and self.__entries.getEntry(count-1).getDate().toordinal()!=self.__date.toordinal():
			rsync.setLink(self.__entries.getEntry(0).getAbsolutePath())
		if count>1 and os.path.exists(dst) is True:
			rsync.setLink(self.__entries.getEntry(count-2).getAbsolutePath())
		if count>1 and os.path.exists(dst) is not True:
			rsync.setLink(self.__entries.getEntry(count-1).getAbsolutePath())

		print(rsync.getCommand())
		rsync.exec()
		if os.path.exists(dst) is False:
			print("Renaming "+tmp+" to "+dst)
			os.rename(tmp, dst)
		self.__replicate(dst)

	def __replicate(self, daily:str):
		tmp = self.__config.getTarget()+"/temp.period"
		if os.path.exists(tmp):
			print("Deleting temporary "+tmp)
			shutil.rmtree(tmp)
		if self.__date.strftime("%w")=="0":
			self.__replicateAndRename(daily, tmp, "weekly")
		if self.__date.strftime("%d")=="01":
			self.__replicateAndRename(daily, tmp, "monthly")
		if self.__date.strftime("%d-%m")=="01-01":
			self.__replicateAndRename(daily, tmp, "yearly")

	def __replicateAndRename(self, daily, tmp, period):
		dst = daily+"."+period
		if os.path.exists(dst):
			print("Deleting "+dst)
			shutil.rmtree(dst)
		print("Copying " + daily + " to " + tmp)
		subprocess.run(["cp", daily, tmp, "-al"])
		print("Renaming " + tmp + " "+dst)
		os.rename(tmp, dst)

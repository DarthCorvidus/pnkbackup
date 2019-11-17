from glob import glob
import os

from include.lib.Argv.Argv import Argv
from include.local.BackupJobs.ArgvBackup import ArgvBackup
from include.local.BackupJobs.BackupJob import BackupJob


class BackupJobs:
	__argv = None
	__jobs = None

	def __init__(self, argv:list):
		model = ArgvBackup()
		self.__argv = Argv(model, argv)
		self.__jobs = []
		if os.path.isfile(self.__argv.getPositionalValue(0)):
			self.__jobs.append(BackupJob(self.__argv.getPositionalValue(0), self.__argv))
			return
		if os.path.isdir(self.__argv.getPositionalValue(0)) is False:
			return
		files = []
		for path in glob(self.__argv.getPositionalValue(0)+"/*.conf"):
			files.append(path)
		files.sort()
		for path in files:
			self.__jobs.append(BackupJob(path, self.__argv))

	def run(self):
		for job in self.__jobs:
			job.run()
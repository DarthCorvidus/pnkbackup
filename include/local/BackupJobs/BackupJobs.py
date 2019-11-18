from glob import glob
import os
from subprocess import CalledProcessError

from include.lib.Argv.Argv import Argv
from include.local.BackupJobs.ArgvBackup import ArgvBackup
from include.local.BackupJobs.BackupJob import BackupJob


class BackupJobs:
	__argv = None
	__jobs = None
	__success = []
	__failed = {}
	def __init__(self, argv:list):
		__failed = {}
		__success = []
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

	def printSuccess(self):
		if len(self.__success)>0:
			print("Successful jobs:")
		for config in self.__success:
			print("\t"+config)

	def printFailed(self):
		if len(self.__failed)>0:
			print("Failed Jobs:")
		for name in self.__failed.keys():
			print("\t"+name+": "+self.__failed[name])
	def run(self):
		for job in self.__jobs:
			try:
				job.run()
				self.__success.append(job.getConfigBasename())
			except Exception as e:
				self.__failed[job.getConfigBasename()] = e.__class__.__name__
		self.printSuccess()
		self.printFailed()

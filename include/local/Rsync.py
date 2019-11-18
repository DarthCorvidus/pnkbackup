import os
import subprocess

class Rsync:
	__source = None
	__target = None
	__exclude = None
	__linkDest = None
	__param = None

	def __init__(self, source, target):
		self.__param = []
		self.__param.append("rsync")
		self.__param.append(source)
		self.__param.append(target)
		self.__param.append("-avz")
		self.__param.append("--delete")

	def setTarget(self, target):
		self.__param[2] = target

	def setExcludeFrom(self, exclude:dir):
		if os.path.isfile(exclude) is False:
			raise RuntimeError("exclude file "+exclude+" does not exist or is no file")
		self.__param.append("--exclude-from="+exclude)

	def getCommand(self):
		return " ".join(self.__param)

	def setLink(self, linkdest:str):
		self.__param.append("--link-dest="+linkdest)

	def exec(self):
		subprocess.check_output(self.__param)
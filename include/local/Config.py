import os

class Config:
	__values = {}
	__filename = ""
	def __init__(self, file):
		self.__values = {}
		self.__filename = file
		handle = open(file, "r")
		for line in handle:
			self.__parse(line)
		handle.close()
		self.__checkExclude()

	def getFilename(self) -> str:
		return self.__filename

	def __parse(self, line:str):
		stripped = line.strip()
		if len(stripped)==0:
			return
		if stripped[0] == "#":
			return
		split = stripped.split("=")
		self.__values[split[0].strip()] = split[1].strip()

	def getSource(self):
		return self.__values["source"]

	def getTarget(self):
		return self.__values["target"]

	def hasExclude(self):
		return "exclude" in self.__values.keys()

	def getExclude(self):
		return self.__values["exclude"]

	def __checkExclude(self):
		if self.hasExclude() is False:
			return
		exclude = self.getExclude()
		if os.path.exists(exclude) is False:
			raise Exception("exclude file "+self.getExclude()+" does not exist")
		if os.path.isfile(self.getExclude()) is False:
			raise Exception("exclude file "+self.getExclude()+" is not a file")
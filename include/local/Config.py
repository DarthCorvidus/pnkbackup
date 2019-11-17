class Config:
	__values = {}

	def __init__(self, file):
		self.__values = {}
		handle = open(file, "r")
		for line in handle:
			self.__parse(line)
		handle.close()

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
from include.lib.Argv.ArgModel import ArgModel
from include.lib.Argv.ArgString import ArgString
from include.lib.Argv.ArgvModel import ArgvModel


class ArgvRebuild(ArgvModel):
	__positional = None
	__positionalNames = None
	__named = None

	def __init__(self):
		self.__positional = []
		self.__positionalNames = []
		self.__positional.append(ArgString())
		self.__positionalNames.append("backup")
		self.__named = {}
		self.__named["max"] = ArgString()

	def getArgNames(self) -> list:
		return self.__named.keys()

	def getNamedArg(self, name: str) -> ArgModel:
		return self.__named[name]

	def getPositionalCount(self) -> int:
		return len(self.__positional)

	def getPositionalArg(self, i: int) -> ArgModel:
		return self.__positional[i]

	def getPositionalName(self, i: int) -> str:
		pass

	def getBoolean(self) -> list:
		return ["weekly", "monthly", "yearly", "all", "run"]

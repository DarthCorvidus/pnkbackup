from include.lib.Argv.ArgModel import ArgModel
from include.lib.Argv.ArgString import ArgString
from include.lib.Argv.ArgvModel import ArgvModel
from include.lib.Typetools.Validate.ValidatePath import ValidatePath


class ArgvCopy(ArgvModel):
	__positional = None
	__positionalNames = None
	__named = None

	def __init__(self):
		self.__positional = []
		self.__positionalNames = []
		config = ArgString()
		config.setValidate(ValidatePath())
		self.__positional.append(config)
		self.__positionalNames.append("source")
		self.__positional.append(config)
		self.__positionalNames.append("target")

	def getArgNames(self) -> list:
		pass

	def getNamedArg(self, name: str) -> ArgModel:
		pass

	def getPositionalCount(self) -> int:
		return len(self.__positional)

	def getPositionalArg(self, i: int) -> ArgModel:
		return self.__positional[i]

	def getPositionalName(self, i: int) -> str:
		return self.__positionalNames[i]

	def getBoolean(self) -> list:
		return ["run"]
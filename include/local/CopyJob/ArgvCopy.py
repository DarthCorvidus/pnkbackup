from include.lib.Argv.ArgModel import ArgModel
from include.lib.Argv.ArgString import ArgString
from include.lib.Argv.ArgvModel import ArgvModel
from include.lib.Typetools.Validate.ValidateDate import ValidateDate
from include.lib.Typetools.Validate.ValidatePath import ValidatePath


class ArgvCopy(ArgvModel):
	__positional = None
	__positionalNames = None
	__named = None

	def __init__(self):
		self.__positional = []
		self.__positionalNames = []
		self.__named = {}
		config = ArgString()
		config.setValidate(ValidatePath())
		self.__positional.append(config)
		self.__positionalNames.append("source")
		self.__positional.append(config)
		self.__positionalNames.append("target")
		self.__named["max"] = ArgString()
		date = ArgString()
		date.setValidate(ValidateDate("iso"))
		self.__named["to"] = date
		self.__named["from"] = date

	def getArgNames(self) -> list:
		return self.__named.keys()

	def getNamedArg(self, name: str) -> ArgModel:
		return self.__named[name]

	def getPositionalCount(self) -> int:
		return len(self.__positional)

	def getPositionalArg(self, i: int) -> ArgModel:
		return self.__positional[i]

	def getPositionalName(self, i: int) -> str:
		return self.__positionalNames[i]

	def getBoolean(self) -> list:
		return ["run"]
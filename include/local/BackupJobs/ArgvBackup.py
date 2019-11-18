from datetime import date

from include.lib.Argv.ArgModel import ArgModel
from include.lib.Argv.ArgString import ArgString
from include.lib.Argv.ArgvModel import ArgvModel
from include.lib.Typetools.Validate.ValidateDate import ValidateDate
from include.lib.Typetools.Validate.ValidatePath import ValidatePath


class ArgvBackup(ArgvModel):
	__positional = None
	__positionalNames = None
	__named = None

	def __init__(self):
		self.__named = {}
		self.__positional = []
		self.__positionalNames = []
		config = ArgString()
		config.setValidate(ValidatePath())
		self.__positional.append(config)
		self.__positionalNames.append("configuration")
		force = ArgString()
		#Set today as default date and use argv.getNamed("force-date") whereever today's date is needed, which saves us
		#from having two dates & lots of comparing.
		force.setDefault(date.today().strftime("%Y-%m-%d"))
		force.setValidate(ValidateDate("iso"))
		self.__named["force-date"] = force

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
		pass

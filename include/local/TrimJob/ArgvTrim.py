import datetime

from include.lib.Argv import ArgModel
from include.lib.Argv.ArgString import ArgString
from include.lib.Argv.ArgvModel import ArgvModel
from include.lib.Typetools.Validate.Validate import Validate
from include.lib.Typetools.Validate.ValidateDate import ValidateDate


class ArgvTrim(ArgvModel):
	__positional = []
	__named = {}
	__positionalName = []

	def __init__(self):
		self.__positional = []
		self.__named = {}
		self.__positionalName = []
		backup = ArgString()
		backup.setMandatory(True)
		self.__positional.append(backup)
		self.__positionalName.append("backup")
		fromdate = ArgString()
		fromdate.setValidate(ValidateDate("iso"))
		self.__named["from"] = fromdate
		todate = ArgString()
		todate.setDefault(datetime.date.today().strftime("%Y-%m-%d"))
		todate.setValidate(ValidateDate("iso"))
		self.__named["to"] = todate
		subdir = ArgString()
		self.__named["subdir"] = subdir
		self.__named["keepDays"] = ArgString()
		self.__named["keepWeeks"] = ArgString()
		self.__named["keepMonths"] = ArgString()
		self.__named["keepYears"] = ArgString()
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
		return self.__positionalName[i]

	def getBoolean(self) -> list:
		return ["run"]


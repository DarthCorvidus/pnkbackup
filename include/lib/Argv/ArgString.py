from include.lib.Argv import ArgModel
from include.lib.Typetools.Convert.Convert import Convert
from include.lib.Typetools.Validate.Validate import Validate


class ArgString(ArgModel.ArgModel):
	__default = None
	__mandatory = False
	__validate = None
	__convert = None

	def __init__(self):
		self.__default = None
		self.__mandatory = False
		self.__validate = None
		self.__convert = None

	def setMandatory(self, mandatory:bool):
		self.__mandatory = mandatory

	def setConvert(self, convert:Convert):
		self.__convert = convert

	def hasConvert(self) -> bool:
		return self.__convert is not None

	def getConvert(self) -> Convert:
		return self.__convert;

	def setDefault(self, default:str):
		self.__default = default

	def hasDefault(self) -> bool:
		return self.__default is not None

	def getDefault(self) -> str:
		return self.__default

	def setValidate(self, validate:Validate):
		self.__validate = validate

	def hasValidate(self) -> bool:
		return self.__validate is not None

	def getValidate(self) -> Validate:
		return self.__validate

	def isMandatory(self) -> bool:
		return self.__mandatory

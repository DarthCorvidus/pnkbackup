import abc

from include.lib.Typetools.Convert.Convert import Convert
from include.lib.Typetools.Validate.Validate import Validate


class ArgModel(metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def getDefault(self) -> str:
		pass

	@abc.abstractmethod
	def hasDefault(self) -> bool:
		pass

	@abc.abstractmethod
	def hasValidate(self) -> bool:
		pass

	@abc.abstractmethod
	def getValidate(self) -> Validate:
		pass

	@abc.abstractmethod
	def hasConvert(self) -> bool:
		pass

	@abc.abstractmethod
	def getConvert(self) -> Convert:
		pass

	@abc.abstractmethod
	def isMandatory(self) -> bool:
		pass

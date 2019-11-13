import abc

from include.lib.Argv.ArgModel import ArgModel


class ArgvModel(metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def getArgNames(self) -> list:
		pass

	@abc.abstractmethod
	def getNamedArg(self, name:str) -> ArgModel:
		pass

	@abc.abstractmethod
	def getPositionalCount(self) -> int:
		pass

	@abc.abstractmethod
	def getPositionalArg(self, i:int) -> ArgModel:
		pass

	@abc.abstractmethod
	def getPositionalName(self, i:int) -> str:
		pass

	@abc.abstractmethod
	def getBoolean(self) -> list:
		pass

import abc


class Convert(metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def convert(self, convertee:str) -> str:
		pass

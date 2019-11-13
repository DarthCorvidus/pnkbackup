import abc


class Validate(metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def validate(self, validee:str):
		pass

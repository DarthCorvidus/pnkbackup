class ArgvException(Exception):
	def __init__(self, message):
		super()
		self.__message = message

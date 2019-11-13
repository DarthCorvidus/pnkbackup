from include.lib.Argv import ArgvModel
from include.lib.Argv.ArgvException import ArgvException
from include.lib.Argv.ArgvModel import ArgvModel
from include.lib.Typetools.Validate.ValidateException import ValidateException


class Argv:
	__argv = None
	__givenPositional = []
	__givenNamed = {}
	__givenBoolean = []
	__argvModel = None
	def __init__(self, argvModel:ArgvModel, argv):
		self.__argv = argv[1:]
		self.__givenPositional = []
		self.__givenNamed = {}
		self.__givenBoolean = []
		self.__argvModel = argvModel
		for arg in self.__argv:
			if arg[0:2] != "--":
				self.__givenPositional.append(arg)
				continue
			self.__parseParameter(arg)

		print(self.__givenPositional)
		print(self.__givenNamed)
		print(self.__givenBoolean)
		self.__checkBoolean()
		self.__checkNamed()
		self.__validateNamed()

	def __parseParameter(self, arg:str):
		pos = arg.find("=");
		if pos == -1:
			self.__givenBoolean.append(arg[2:])
			return
		self.__givenNamed[arg[2:pos]] = arg[pos+1:]

	def __checkPositional(self):
		pass

	def __checkBoolean(self):
		defined = self.__argvModel.getBoolean();
		for given in self.__givenBoolean:
			if given not in defined:
				raise ArgvException("Unknown boolean parameter --"+given);

	def __checkNamed(self):
		defined = self.__argvModel.getArgNames()
		for name in defined:
			arg = self.__argvModel.getNamedArg(name)
			if name not in self.__givenNamed.keys() and arg.isMandatory() is True:
				raise ArgvException("mandatory argument --"+name+" missing")

		for name in self.__givenNamed.keys():
			if name not in defined:
				raise ArgvException("argument --"+name+" not expected")

	def __validateNamed(self):
		for name in self.__givenNamed.keys():
			arg = self.__argvModel.getNamedArg(name)
			value = self.__givenNamed[name]
			print(value)
			if arg.hasValidate() is False:
				continue
			try:
				arg.getValidate().validate(value)
			except ValidateException as e:
				raise ArgvException("--"+name+": "+e.value);
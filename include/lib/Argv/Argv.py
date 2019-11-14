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

		self.__getDefaults();
		self.__checkPositional()
		self.__checkNamed()
		self.__checkBoolean()
		self.__validateNamed()
		self.__validatePositional()

	def __getDefaults(self):
		for name in self.__argvModel.getArgNames():
			if name in self.__givenNamed.keys():
				continue
			if self.__argvModel.getNamedArg(name).hasDefault() is False:
				continue
			print(name + " has default")
			self.__givenNamed[name] = self.__argvModel.getNamedArg(name).getDefault()

	def __parseParameter(self, arg:str):
		pos = arg.find("=");
		if pos == -1:
			self.__givenBoolean.append(arg[2:])
			return
		self.__givenNamed[arg[2:pos]] = arg[pos+1:]

	def __checkPositional(self):
		definedLength = self.__argvModel.getPositionalCount()
		availableLength = len(self.__givenPositional)
		if definedLength==availableLength:
			return
		if availableLength>definedLength:
			raise ArgvException("Unexpected positional argument "+str(definedLength+1))
		if availableLength<definedLength:
			pos = availableLength+1;
			name = self.__argvModel.getPositionalName(availableLength);
			raise ArgvException("Positional argument "+str(pos)+" missing ("+name+")")



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
			if arg.hasValidate() is False:
				continue
			try:
				arg.getValidate().validate(value)
			except ValidateException as e:
				raise ArgvException("--"+name+": "+e.value);

	def __validatePositional(self):
		for pos in range(len(self.__givenPositional)):
			arg = self.__argvModel.getPositionalArg(pos)
			value = self.__givenPositional[pos]
			if arg.hasValidate() is False:
				continue
			try:
				arg.getValidate().validate(value)
			except ValidateException as e:
				raise ArgvException("Argument "+(str(pos+1))+": "+e.value)

	def getBoolean(self, key:str)-> bool:
		if key not in self.__argvModel.getBoolean():
			raise Exception("boolean argument '"+key+"' not defined in "+self.__argvModel.__class__.__name__)
		if key in self.__givenBoolean:
			return True
		return False

	def hasNamedValue(self, key) -> str:
		if key not in self.__argvModel.getArgNames():
			raise Exception("named argument '" + key + "' not defined in " + self.__argvModel.__class__.__name__)
		return key in self.__givenNamed.keys();

	def getNamedValue(self, key) -> str:
		if self.hasNamedValue(key) is False:
			raise Exception("named argument '" + key + "' not available")
		return self.__givenNamed[key]

	def getPositionalValue(self, key:int) -> str:
		if key > len(self.__givenPositional):
			raise Exception("positional argument "+str(key)+" not defined in "+ self.__argvModel.__class__.__name__)
		return self.__givenPositional[key-1]
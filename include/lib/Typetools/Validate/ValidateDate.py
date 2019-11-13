from include.lib.Typetools.Validate import Validate
import re

from include.lib.Typetools.Validate.ValidateException import ValidateException


class ValidateDate(Validate.Validate):
	dateformat = ""

	def __init__(self, dateformat:str):
		self.checkParameter(dateformat)
		self.dateformat = dateformat

	@staticmethod
	def checkParameter(parameter:str):
		if parameter not in ("german", "us", "iso"):
			raise ValidateException("parameter "+parameter+" not valid, must be german, us or iso")

	def validate(self, validee):
		match = None
		if self.dateformat == "german":
			match = re.match("^.{2}\..{2}\..{4}$", validee)
		if self.dateformat == "us":
			match = re.match("^.{2}/.{2}/.{4}$", validee)
		if self.dateformat == "iso":
			match = re.match("^.{4}-.{2}-.{2}$", validee)
		if match == None:
			raise ValidateException(validee+" does not conform to "+self.dateformat+" date format")
		pass
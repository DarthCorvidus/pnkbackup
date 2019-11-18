import os

from include.lib.Typetools.Validate.Validate import Validate
from include.lib.Typetools.Validate.ValidateException import ValidateException


class ValidatePath(Validate):
	def __init__(self):
		pass

	def validate(self, validee):
		if os.path.exists(validee) is False:
			raise ValidateException("path "+validee+" doesn't exist")
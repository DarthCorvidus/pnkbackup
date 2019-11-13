from datetime import date

from include.lib.Typetools.Convert import Convert


class ConvertDate(Convert.Convert):
	source = ""
	target = ""
	def __init__(self, source:str, target:str):
		self.checkParameter(source)
		self.checkParameter(target)
		self.target = target
		self.source = source
		pass

	@staticmethod
	def checkParameter(parameter:str):
		if parameter not in ("german", "us", "iso"):
			raise TypeError("parameter "+parameter+" not valid, must be german, us or iso")

	@staticmethod
	def splitGerman(date:str):
		german = date.split(".")
		iso = []
		iso.append(german[2])
		iso.append(german[1])
		iso.append(german[0])
		return iso
	@staticmethod
	def splitUS(date:str):
		german = date.split("/")
		iso = []
		iso.append(german[2])
		iso.append(german[0])
		iso.append(german[1])
		return iso
	@staticmethod
	def joinUS(date:list):
		return date[1]+"/"+date[2]+"/"+date[0]

	@staticmethod
	def joinGerman(date:list):
		return date[2] + "." + date[1] + "." + date[0]

	def convert(self, convertee:str):
		if self.target == self.source:
			return convertee
		if(self.source=="german" and self.target=="iso"):
			iso = self.splitGerman(convertee)
			return "-".join(iso)
		if self.source == "german" and self.target=="us":
			iso = self.splitGerman(convertee)
			return self.joinUS()
		if(self.source=="iso" and self.target=="german"):
			iso = convertee.split("-")
			return self.joinGerman(iso)
		if(self.source=="iso" and self.target=="us"):
			iso = convertee.split("-")
			return self.joinUS(iso)
		if self.source=="us" and self.target=="iso":
			iso = self.splitUS(convertee)
			return "-".join(iso)
		if self.source=="us" and self.target=="german":
			iso = self.splitUS(convertee)
			return self.joinGerman(iso)

	@staticmethod
	def datefromiso(iso:str) -> date:
		split = iso.split("-")
		return date(int(split[0]), int(split[1]), int(split[2]))
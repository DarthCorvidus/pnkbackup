import os

import sys
from glob import glob

from include.lib.Typetools.Convert.ConvertDate import ConvertDate
from include.local.BackupEntry import BackupEntry
from include.local.BackupEntryFilter import BackupEntryFilter


class BackupEntries:
	__entries = []

	def __init__(self):
		self.__entries = []

	@staticmethod
	def fromPath(dir):
		files = glob(dir+"/*")
		files.sort();
		entries = BackupEntries()
		for file in files:
			try:
				entry = BackupEntry(file)
				entries.addEntry(entry)
			except Exception as e:
				print("Skipping "+file)
		return entries

	def addEntry(self, entry:BackupEntry):
		self.__entries.append(entry)

	def getEntryCount(self) -> int:
		return len(self.__entries)

	def getEntry(self, i:int) -> BackupEntry:
		return self.__entries[i]

	def getFiltered(self, filter:BackupEntryFilter):
		new = BackupEntries()
		i = 0
		for entry in self.__entries:
			if filter.filter(entry) is True:
				new.addEntry(entry)
				i = i+1
			if filter.hasLimit() and i>=filter.getLimit():
				return new
		return new

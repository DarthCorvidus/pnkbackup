import os
from datetime import date

from reportlab.graphics.charts.lineplots import _maxWidth

from include.local.BackupEntries import BackupEntries
from include.local.Config import Config


class BackupStat:
	def __init__(self, config:Config):
		self.__config = config
		self.__entries = BackupEntries.fromPath(config.getTarget())

	def run(self):
		print(os.path.basename(self.__config.getFilename()))
		basenames = self.__entries.getBasenames()

		first = self.__entries.getEntry(0)
		last = self.__entries.getEntry(self.__entries.getEntryCount()-1)
		print("\tRange:    " + first.getDate().isoformat() + " to " + last.getDate().isoformat())
		print("\tLocation: "+self.__config.getTarget())
		daily = 0
		weekly = 0
		monthly = 0
		yearly = 0
		maxDaily = 0
		maxWeekly = 0
		maxMonthly = 0
		maxYearly = 0
		current = first.getDate()
		while current.toordinal() < last.getDate().toordinal():
			maxDaily = maxDaily + 1
			if current.isoformat() in basenames:
				daily = daily+1

			if current.strftime("%w")=="0":
				maxWeekly = maxWeekly + 1
			if current.strftime("%w") == "0" and current.isoformat() + ".weekly" in basenames:
				weekly = weekly + 1

			if current.strftime("%d")=="01":
				maxMonthly = maxMonthly + 1
			if current.strftime("%d")=="01" and current.isoformat()+".monthly" in basenames:
				monthly = monthly+1

			if current.strftime("%m-%d")=="01-01":
				maxYearly = maxYearly + 1
			if current.strftime("%m-%d") == "01-01" and current.isoformat() + ".yearly" in basenames:
				yearly = yearly + 1



			current = date.fromordinal(current.toordinal()+1)

		print("\tDaily:    " + str(daily) + " of " + str(maxDaily))
		print("\tWeekly:   " + str(weekly) + " of " + str(maxWeekly))
		print("\tMonthly:  " + str(monthly) + " of " + str(maxMonthly))
		print("\tYearly:   " + str(yearly) + " of " + str(maxYearly))
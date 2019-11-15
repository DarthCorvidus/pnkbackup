#!/usr/bin/env python3
import datetime
import os
import sys
#from include.local.Main import Main

#main = BackupJob()
#main.run()
from include.lib.Argv.ArgString import ArgString
from include.lib.Argv.Argv import Argv
from include.lib.Argv.ArgvException import ArgvException
from include.lib.Typetools.Convert import ConvertDate
from include.lib.Typetools.Convert.ConvertDate import ConvertDate
from include.lib.Typetools.Validate.ValidateDate import ValidateDate
from include.local.BackupEntries import BackupEntries
from include.local.BackupEntryFilter import BackupEntryFilter
from include.local.RebuildJob.RebuildJob import RebuildJob
from include.local.TrimJob import TrimJob
from include.local.TrimJob.ArgvTrim import ArgvTrim
from include.local.TrimJob.TrimJob import TrimJob

try:
	job = RebuildJob(sys.argv);
	job.run()
except ArgvException as e:
	print(e)
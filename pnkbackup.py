#!/usr/bin/env python3
import sys
from include.lib.Argv.ArgvException import ArgvException
from include.local.BackupJobs.BackupJobs import BackupJobs

try:
	backup = BackupJobs(sys.argv)
	backup.run()
except ArgvException as e:
	print(e)
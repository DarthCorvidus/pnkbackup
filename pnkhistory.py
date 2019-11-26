#!/usr/bin/env python3
import sys
from include.lib.Argv.ArgvException import ArgvException
from include.local.BackupJobs.BackupJobs import BackupJobs
from include.local.History.History import History

try:
	history = History(sys.argv)
	history.run()
except ArgvException as e:
	print(e)
except KeyboardInterrupt as e:
	print("Interrupted by user (CTRL+C)")
#!/usr/bin/env python3
import sys
from include.lib.Argv.ArgvException import ArgvException
from include.local.TrimJob.TrimJob import TrimJob

try:
	job = TrimJob(sys.argv);
	job.run()
except ArgvException as e:
	print(e)
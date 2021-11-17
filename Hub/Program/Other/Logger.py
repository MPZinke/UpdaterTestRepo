#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

###########################################################################
#
#	created by: MPZinke
#	on 2020.10.15
#
#	DESCRIPTION:
#	BUGS:
#	FUTURE:
#
###########################################################################


from datetime import datetime;
from json import dumps as json_dumps;
from sys import stderr;
import traceback;
from typing import Union;

from Other.Global import LOG_DIR;


# Writes error to log file. If issue occurs writing error, error is sent to stderr along with previous function call.
# Takes error object or string.
# Tries to traceback error. Creates json error message. Writes error to log (or stderr).
# Returns whether successfully written to log.
def log_error(error : Union[Exception, str]) -> bool:
	try:
		try: module = traceback.format_exc();
		except: module = "Unknown traceback";
		error_data = {"time": datetime.now().strftime("%H:%M:%S"), "module": module, "error": str(error)};
		error_message = json_dumps(error_data, indent=4);

		print(error_message);

		log_name = LOG_DIR+"/"+datetime.now().strftime("%Y.%m.%d")+".log";
		with open(log_name, "a") as log: log.write(error_message);

		return True;

	except Exception as log_error_error:
		from inspect import stack;
		print(stack()[1][3]+": ", error, file=stderr);

		return False;

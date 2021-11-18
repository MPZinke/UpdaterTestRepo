#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on ..                                                                                                              #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from typing import Union;

from Other.Class.ZThread import ZThread;
import Other.Logger;


class ZWidget:
	def __init__(self, name: str, system: object=None, sleep_time: Union[int, float]=0):
		self._System = system;
		self._sleep_time = sleep_time;
		self._zthread = ZThread(name, self._loop_process, self.sleep_time);  # main driver of widget


	def __del__(self):
		try: self._zthread.kill();
		except: pass;


	# ————————————————————— THREAD —————————————————————

	# Securely ends widget update.
	# Returns whether thread was successfully killed.
	def kill(self) -> None:
		try:
			self._zthread.kill();
			return True;
		except Exception as error:
			Logger.log_error(error);
			return False;

	# Checks if ZThread is still active.
	def is_alive(self) -> None:
		return self._zthread.is_alive();


	# Starts the ZThread.
	def start(self) -> None:
		self._zthread.start();


	# Overrideable function to set the amount of time a thread can sleep.
	# Defaults to returning the sleep time.
	# Can be overridden to calculate a sleep time.  This can be so that specific conditions can be introduced to
	#   determine the sleep time (EG at a specific time of day).
	def sleep_time(self):
		return self._sleep_time;


	# PLACEHOLDER: this is what is passed to the ZThread and is operated on.
	def _loop_process(self) -> None:
		raise Exception("ZWidget::_loop_process has not been overridden");

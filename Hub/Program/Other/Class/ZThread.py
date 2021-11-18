#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"


########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.11.04                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE: Consider moving to multiprocessing::Process instead.                                                       #
#                                                                                                                      #
########################################################################################################################


from collections.abc import Callable;
from threading import Condition, Thread;
import warnings;
from warnings import warn as Warn;
from typing import Union;

from Other.Global import warning_message;
import Other.Logger;


# Modified thread class for executing a process and sleeping afterwards.
# Also allows for sleeping and waking a thread.
class ZThread(Thread):
	def __init__(self, name : str, loop_process : Callable, sleep_time : Callable):
		Thread.__init__(self, name=name, target=self._thread_loop);

		self._condition = Condition();  # allows for sleep/wake feature
		self._is_active = True;  # used by thread_loop() for maintaining while loop
		self._loop_process = loop_process;  # operations special to child object
		self._sleep_time = sleep_time;  # function pointer to determine/return the amount of time it should sleep

		warnings.formatwarning = warning_message;


	# Ends a thread.
	# Releases loop, wakes sleeping condition, joins thread with rest of program.
	def kill(self) -> None:
		if(not self._is_active and not self.is_alive()): raise Exception("Thread is already killed");

		self._is_active = False;
		with self._condition: self._condition.notify();


	# Changes the amount of time Condition::wait() will wait until next iteration.
	# Takes a function to determine the time ::_sleep_time will calculate. New sleep amount will begin after current 
	# iteration on _thread_loop is complete.
	# To implement immediately, follow with ::sleep(sleep_time()).
	def set_sleep_time(self, sleep_time : Callable) -> None:
		self._sleep_time = sleep_time;


	# Sleeps thread_loop for amount of time.
	# Takes a numeric amount of time defaulted to None.
	# Sleeps for default amount of time if specified, otherwise indefinitely.
	def sleep(self, sleep_amount : int=0) -> None:
		with self._condition:
			if(sleep_amount): self._condition.wait(sleep_amount);
			else:
				Warn(f"Thread: {self.name} has been indefinitely put to sleep");
				self._condition.wait();  # incase 0 is used, default to indefinitely


	# Starts a thread after deciding whether to run ::_loop_process on first iteration.
	# Takes whether the first iteration should be skipped.
	# Sets whether the first iterations should be skipped and starts self (Thread::start).
	def start_thread(self, skip_first_iteration : bool=False):
		self._skip_iteration_process = skip_first_iteration;
		self.start();


	# Main loop that runs thread if activated.
	# Check that the it is supposed to do stuff, then sleeps thread
	def _thread_loop(self) -> None:
		try:  # make it safe!!!
			while(self._is_active):
				self._loop_process();
				self.sleep(self._sleep_time());
		except Exception as error:
			try: Logger.log_error(error);
			except: pass;


	# Wakes thread (condition from sleep).
	def wake(self) -> None:
		if(not self._is_active): raise Exception("Waking a dead thread does nothing. Try using restart()");
		with self._condition: self._condition.notify();

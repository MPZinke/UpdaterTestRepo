#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2021.11.14                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from os import execl as os_execl;
from os.path import abspath as os_path_abspath
import sys;
from time import sleep;


from Updater.Updater import Updater;


class Main:
	def __init__(self):
		self._Updater = Updater(self);
		self._Updater.start();

		self.main_loop();


	def main_loop(self):
		while(True):
			try:
				sleep(2);
			except KeyboardInterrupt:
				self._Updater.kill();
				return;


	def restart_program(self):
		self._Updater.kill()
		print("Killed Updater")
		os_execl(sys.executable, os_path_abspath(__file__), *sys.argv) 


def main():
	print("————————————————————————————————————————————————— v0.2.7 —————————————————————————————————————————————————")
	program = Main();
	program.main_loop();


if __name__ == '__main__':
	main();

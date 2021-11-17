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


from time import sleep

from Updater import Updater


class Main:
	def __init__(self):
		self._Updater = None;
		self._Updater.start();

		self.main_loop();


	def main_loop(self):
		while(True):
			sleep(2);


def main():
	program = Main();


if __name__ == '__main__':
	main();

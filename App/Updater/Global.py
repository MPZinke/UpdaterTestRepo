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


from datetime import datetime, timedelta;
from pathlib import Path as __pathlib__Path;
import sys;


# ———— Directories ————
REPO_DIR = str(__pathlib__Path(__file__).parent.parent.parent.parent);  # /usr/local/SmartCurtain
HUB_DIR = str(__pathlib__Path(__file__).parent.parent.parent);  # /usr/local/SmartCurtain/Hub
DB_DIR = str(__pathlib__Path(__file__).parent.parent.parent)+"/DB";  # /usr/local/SmartCurtain/Hub/DB
PYTHON_DIR = str(__pathlib__Path(__file__).parent.parent);  # /usr/local/SmartCurtain/Hub/Program
# ———— Directories::Other ————
LOG_DIR = "/var/log/SmartCurtain"


NONETYPE = type(None);


# SUGAR
# Gets the substring from a string using a list parameter.
# Takes the string to get substring from, list of start and end points.
# Uses standard substring method
def substr(string: str, span: list) -> str:
	return string[span[0]: span[1]];


# Get the datetime object for the next day at 00:00:00.
# Compliments of https://jacobbridges.github.io/post/how-many-seconds-until-midnight/
def tomorrow_00_00():
	tomorrow = datetime.now() + timedelta(1);
	return datetime(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day, hour=0, minute=0, second=0);


# SUGAR: tries to convert a value to the specified type.
# Takes value to convert, type to convert to.
# If it fails, returns None.
def try_convert(value, value_type):
	try: return value_type(value);
	except: return None;


# Used to override warning format & return only the warning message.
def warning_message(message, category, filename, lineno, line=''):
	return str(message)+"\n";
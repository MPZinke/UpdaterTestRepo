#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2021.10.13                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from re import match as re_match, search as re_search;


class Version:
	def __init__(self, version_string: str):
		# Check that it matches the regex
		match = re_match(r"v[0-9]+(\.[0-9]+){0,2}", version_string)
		if(not match or match.span()[0] != 0 or match.span()[1] != len(version_string)):
			raise Exception(fr"{version_string} does not match format {{v[0-9]+(\.[0-9]+){0,2}}}");

		version_parts = version_string.split(".");
		self._major_version = int(version_parts[0][1:] if version_parts else 0);
		self._minor_version = int(version_parts[1] if len(version_parts) > 1 else 0);
		self._patch_version = int(version_parts[2] if len(version_parts) > 2 else 0);


	# Gets the version number from a string by REGEX.
	@staticmethod
	def version_string(string: str):
		search = re_search(r"v[0-9]+(\.[0-9]+){0,2}", string);

		return search.group(0) if search else None;


	def major_version(self):
		return self._major_version;


	def minor_version(self):
		return self._minor_version;


	def patch_version(self):
		return self._patch_version;


	def __str__(self):
		return f"v{self._major_version}.{self._minor_version}.{self._patch_version}";


	def __eq__(self, right: object):
		if(self._major_version != right.major_version()): return False;
		if(self._minor_version != right.minor_version()): return False;
		if(self._patch_version != right.patch_version()): return False;

		return True;


	def __ne__(self, right: object):
		if(self._major_version != right.major_version()): return True;
		if(self._minor_version != right.minor_version()): return True;
		if(self._patch_version != right.patch_version()): return True;

		return False;


	def __gt__(self, right: object):
		if(self._major_version > right.major_version()): return True;
		if(self._minor_version > right.minor_version()): return True;
		if(self._patch_version > right.patch_version()): return True;

		return False;


	def __ge__(self, right: object):
		if(self._major_version > right.major_version()): return True;
		if(self._major_version < right.major_version()): return False;
		if(self._minor_version > right.minor_version()): return True;
		if(self._minor_version < right.minor_version()): return False;
		if(self._patch_version > right.patch_version()): return True;
		if(self._patch_version < right.patch_version()): return False;

		return True;


	def __lt__(self, right: object):
		if(self._major_version < right.major_version()): return True;
		if(self._minor_version < right.minor_version()): return True;
		if(self._patch_version < right.patch_version()): return True;

		return False;


	def __le__(self, right: object):
		if(self._major_version < right.major_version()): return True;
		if(self._major_version > right.major_version()): return False;
		if(self._minor_version < right.minor_version()): return True;
		if(self._minor_version > right.minor_version()): return False;
		if(self._patch_version < right.patch_version()): return True;
		if(self._patch_version > right.patch_version()): return False;

		return True;

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2021.10.07                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from datetime import datetime;
from os import devnull as os_devnull, listdir as os_listdir;
from os.path import	basename as os_path_basename, exists as os_path_exists, isfile as os_path_isfile, \
					join as os_path_join, splitext as os_path_splitext;
from re import search as re_search;
from subprocess import call as subprocess_call, check_output as subprocess_check_output;
from threading import Lock;

# from Global import DB_DIR, substr;
from Other.Global import *;
from Other.Global import tomorrow_00_00;
from Updater.Version import Version;
from Other.Class.ZWidget import ZWidget;


class Updater(ZWidget):
	def __init__(self):
		ZWidget.__init__(self, "Updater");
		self._mutex = Lock();

		self.local_version = self.get_local_version();
		self.origin_Production_version = self.get_remote_version();


	# ——————————————————————————————————————————————————— ZWIDGET  ——————————————————————————————————————————————————— #

	# Increment versions, checking for DB updates. If found, update DB
	def _loop_process(self):
		self.origin_Production_version = self.get_remote_version();

		if(self.origin_Production_version != self.local_version):
			self._mutex.acquire();

			try:
				self.update_git();
				self.update_db();
				self.restart_service();

			except Exception as error:
				# Program will never get here, if it fails at some point
				self._mutex.release();
				raise error;


	# Compliments of https://jacobbridges.github.io/post/how-many-seconds-until-midnight/
	def sleep_time(self) -> int:
		return (tomorrow_00_00() - datetime.now()).seconds + 30;  # give time to let event creators to do their thing


	# ————————————————————————————————————————————— GIT VERSION GETTERS  ————————————————————————————————————————————— #

	# Get current version from repo.
	def get_local_version(self):
		git_describe = subprocess_check_output(["git", "-C", REPO_DIR, "describe", "--tags"]);
		if(not git_describe): raise Exception("git describe was unable to get version number");

		describe_version = Version.version_string(git_describe.decode("utf-8"))
		if(not describe_version): raise Exception("Unable to search version number from git describe");
		return Version(describe_version);


	# Get remote version from remote repo.
	def get_remote_version(self):
		git_ls_remote = subprocess_check_output(["git", "-C", REPO_DIR, "ls-remote", "--tag", "origin"]);
		if(not git_ls_remote): raise Exception("git describe was unable to get version number");

		tag_strings = [Version.version_string(line) for line in git_ls_remote.decode("utf-8").rstrip().split("\n")];
		tag_strings = [tag_string for tag_string in tag_strings if(tag_string)];
		if(not tag_strings): raise Exception("Unable to find any version number from git describe");

		tags = [Version(tag) for tag in tag_strings];
		tags.sort();
		return tags[-1];


	# Checks whether provided branch name is the currently checked out branch.
	def branch_is_(self, branch_name: str) -> bool:
		git_branch = subprocess_check_output(["git", "-C", REPO_DIR, "branch"]);
		if(not git_branch): return False;

		local_branches = git_branch.decode("utf-8").rstrip().split("\n");
		return f"* {branch_name}" in local_branches;


	# ———————————————————————————————————————————————————— UPDATE ———————————————————————————————————————————————————— #

	# Updates the DB incrementally with known update files.
	# Gets all files in folder except ./.add. Creates a Version object for all files. Sorts files by version number.
	#  Runs DB update file in mysql.
	def update_db(self):
		DB_update_folder = DB_DIR+"/Updates";
		if(not os_path_exists(DB_update_folder)): return;

		# Get all files that match versioning
		file_versions = [];
		for file in os_listdir(DB_update_folder):
			filepath = os_path_join(DB_update_folder, file);
			# Try to get the file's name excluding extension (valid filename example: v0.0.0.sql)
			version_string = Version.version_string(os_path_splitext(os_path_basename(filepath))[0]);

			# Include only files with proper version names within update range
			if(os_path_isfile(filepath) and version_string and self.version_is_usable(Version(version_string))):
				file_versions.append({"path": filepath, "version": Version(version_string)});

		file_versions.sort(key=lambda file_version : file_version["version"]);

		for file in file_versions:
			if(self.call_shell_command(["sudo", "mysql", "-u", "root", "<", file["path"]])):
				raise Exception(f"Failed to update DB with file {file['path']}");


	# Updates the Python and DB repository for the Hub.
	def update_git(self):
		if(not self.branch_is_("Production")):
			if(self.call_shell_command(["git", "-C", REPO_DIR, "checkout", "Production"])):
				raise Exception("Could not checkout Production branch");

		if(self.call_shell_command(["git", "-C", REPO_DIR, "pull"])):
			raise Exception("Could not pull repository");


	def restart_service(self):
		if(self.call_shell_command(["sudo", "systemctl", "restart", "UpdaterTestRepo.service"])):
			raise Exception("Could not restart systemctl service");


	# ——————————————————————————————————————————————————— UTILITY  ——————————————————————————————————————————————————— #

	def call_shell_command(self, params: list):
		with open(os_devnull, 'w') as FNULL:
			return subprocess_call(params, stdout=FNULL);


	# SUMMARY: Gets versions that are within version range (greater than current up to new version).
	# PARAMS: Takes the version object to compare to local_version and origin_Production_version.
	# DETAILS: This allows for all incremental DB updates to be processed in order.
	def version_is_usable(self, version: Version) -> bool:
		try:
			return self.local_version < version and version <= self.origin_Production_version;
		except Exception as error:
			Logger.log_error(error);
			return False;

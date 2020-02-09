#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Saku Rautio"
__email__ = "sakupetterirautio@gmail.com"
__date__ = "2020-02-02"

__license__ = "MIT"
__version__ = "1.0.0"

import sys
from datetime import datetime

from error_code import ErrorCode
from config import Config
from logger import Logger
LOG_TAG = "Manager"
import version
import VersionEmailer.version_emailer as emailer
import VersionFileGenerator.version_file_generator as versionFileGenerator


def PrintHelp(argv: list, argc: int) -> ErrorCode:
   """
   Print a help message on how to use the Version Manager.

   Args:
      argv (list): The given arguments.
      argc (int): The count of given arguments.
   
   Returns:
      An ErrorCode object telling what the outcome of calling the function was.
   """
   HELP_MESSAGE = \
"""
The version manager program.

Usage:
version_manager.py <command> [args]

Required:
   command  What you want the version manager to do. Available commands:
            generate    Generate files using Git versioning.
            version     Use the Git versioning.
            email       Send emails using Git versioning.

Optional:
   help   Print this message.
   Use '<command> help' to get information about that particular command.
"""
   print(HELP_MESSAGE)
   return ErrorCode.OK

if __name__ == '__main__':
   result = ErrorCode.OK

   # Init
   Config.InitConfig()
   Logger.Init()

   argv = sys.argv[1:]
   argc = len(sys.argv)
   
   if (argc < 1):
      Logger.Error(LOG_TAG, "No command given")
      result = ErrorCode.UNKNOWN_COMMAND
   else:
      commandSwitcher = {
         'generate': versionFileGenerator.HandleCommand,
         'version': version.HandleCommand,
         'email': emailer.HandleCommand,
         'help': PrintHelp
      }
      chosenCommand = commandSwitcher.get(argv[0], None)
      if (chosenCommand == None):
         Logger.Warning(LOG_TAG, 'Unknown command: {0}'.format(argv[0]))
         result = ErrorCode.UNKNOWN_COMMAND
      else:
         result = chosenCommand(argv, argc)
   
   sys.exit(result)

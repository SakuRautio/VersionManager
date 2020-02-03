#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Saku Rautio"
__email__ = "sakupetterirautio@gmail.com"
__date__ = "2020-02-02"

__license__ = "MIT"
__version__ = "1.0.0"

import json
import os
import inspect

from error_code import ErrorCode
LOG_TAG = "Config"

class Config:
   """
   Parse and provide the config.json.
   """
   config = None
   @staticmethod
   def InitConfig() -> ErrorCode:
      """
      Initialize the global variable 'CONFIG' so that
      other modules can use it. Read the data from
      the 'config.json' to the 'CONFIG' variable,
      making it a dictionary representation of the
      'config.json' file contents.

      Returns:
         An error code from the ErrorCode class.
      """
      try:
         scriptDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
         with open(os.path.join(scriptDir, 'config.json'), 'r') as configFile:
            Config.config = json.load(configFile)
      except:
         return ErrorCode.FILE_ERROR

      return ErrorCode.OK 
   @staticmethod
   def GetConfig() -> dict:
      if (Config.config == None):
         Config.InitConfig()
      return Config.config

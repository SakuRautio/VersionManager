#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Saku Rautio"
__email__ = "sakupetterirautio@gmail.com"
__date__ = "2020-02-02"

__license__ = "MIT"
__version__ = "1.0.0"

import os
from datetime import datetime
from enum import IntEnum, auto, unique

from config import Config
from date import Date

class Logger:
   """
   Provide an API for a logger for the program,
   which prints out logged messages to the terminal
   and saves the logged messages to a log file (if enabled in the 'config.json' and the file path is set).
   """
   LOG_FILE = 'version_manager_{timestamp}.log'
   LOG_MESSAGE_FORMAT = '[{level}:{timestamp}:{tag}]: {message}'
   @unique
   class LogLevel(IntEnum):
      """
      The possible log levels for log messages.
      The higher the value, the more serious the
      log message.
      """
      DEBUG = 0
      INFO = auto()
      WARNING = auto()
      ERROR = auto()
   LogLevelsToStrings = {
      LogLevel.DEBUG: 'Debug',
      LogLevel.INFO: 'Info',
      LogLevel.WARNING: 'Warning',
      LogLevel.ERROR: 'Error'
   }
   StringsToLogLevels = {
      'Debug': LogLevel.DEBUG,
      'Info': LogLevel.INFO,
      'Warning': LogLevel.WARNING,
      'Error': LogLevel.ERROR
   }
   time = None
   logLevel = LogLevel.DEBUG
   @staticmethod
   def Init():
      Logger.time = Date.Now()
      config = Config.GetConfig()
      Logger.logLevel = Logger.StringsToLogLevels.get(
         config['Log']['Log level'], Logger.LogLevel.DEBUG
      )
   @staticmethod
   def LogToFile(message: str):
      """
      Log a given message to the log file path
      specified in the config.json.

      Args:
         message (str): The message to log to file.

      """
      logFileName = Logger.LOG_FILE.format(timestamp=Logger.time)
      config = Config.GetConfig()
      logFilePath = config['Log']['File path']
      logFilePath = os.path.join(logFilePath, logFileName)
      fileOpenType = 'w+'
      if (os.path.exists(logFileName)):
         fileOpenType = 'a+'
      try:
         os.makedirs(os.path.dirname(logFilePath))
         logFile = open(logFilePath, fileOpenType)
         logFile.write(message + '\n')
         logFile.close
      except IOError as err:
         print(err)
   @staticmethod
   def Error(tag: str, message: str):
      """
      Log an error message and, if enabled,
      log the error to a file.
      
      Args:
         tag (str): The tag for the log message.
         message (str): The message to log.
      """
      logMessage = Logger.LOG_MESSAGE_FORMAT.format(
         level=Logger.LogLevelsToStrings.get(Logger.LogLevel.ERROR, 'Unknown'),
         timestamp=datetime.now().strftime(Date.ISO_8601_FORMAT),
         tag=tag,
         message=message
      )
      config = Config.GetConfig()
      if (config['Log']['File logging enabled'] and Logger.logLevel <= Logger.LogLevel.ERROR):
         Logger.LogToFile(logMessage)
      print(logMessage)
   @staticmethod
   def Warning(tag: str, message: str):
      """
      Log a warning message and, if enabled,
      log the error to a file.
      
      Args:
         tag (str): The tag for the log message.
         message (str): The message to log.
      """
      logMessage = Logger.LOG_MESSAGE_FORMAT.format(
         level=Logger.LogLevelsToStrings.get(Logger.LogLevel.WARNING, 'Unknown'),
         timestamp=datetime.now().strftime(Date.ISO_8601_FORMAT),
         tag=tag,
         message=message
      )
      config = Config.GetConfig()
      if (config['Log']['File logging enabled'] and Logger.logLevel >= Logger.LogLevel.WARNING):
         Logger.LogToFile(logMessage)
      print(logMessage)
   @staticmethod
   def Info(tag: str, message: str):
      """
      Log an info message and, if enabled,
      log the error to a file.
      
      Args:
         tag (str): The tag for the log message.
         message (str): The message to log.
      """
      logMessage = Logger.LOG_MESSAGE_FORMAT.format(
         level=Logger.LogLevelsToStrings.get(Logger.LogLevel.INFO, 'Unknown'),
         timestamp=datetime.now().strftime(Date.ISO_8601_FORMAT),
         tag=tag,
         message=message
      )
      config = Config.GetConfig()
      if (config['Log']['File logging enabled'] and Logger.logLevel >= Logger.LogLevel.INFO):
         Logger.LogToFile(logMessage)
      print(logMessage)
   @staticmethod
   def Debug(tag: str, message: str):
      """
      Log a debug message and, if enabled,
      log the error to a file.
      
      Args:
         tag (str): The tag for the log message.
         message (str): The message to log.
      """
      logMessage = Logger.LOG_MESSAGE_FORMAT.format(
         level=Logger.LogLevelsToStrings.get(Logger.LogLevel.DEBUG, 'Unknown'),
         timestamp=datetime.now().strftime(Date.ISO_8601_FORMAT),
         tag=tag,
         message=message
      )
      config = Config.GetConfig()
      if (config['Log']['File logging enabled'] and Logger.logLevel >= Logger.LogLevel.DEBUG):
         Logger.LogToFile(logMessage)
      print(logMessage)

#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Saku Rautio"
__email__ = "sakupetterirautio@gmail.com"
__date__ = "2020-02-02"

__license__ = "MIT"
__version__ = "1.0.0"

from datetime import datetime

class Date:
   """
   This class provides helpers for date stuff.
   For example, converting dates to strings
   and strings to dates.
   """
   ISO_8601_FORMAT = '%Y_%m_%d-%H_%M_%S'
   GIT_STRING_FORMAT = '%a %b %d %H:%M:%S %Y %z'
   @staticmethod
   def ConvertDateToString(x: datetime) -> str:
      """
      Convert the given date into a ISO 8601
      formatted string.
      """
      return x.strftime(Date.ISO_8601_FORMAT)
   @staticmethod
   def ConvertStringToDateWithFormat(customFormat: str, x: str) -> datetime:
      """
      Convert the given date into a custom
      formatted string.
      """
      return datetime.strptime(x, customFormat)
   @staticmethod
   def ConvertGitStringToDate(x: str) -> datetime:
      """
      Convert the given string, which is formatted
      in the way Git formats dates, into a date.
      """
      return Date.ConvertStringToDateWithFormat(Date.GIT_STRING_FORMAT, x)
   @staticmethod
   def ConvertStringToDate(x: str) -> datetime:
      """
      Convert the given ISO 8601 formatted string
      into a date.
      """
      return datetime.strptime(x, Date.ISO_8601_FORMAT)
   @staticmethod
   def Now() -> datetime:
      """
      Get the current date and time information as
      an object of the datetime class.
      """
      return datetime.now()
   @staticmethod
   def NowAsString() -> str:
      """
      Convert the current date and time information as
      an object of the datetime class into a string
      formatted in the ISO 8601 format.
      """
      return Date.Now().strftime(Date.ISO_8601_FORMAT)

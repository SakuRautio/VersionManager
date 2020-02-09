#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Saku Rautio"
__email__ = "sakupetterirautio@gmail.com"
__date__ = "2020-02-02"

__license__ = "MIT"
__version__ = "1.0.0"

class User:
   """
   The class representation of a Git user.

   Attributes:
      name (str): The name of the user.
      email (str): The email of the user.
   """
   def __init__(self):
      self.name = ""
      self.email = ""

class Commit:
   """
   The class representation of a Git commit.

   Attributes:
      hash (str): The hash of the commit.
      author (User): The author of the commit.
      date (datetime.datetime): The timestamp of the commit.
      title (str): The title of the commit.
      message (str): The message of the commit.
   """
   def __init__(self):
      self.hash = ""
      self.author = User()
      self.date = None
      self.title = ""
      self.message = ""

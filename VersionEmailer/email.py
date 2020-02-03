#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Saku Rautio"
__email__ = "sakupetterirautio@gmail.com"
__date__ = "2020-02-02"

__license__ = "MIT"
__version__ = "1.0.0"

"""
This module provides structures for email stuff
and methods for using them.
"""

import smtplib
from email.message import EmailMessage
import os
import argparse

from error_code import ErrorCode
from git import Commit
from date import Date
from logger import Logger
from config import Config
LOG_TAG = "Email"
from version import Version

class HTMLEmail:
   COMMIT_LIST_ITEM_FORMAT = \
"""
<li>
   {title}
   {author}
   {date}
   {message}
</li>
"""
   @staticmethod
   def Send(templateFilePath: str, commits: list) -> ErrorCode:
      """
      Send an HTML email of the given commits in the style
      of the given template file. Use the email
      settings (subject, to, from) from the config.json.

      Args:
         templateFilePath (str): The path to the
         email template file.
         commits (list): The list of commits to
         list in the email.
      
      Returns:
         An ErrorCode object telling what the outcome of calling the function was.
      """
      config = Config.GetConfig()
      email = EmailMessage()
      email['Subject'] = config.get('Email').get('Subject')
      email['To'] = config.get('Email').get('To')
      email['From'] = config.get('Email').get('From')

      version = ""
      author = ""
      if (len(commits)):
         author = commits[0].author
         version = commits[0].tag

      textTemplate = ""
      htmlPart = ""
      try:
         with open(templateFilePath, 'r') as templateFile:
            textTemplate = templateFile.read()
      except IOError as err:
         Logger.Error(LOG_TAG, err)
         return ErrorCode.FILE_ERROR

      if (len(textTemplate) == 0):
         Logger.Error(LOG_TAG, "Template file empty")
         return ErrorCode.FILE_ERROR

      htmlPart = textTemplate.format(
         title=config.get('Email').get('Subject'), version=version, author=author,
         changeLog='\n'.join(list(map(
            lambda x: HTMLEmail.COMMIT_LIST_ITEM_FORMAT.format(
               title=x.title,
               author=x.author,
               date=Date.ConvertDateToString(x.date),
               message=x.message
            )
         )))
      )
      email.set_content(htmlPart)
      email.add_alternative(htmlPart, subtype='html')
      
      smtp = smtplib.SMTP(config.get('Email').get('SMTP').get('Server'))
      smtp.send(email)
      smtp.quit()

      return ErrorCode.OK

class TextEmail:
   COMMIT_LIST_ITEM_FORMAT = \
"""
   *  {title}
      {author}
      {date}
      {message}
"""
   @staticmethod
   def Send(templateFilePath: str, commits: list) -> ErrorCode:
      """
      Send a text email of the given commits in the style
      of the given template file. Use the email
      settings (subject, to, from) from the config.json.

      Args:
         templateFilePath (str): The path to the
         email template file.
         commits (list): The list of commits to
         list in the email.
      
      Returns:
        An ErrorCode object telling what the outcome of calling the function was.
      """
      email = EmailMessage()
      email['Subject'] = config.get('Email').get('Subject')
      email['To'] = config.get('Email').get('To')
      email['From'] = config.get('Email').get('From')

      version = ""
      author = ""
      if (len(commits)):
         author = commits[0].author
         version = commits[0].tag

      if not os.path.exists(templateFilePath):
         return ErrorCode.FILE_ERROR
      textTemplate = ""
      textPart = ""
      try:
         with open(templateFilePath, 'r') as templateFile:
            textTemplate = templateFile.read()
      except IOError as err:
         Logger.Error(LOG_TAG, err)
         return ErrorCode.FILE_ERROR

      if (len(textTemplate) == 0):
         Logger.Error(LOG_TAG, "Template file empty")
         return ErrorCode.FILE_ERROR

      textPart = textTemplate.format(
         title=config.get('Email').get('Subject'), version=version, author=author,
         changeLog='\n'.join(list(map(
            lambda x: TextEmail.COMMIT_LIST_ITEM_FORMAT.format(
               title=x.title,
               author=x.author,
               date=Date.ConvertDateToString(x.date),
               message=x.message
            )
         )))
      )
      email.set_content(textPart)
      
      try:
         smtp = smtplib.SMTP(config.get('Email').get('SMTP').get('Server'))
         smtp.send(email)
         smtp.quit()
      except Exception as err:
         Logger.Error(LOG_TAG, err)
         return ErrorCode.SMTP_ERROR

      return ErrorCode.OK

def HandleCommand(argv: list, argc: int) -> ErrorCode:
   """
   Handle a command given to this module

   Args:
      args (list): The given arguments.

   Returns:
      An ErrorCode object telling what the outcome of calling the function was.
   """
   result = ErrorCode.OK

   HELP_MESSAGE = \
   """
   The version file generator.

   Usage:
   version_manager.py email [optional] <command>

   Required:
   command  What you want the emailer to do. Available commands:
            send  Send an email based on the config.json.

   Optional:
   help    Print this message.
   """

   argv = argv[1:]
   argc = len(argv)

   if (argc < 1):
      Logger.Warning(LOG_TAG, 'No command given')
      return ErrorCode.TOO_FEW_ARGUMENTS
   
   if (argv[0] == 'help'):
      print(HELP_MESSAGE)
      return ErrorCode.OK
   if (argv[0] == 'send'):
      templateFilePath = config.get('Email').get('Email template file')
      commits = Version.GetCommitsBetweenIds('HEAD', 'HEAD~1')
      if (config.get('Email').get('Email as HTML')):
         result = HTMLEmail.Send(templateFilePath, commits)
      else:
         result = TextEmail.Send(templateFilePath, commits)

   return result

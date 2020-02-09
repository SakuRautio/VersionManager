#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Saku Rautio"
__email__ = "sakupetterirautio@gmail.com"
__date__ = "2020-02-02"

__license__ = "MIT"
__version__ = "1.0.0"

"""
This module produces a file based on the
project's Git tag. It takes the tag string (as an argument),
parses it into parts, and then writes the tag's fields
into to a specified file given as an
argument based on the template file 'version_file.template'.

Example tag: 1.2.1-rc.3
"""

import subprocess
from enum import IntEnum, unique
from string import Template

import numpy

from date import Date
from error_code import ErrorCode
from git import Commit, User
from logger import Logger

LOG_TAG = "Version"

class Version:
    """A representation of the version tag.
    
    Attributes:
        major    (int): The major version number of the version
        minor    (int): The minor version number of the version
        bug      (int): The bug version number of the version
        stage    (Version.Stage): The stage of the version
        stageRev (int): The stage revision of the version
    """
    @unique
    class Stage(IntEnum):
        """The different stages the program can be set.
        """
        UNKNOWN = -1,
        DEVELOPMENT = 0,
        RELEASE = 1,
        RELEASE_CANDIDATE = 2,
        ALPHA = 3,
        BETA = 4
    StageStringsToStages = {
        'dev': Stage.DEVELOPMENT,
        'rel': Stage.RELEASE,
        'rc': Stage.RELEASE_CANDIDATE,
        'alpha': Stage.ALPHA,
        'beta': Stage.BETA
    }
    def __init__(self):
        self.major = -1
        self.minor = -1
        self.bug = -1
        self.stage = self.Stage.UNKNOWN
        self.stageRev = -1
    def __str__(self):
        asDict = dict()
        asDict['major'] = self.major
        asDict['minor'] = self.minor
        asDict['bug'] = self.bug
        asDict['stage'] = self.stage
        asDict['stageRev'] = self.stageRev
        return '{0}'.format(asDict)
    @staticmethod
    def GetCurrentTag() -> str:
        """
        Get the current tag.

        Returns:
            The current tag.
        """
        output = subprocess.check_output(['git', 'describe', 'HEAD', '--abbrev=0', '--tags']).decode('utf-8')
        return str(output).replace('\r','').replace('\n','')
    @staticmethod
    def GetPreviousTag() -> str:
        """
        Get the previous tag.

        Returns:
            The previous tag.
        """
        output = subprocess.check_output(['git', 'describe', 'HEAD~1', '--abbrev=0', '--tags']).decode('utf-8')
        return str(output).replace('\r','').replace('\n','')
    @staticmethod
    def GetCurrentHash() -> str:
        """
        Get the hash of the current Git commit.

        Returns:
            The hash of the current commit.
        """
        output = subprocess.check_output(['git', 'rev-parse', '--verify', 'HEAD']).decode('utf-8')
        return str(output).replace('\r','').replace('\n','')
    @staticmethod
    def GetPreviousHash() -> str:
        """
        Get the hash of the previous Git commit.

        Returns:
            The hash of the previous commit.
        """
        output = subprocess.check_output(['git', 'rev-parse', '--verify', 'HEAD~1']).decode('utf-8')
        return str(output).replace('\r','').replace('\n','')
    @staticmethod
    def GetCommitsBetweenIds(newer: str, older: str) -> list:
        """
        Get a list of commits between two Git commits.
        
        Args:
            newer (str): The newer Git commit id for the comparison.
            older (str): The older Git commit id for the comparison.
        
        Returns:
            A list of commits.
        """
        commits = list()
        output = subprocess.check_output(['git', 'log', '{newer}...{older}'.format(newer=newer, older=older)]).decode('utf-8')
        if (len(output) < 1):
            return commits
        commitLog = str(output).split('\n')
        lineIndex = 0
        while (lineIndex < len(commitLog)):
            commitLogLine = str(commitLog[lineIndex])
            if (commitLogLine.startswith('commit')):
                # Commit log item startsexpression
                commit = Commit()
                # Get commit hash from the commit
                commit.hash = str(commitLog[lineIndex]).split(' ')[1]
                lineIndex = lineIndex + 1
                # Get "Author:", "{author's name} <{author's email}>"
                logLine = str(commitLog[lineIndex]).split(':', 1)[1].lstrip()
                user = User()
                user.name = logLine.split('<', 1)[0].rstrip(' ')
                user.email = logLine.split('<', 1)[1].lstrip().replace('\r','').replace('\n','')
                commit.author = user
                lineIndex = lineIndex + 1
                # Split "Date:   ", "{actual date}"
                logLine = str(commitLog[lineIndex]).split('Date:')[1]
                dateString = logLine = logLine.lstrip().replace('\r','').replace('\n','')
                commit.date = Date.ConvertGitStringToDate(dateString)
                # Skip extra line between date and commit title
                lineIndex = lineIndex + 2
                # Add the title to the commit but remove leading whitespace and trailing linefeed
                commit.title = str(commitLog[lineIndex]).lstrip().replace('\r','').replace('\n','')
                lineIndex = lineIndex + 1
                # Skip extra line between title and commit message
                lineIndex = lineIndex + 1
                # Commit message lasts until another commit message starts or the log ends
                commit.message = ""
                while (lineIndex < len(commitLog)):
                    if (str(commitLog[lineIndex]).startswith('commit')):
                        break
                    commit.message = commit.message + commitLog[lineIndex].lstrip()
                    lineIndex = lineIndex + 1
                commits.append(commit)
                break
            else:
                lineIndex = lineIndex + 1
        return commits
    @staticmethod
    def GenerateVersionFromString(versionString: str):
        """Create an instance of the Version class based on the tag string.
        
        Args:
            versionString (str): The Git tag in human readable format.
        
        Returns:
            An instance of the Version class.
        """
        version = Version()
        # Get major
        versionString = versionString.split('.', 1)
        version.major = int(versionString[0])
        if (len(versionString) < 2):
            return version
        # Get minor
        versionString = versionString[1].split('.', 1)
        version.minor = int(versionString[0])
        if (len(versionString) < 2):
            return version
        # Get bug
        versionString = versionString[1].split('-', 1)
        version.bug = int(versionString[0])
        if (len(versionString) < 2):
            return version
        # Get stage
        versionString = versionString[1].split('.', 1)
        version.stage = Version.StageStringsToStages.get(versionString[0], Version.Stage.UNKNOWN)
        if (len(versionString) < 2):
            return version
        # Get stage rev
        versionString = versionString[1]
        version.stageRev = int(versionString)
        if (len(versionString) < 2):
            return version
        # Return result
        return version
    @staticmethod
    def PushTagsToOrigin() -> ErrorCode:
        """
        Push existing Git tags to 'origin'.
        """
        output = subprocess.run(['git', 'push', 'origin', '--tags'], capture_output=True)
        if (output.returncode):
            Logger.Error(LOG_TAG, output.stdout)
            Logger.Error(LOG_TAG, output.stderr)
            return (ErrorCode.COMMAND_FAILED)
        return ErrorCode.OK

def HandleDiffCommand(argv: list, argc: int) -> ErrorCode:
    result = ErrorCode.OK

    HELP_MESSAGE = \
    """
    Get difference between Git versions.

    Usage:
    version_manager.py version get diff [optional] <from> <to>

    Required:
    from    The Git version to compare from
    to      The Git versionn to compare to

    Optional:
    help    Print this message
    """

    argv = argv[1:]
    argc = len(argv)

    fromArg = argv[0]
    if (fromArg == 'help'):
        print(HELP_MESSAGE)
        return result
    
    if (argc < 2):
        Logger.Error(LOG_TAG, 'Missing arguments')
        return ErrorCode.TOO_FEW_ARGUMENTS
    toArg = argv[1]
    
    responseTemplate = \
    """
    Commit difference between {0} and {1}:
    {2}
    """
    
    difference = Version.GetCommitsBetweenIds(fromArg, toArg)
    difference = ''.join(list(map(
        lambda commit:
"""
=========================================
Author: {0}
Date: {1}
Title: {2}
Message: {3}
=========================================
""".format(commit.author.name, Date.ConvertDateToString(commit.date), commit.title, commit.message),
        difference
    )))
    print(responseTemplate.format(fromArg, toArg, difference))

    return result
    
def HandleHashCommand(argv: list, argc: int) -> ErrorCode:
    result = ErrorCode.OK
    latestHash = Version.GetCurrentHash()
    print('Current commit hash: {0}'.format(latestHash))
    return result

def HandleTagCommand(argv: list, argc: int) -> ErrorCode:
    result = ErrorCode.OK
    latestTag = Version.GetCurrentTag()
    print('Latest tag: {0}'.format(latestTag))
    return result

def PrintHelpMessageGet(argv: list, argc: int) -> ErrorCode:
    result = ErrorCode.OK
    HELP_MESSAGE = \
    """
    The Git version information getter.

    Usage:
    version_manager.py version get [info] <info> [args]

    Required:
    info  What kind of information you wish to get. Available info:
            diff    Get commits between two versions
            hash    Get current commit hash
            tag     Get latest tag

    Optional:
    help    Print this message. (Only available for diff)
    Use 'version <info> help' to get information about that particular command.
    """
    print(HELP_MESSAGE)
    return result

def HandleGetCommand(argv: list, argc: int) -> ErrorCode:
    result = ErrorCode.OK

    argv = argv[1:]
    argc = len(argv)

    if (argc < 1):
        Logger.Warning(LOG_TAG, 'No command given')
        result = ErrorCode.UNKNOWN_COMMAND
    else:
        chosenInfo = argv[0]
        commandSwitcher = {
            'help': PrintHelpMessageGet,
            'diff': HandleDiffCommand,
            'hash': HandleHashCommand,
            'tag': HandleTagCommand
        }
        chosenCommand = commandSwitcher.get(chosenInfo, None)
        if (chosenCommand == None):
            Logger.Error(LOG_TAG, 'Unknown info given: {0}'.format(chosenInfo))
            result = ErrorCode.UNKNOWN_COMMAND
        else:
            result = chosenCommand(argv, argc)

    return result



def PrintHelpMessage(argv: list, argc: int) -> ErrorCode:
    result = ErrorCode.OK
    HELP_MESSAGE = \
    """
    The Git version helper.

    Usage:
    version_manager.py version [optional] <command> [args]

    Required:
    command  What you want the Git version helper to do. Available commands:
                push    Push existing tag to origin.
                get     Get information regarding the Git repo.

    Optional:
    help    Print this message.
    Use 'version <command> help' to get information about that particular command.
    """
    print(HELP_MESSAGE)
    return result

def HandleCommand(argv: list, argc: int) -> ErrorCode:
    """
    Handle a command given to this module

    Args:
        argv (list): The given arguments.
        argc (int): The count of given arguments.
    
    Returns:
        An ErrorCode object telling what the outcome of calling the function was.
    """
    result = ErrorCode.OK

    argv = argv[1:]
    argc = len(argv)

    if (argc < 1):
        Logger.Warning(LOG_TAG, 'No command given')
        result = ErrorCode.UNKNOWN_COMMAND
    else:
        PUSH_COMMAND_ID = 1
        commandSwitcher = {
            'help': PrintHelpMessage,
            'push': PUSH_COMMAND_ID,
            'get': HandleGetCommand
        }
        chosenCommand = commandSwitcher.get(argv[0], None)
        if (chosenCommand == None):
            Logger.Warning(LOG_TAG, 'Unknown command: {0}'.format(argv[0]))
            result = ErrorCode.UNKNOWN_COMMAND
        elif (chosenCommand == PUSH_COMMAND_ID):
            if (argc > 1):
                if (argv[1] == 'help'):
                    print('Pushes Git tags to origin.')
                else:
                    Logger.Warning(LOG_TAG, 'Unknown argument: {0}'.format(argv[1]))
                    result = ErrorCode.UNKNOWN_COMMAND
            else:
                result = Version.PushTagsToOrigin()
        else:
            result = chosenCommand(argv, argc)

    return result

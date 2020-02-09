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

from string import Template
import numpy
import os
import inspect
import argparse

from error_code import ErrorCode
from version import Version
from logger import Logger
LOG_TAG = "VersionFileGenerator"

def GenerateVersionFileFromVersion(version: Version, templateFilePath: str, versionFilePath: str) -> ErrorCode:
    """Generates a version file from a version object.
    
    Args:
        version (Version):
            An instance of the Version class, which is an object representation of the version tag string.
        templateFilePath (str): Path to the template file for a version file.
        versionFilePath (str):
            The path to the version source file which is to be generaated.
    
    Returns:
        An ErrorCode object telling what the outcome of calling the function was.
    """
    result = ErrorCode.UNKNOWN_ERROR
    
    # Create path to file
    versionFileDirectory = os.path.dirname(versionFilePath)
    if not os.path.exists(versionFileDirectory):
        try:
            os.makedirs(versionFileDirectory)
        except OSError as err:
            Logger.Error(LOG_TAG, 'Could not create directory for file: {0}'.format(err))
            result = ErrorCode.FILE_ERROR
            return result
   
    # Create version file
    versionFile = None
    try:
        versionFile = open(versionFilePath, 'w+')
    except IOError as err:
        versionFile.close()
        Logger.Error(LOG_TAG, 'Could not open version file: {0}'.format(err))
        result = ErrorCode.FILE_ERROR
        return result
    if (versionFile == None):
        Logger.Error(LOG_TAG, 'Some weird shit happened with the version file')
        return result

    with versionFile:
        versionFileTemplateString = None
        templateFile = None

        # Open template file
        try:
            templateFile = open(templateFilePath, 'r')
        except IOError as err:
            templateFile.close()
            Logger.Error(LOG_TAG, 'Could not open version file template file: {0}'.format(err))
            result = ErrorCode.FILE_ERROR
            return result
        if (templateFile == None):
            Logger.Error(LOG_TAG, 'Some weird shit happened with the version file template')
            return result

        # Read the template file contents to str object
        try:
            versionFileTemplateString = Template(templateFile.read())
        except IOError as err:
            Logger.Error(LOG_TAG, 'Could not read version file template file: {0}'.format(err))
        finally:
            templateFile.close()
        if (versionFileTemplateString == None):
            Logger.Error(LOG_TAG, 'Some weird shit happened with the version file template')
            return result

        # Write the version file
        versionFileString = versionFileTemplateString.safe_substitute(
            major=version.major, minor=version.minor,
            bug=version.bug, stage=version.stage.value, stageRev=version.stageRev)
        try:
            versionFile.write(versionFileString)
        except IOError as err:
            Logger.Error(LOG_TAG, 'Could not write to version file: {0}'.format(err))
            result = ErrorCode.FILE_ERROR
            return result
   
    result = ErrorCode.OK   
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

    HELP_MESSAGE = \
    """
    The version file generator.

    Usage:
    version_manager.py generate [optional] <template> <output>

    Required:
        template   Push existing tag to origin.
        output     Get information regarding the Git repo.

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
    
    if (argc < 2):
        Logger.Warning(LOG_TAG, 'Missing arguments')
        return ErrorCode.TOO_FEW_ARGUMENTS
    
    gitTagString = Version.GetCurrentTag()
    version = Version.GenerateVersionFromString(gitTagString)
    templateFilePath = argv[0]
    outputFilePath = argv[1]

    return GenerateVersionFileFromVersion(version, templateFilePath, outputFilePath)

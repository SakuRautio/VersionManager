# Version Manager

![](https://github.com/SakuRautio/VersionManager/workflows/CI/badge.svg)

A manager software library which can be integrated into any Git project to help automate versioning.

## Requirements

To install and run the packages needed by this program, your system will need to have:

   * a working *Python* [version 3.6 or higher][Python38 installation path]
   * the python3-pip package
   * Git installed (of course 🙄)

For Windows users, the installer luckily installs all the necessary stuff with the default values. But be sure it installs Python with *pip*, appends the installation directory to you $PATH, and also will remove the stupid 255 character max path limit.

## Version definition

The version is in the format `[major].[minor].[bug]-[stage].[stage revision]`.

The fields *major*, *minor*, *bug* and *stage revision* are all integers. The field *Stage* is a string and can be one of the following:

| Value | Stage |
|-------|-------|
| dev | development |
| rel | release |
| rc | release candidate |
| alpha | alpha |
| beta | beta |

For example: `1.2.1-rc.3`.

## Adding Version Manager to your project

Add it as a submodule with `git submodule add git@github.com:SakuRautio/VersionManager.git lib/VersionManager` or alternatively make a fork, make changes to the template file and python scripts and then add that project as a submodule.

You can then configure the Version Manager by editing the `config.json` file to your liking.

### Version File Generator

Converts a given Git tag into a version source file based on a template.

[More instructions](./VersionFileGenerator/README.md)

### Version Emailer

Sends an email with a given version and a changelog between the newest and the previous version.

[More instructions](./VersionEmailer/README.md)

---
Author: Saku Rautio   
Date: 2020-01-26   
License: MIT   

[Python38 installation path]: https://www.python.org/downloads/

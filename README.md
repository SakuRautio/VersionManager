# Version Manager

![](https://github.com/SakuRautio/VersionManager/workflows/CI/badge.svg)

A manager software library which can be integrated into any Git project to help automate versioning.

## Requirements

To install and run the packages needed by this program, your system will need to have:

   * Python [version 3.6 or higher][Python Download]
      * The Python3-pip package
      * The Python3-venv package
   * Git installed (of course 🙄)

For Windows users, the installer luckily installs all the necessary stuff with the default values. But be sure it installs Python with *pip*, appends the installation directory to you $PATH, and also will remove the stupid 255 character max path limit.

## Version definition

The version is in the format `[major].[minor].[bug]-[stage].[stage revision]`

The fields *major*, *minor*, *bug* and *stage revision* are all integers.

The field *stage* can be one of the following:

| Value | Stage |
|-------|-------|
| dev | development |
| rel | release |
| rc | release candidate |
| alpha | alpha |
| beta | beta |

For example: `1.2.1-rc.3`

## Adding Version Manager to your project

Add it as a submodule with `git submodule add git@github.com:SakuRautio/VersionManager.git <path to where you want to import it>` or alternatively make a fork, make changes to the template file and python scripts and then add that project as a submodule.

You can then configure the Version Manager by editing the `config.json` file in the directoy where you installed this library to your liking.

As there are required python packages to be installed, it is advised to use the *virtual environment* module.
Create a virtual environment to your current directory with `python3 -m venv <path to where you want to install the virtual environment>`.
Depending on the OS of the computer, run the command:
   * Windows: `<path to virtual environment>\Scripts\activate.bat`
   * Mac or Linux: `source <path to virtual environment>/bin/activate`
Now, you can install the required packages, which will be installed to the virtual environment with `python3 -m pip install -r requirements.txt`.

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

[Python Download]: https://www.python.org/downloads/

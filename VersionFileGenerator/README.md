# Version File Generator

Converts a given Git tag into a version source file based on a template.

## Usage in a project

Include the folder/files to the project in which you want to generate the version file.

Edit one of the `.template` files to suit your needs (or create one of you own) for what you want out of your Git version tag. Then call the generator script with `python3 .../VersionManager/version_manager.py generate <template file> <output file>`, which will create the *output file* according to the *template file*.

### Automating builds

When you have included this library into your project, add calling the script `version_file_generator.py` as a pre-build task. In the pre-build task, call the program like:

   1. `python3 -m pip install -r .../VersionManager/requirements.txt`
      * which will installl the requirements
   2. `python3 .../VersionManager/version_manager.py generate <templateFile> <outputFile>` where
      * `<templateFile>` is a template file to the script, containing fields for the generator to place Git version tag information attributes into.
      * `<outputFile>` is the file where to place the generated result.

# Version Emailer

Sends a Git version email to chosen recipients.
The email contains the changelog between chosen versions of a repository.

Available methods include tags, commit hashes and a raw count of commits (via `HEAD` like in `HEAD...HEAD~1`).

## Usage in a project

To use this program, you call *Version Manager* with the argument `email` and to send an email, by appending `send` to that command.

For all available parameters and options, run the *emailer* with the argument `help`.

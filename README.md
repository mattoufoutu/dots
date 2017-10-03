# dots

`dots` is yet another dotfiles management tool.

TODO: badges, plenty of them!

**THIS PROJECT IS IN ALPHA STAGE AND ISN'T USABLE YET**


## Features

* dotfiles stored in a central folder, and symlinked by `dots` to their real location
* handles versioning, Git knowledge should not be required to use `dots`
* can store multiple machines configuration (one branch per machine, named after its hostname)
* private files (SSH keys, configuration files containing credentials, etc.) can be stored encrypted


## Dependencies

TODO


## Installation

TODO


## Configuration

TODO


## Usage

TODO


## Files layout

* `dot` configuration file is `${HOME}/.dots.conf`
* dotfiles are stored in `${HOME}/dots/files`
* encrypted files are stored in `${HOME}/dots/encrypted`
* decrypted files (symlink targets) are not versioned and are stored in `${HOME}/dots/decrypted`
* GPG key ID is stored in `${HOME}/dots/gpgid`


## License

This project is licensed under the BSD 3-clause license.

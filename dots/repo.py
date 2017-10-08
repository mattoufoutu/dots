# coding: utf-8
import os
import platform
import shutil

from dots.logger import logger as log

from git import Repo


class DotRepository:
    """
    The `dots` repository object. Abstracts operations to the repository.
    """
    homedir = os.path.expanduser('~')

    def __init__(self, cfg):
        self.hostname = platform.node()
        self.path = ''
        self.gpg_key_id = ''
        self.ignored_files = []
        self.load_config(cfg)
        self.files_path = os.path.join(self.path, 'files')
        self.enc_files_path = os.path.join(self.path, 'encrypted')
        self.git_repo = None

    def load_config(self, cfg):
        """
        Assigns instance variables according to the configuration.
        :param cfg: a `ConfigParser` object that holds the configuration file content
        :return: None
        """
        log.debug('loading configuration file')
        section = cfg['DEFAULT']
        # use host-specific configuration, if any
        if self.hostname in cfg:
            section = cfg[self.hostname]
        self.path = os.path.abspath(os.path.expanduser(section['repo_dir']))
        self.gpg_key_id = section['gpg_key_id']
        self.ignored_files = section['ignored_files'].split(',')

    def check_repo(self):
        """
        Checks if the repository structure is valid, outputs an error and exits otherwise.
        :return: None
        """
        if not os.path.exists(self.path):
            log.error("no dots repository found at '{}'".format(self.path))
        if not os.path.exists(self.files_path):
            log.error("corrupted repository, the 'files' subfolder is missing")
        if not os.path.exists(self.enc_files_path):
            log.error("corrupted repository, the 'encrypted' subfolder is missing")
        if not os.path.exists(os.path.join(self.path, '.git')):
            log.error("corrupted repository, folder exists but is not versioned")
        self.git_repo = Repo(self.path)

    def rm_empty_folders(self, bottom, quiet=True):
        """
        Recursively (deepest to shortest) delete empty directories
        :param bottom: path from which deletion should start
        :param quiet: if False, asks for confirmation before deleting a folder
        :return: None
        """
        if not os.listdir(bottom):
            if not quiet:
                if not log.ask_yesno("delete empty folder '{}'?".format(bottom)):
                    return
            log.debug('deleting empty folder: {}'.format(bottom))
            os.rmdir(bottom)
            self.rm_empty_folders(os.path.split(bottom)[0], quiet=quiet)

    def cmd_init(self, _):
        """
        Initializes the dots repository.
        :return: None
        """
        log.info('initializing repository')
        # check if a repository already exists
        if os.path.exists(self.path):
            log.warning("the '{}' folder already exists".format(self.path))
            if log.ask_yesno('overwrite existing repository?'):
                shutil.rmtree(self.path)
                log.debug("creating folder: {}".format(self.path))
                os.mkdir(self.path)
            else:
                return
        log.debug('initializing Git repository')
        self.git_repo = Repo.init(self.path)
        # create .gitignore to avoid tracking decrypted files
        log.debug('adding decrypted files to Git ignore list')
        with open(os.path.join(self.path, '.gitignore'), 'a') as ofile:
            ofile.write('encrypted/*.cleartext\n')
        # create repository subfolders
        for dirpath in (self.files_path, self.enc_files_path):
            log.debug("creating folder: {}".format(dirpath))
            os.mkdir(dirpath)
            log.debug("adding .gitkeep file")
            with open(os.path.join(dirpath, '.gitkeep'), 'w') as _:
                pass
        log.debug('adding new files to Git')
        self.git_repo.index.add(self.git_repo.untracked_files)
        self.git_repo.index.commit('[dots] initial commit')

    def cmd_add(self, args):
        """
        Adds a new file to the repository.
        :param args: command-line arguments
        :return: None
        """
        log.info("adding '{}' to the repository".format(args.file))
        self.check_repo()
        # TODO: implement encryption
        if args.encrypted:
            raise NotImplementedError('encryption is not implemented yet')
        # check if file exists
        if not os.path.exists(args.file) or os.path.islink(args.file):
            log.error('file not found: {}'.format(args.file))
        # check if file is in a subfolder of the home directory
        if not args.file.startswith(self.homedir):
            log.error('file is not in a subfolder of {}'.format(self.homedir))
        if args.file.startswith(self.path):
            log.error("files inside the repository can't be added")
        # generate paths
        repo_relpath = args.file.replace(self.homedir, '')[1:]
        filename = os.path.split(args.file)[1]
        repo_subdirs = os.path.split(repo_relpath)[0].split(os.path.sep)
        repo_dir = os.path.join(self.files_path, *repo_subdirs)
        repo_file = os.path.join(repo_dir, filename)
        # move file into the repository and create symlink
        if not os.path.exists(repo_dir):
            log.debug('creating folder: {}'.format(repo_dir))
            os.makedirs(repo_dir)
        log.debug('moving {} to {}'.format(args.file, repo_file))
        shutil.move(args.file, repo_file)
        log.debug('creating symlink')
        os.symlink(repo_file, args.file)
        # add new file to Git
        log.debug('adding new file to Git')
        self.git_repo.index.add(self.git_repo.untracked_files)
        self.git_repo.index.commit('[dots] add {}'.format(args.file))

    def cmd_rm(self, args):
        """
        Removes a file from the repository.
        :param args: command-line arguments
        :return: None
        """
        log.info("removing '{}' from the repository".format(args.file))
        # check if file is inside the repository and if original file is indeed a symlink
        filepath = os.path.realpath(args.file)
        if not filepath.startswith(self.files_path):
            log.error('not a repository file: {}'.format(args.file))
        orig_path = filepath.replace(self.files_path, self.homedir)
        if not os.path.islink(orig_path):
            log.error('original file path is not a symlink: {}'.format(orig_path))
        if not args.quiet:
            if not log.ask_yesno("do you want to delete '{}'?".format(filepath)):
                exit(0)
        # move file to its original location
        log.debug('deleting symlink: {}'.format(orig_path))
        os.unlink(orig_path)
        log.debug('moving file to its original location')
        shutil.move(filepath, orig_path)
        # check for empty dirs to remove
        self.rm_empty_folders(os.path.split(filepath)[0], quiet=args.quiet)

    def cmd_sync(self, args):
        """
        Synchronizes repository content (adds missing symlinks and warns about conflicts).
        :param args: command-line arguments
        :return: None
        """
        raise NotImplementedError("the 'sync' command is not implemented yet")

    def cmd_publish(self, args):
        """
        Pushes the repository content to the remote Git repository.
        :param args: command-line arguments
        :return: None
        """
        raise NotImplementedError("the 'publish' command is not implemented yet")

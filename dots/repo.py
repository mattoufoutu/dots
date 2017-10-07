# coding: utf-8
import os
import platform
from shutil import rmtree

from dots.logger import logger as log

from git import Repo


class DotRepository:
    """
    The `dots` repository object. Abstracts operations to the repository.
    """
    def __init__(self, cfg):
        self.hostname = platform.node()
        self.path = ''
        self.gpg_key_id = ''
        self.ignored_files = []
        self.load_config(cfg)
        self.files_path = os.path.join(self.path, 'files')
        self.enc_files_path = os.path.join(self.path, 'encrypted')
        self.dec_files_path = os.path.join(self.path, 'decrypted')
        self.git_repo = None

    def load_config(self, cfg):
        """
        Assigns instance variables according to the configuration.
        :param cfg: a `ConfigParser` object that holds the configuration file content
        :return: None
        """
        log.debug('loading configuration file')
        section = cfg['DEFAULT']
        if self.hostname in cfg:
            section = cfg[self.hostname]
        self.path = os.path.expanduser(section['repo_dir'])
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
        if not os.path.exists(self.dec_files_path):
            log.error("corrupted repository, the 'decrypted' subfolder is missing")

    def cmd_init(self, args):
        """
        Initializes the dots repository.
        :param args: command-line arguments
        :return: None
        """
        log.info('initializing repository')
        if os.path.exists(self.path):
            log.warning("the '{}' folder already exists".format(self.path))
            if log.ask_yesno('overwrite existing repository?'):
                rmtree(self.path)
                log.debug("creating folder: {}".format(self.path))
                os.mkdir(self.path)
            else:
                return
        log.debug('initializing Git repository')
        self.git_repo = Repo.init(self.path)
        for dirpath in (self.files_path, self.enc_files_path, self.dec_files_path):
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
        raise NotImplementedError("the 'add' command is not implemented yet")

    def cmd_rm(self, args):
        """
        Removes a file from the repository.
        :param args: command-line arguments
        :return: None
        """
        raise NotImplementedError("the 'rm' command is not implemented yet")

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

# coding: utf-8


class DotRepository:
    def __init__(self, cfg):
        self.cfg = cfg

    def cmd_init(self, args):
        raise NotImplementedError("the 'init' is not implemented yet")

    def cmd_gpgid(self, args):
        raise NotImplementedError("the 'gpgid' command is not implemented yet")

    def cmd_add(self, args):
        raise NotImplementedError("the 'add' command is not implemented yet")

    def cmd_rm(self, args):
        raise NotImplementedError("the 'rm' command is not implemented yet")

    def cmd_sync(self, args):
        raise NotImplementedError("the 'sync' command is not implemented yet")

    def cmd_publish(self, args):
        raise NotImplementedError("the 'publish' command is not implemented yet")

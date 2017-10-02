# coding: utf-8


class DotRepository:
    def __init__(self, cfg):
        self.cfg = cfg

    def cmd_init(self, args):
        raise NotImplementedError

    def cmd_gpgid(self, args):
        raise NotImplementedError

    def cmd_add(self, args):
        raise NotImplementedError

    def cmd_rm(self, args):
        raise NotImplementedError

    def cmd_sync(self, args):
        raise NotImplementedError

    def cmd_publish(self, args):
        raise NotImplementedError

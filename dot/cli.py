# coding: utf-8

from argparse import ArgumentParser

from dot import VERSION
from dot.logger import logger
from dot.repo import DotRepository


def parse_args():
    parser = ArgumentParser(description='Configuration files manager')
    parser.add_argument(
        '-V', '--version',
        help='display program version and exit',
        action='store_true'
    )
    parser.add_argument(
        '-v', '--verbose',
        help='be more verbose',
        action='store_true'
    )
    subparsers = parser.add_subparsers(help='command help')

    parser_init = subparsers.add_parser('init', help='initialize dot repository')
    parser_init.set_defaults(func='init')

    parser_gpgid = subparsers.add_parser('gpgid', help='set GPG key to use for encryption/decryption')
    parser_gpgid.set_defaults(func='gpgid')
    parser_gpgid.add_argument(
        'keyid',
        help='GPG key ID',
        required=True
    )

    parser_add = subparsers.add_parser('add', help='add file to the repository')
    parser_add.set_defaults(func='add')
    parser_add.add_argument(
        'file',
        help='path of the file to add',
        required=True
    )
    parser_add.add_argument(
        '-e', '--encrypted',
        help='encrypt file for versioning',
        action='store_true'
    )

    parser_rm = subparsers.add_parser('rm', help='remove file from the repository')
    parser_rm.set_defaults(func='rm')
    parser_rm.add_argument(
        'file',
        help='path of the file to remove',
        required=True
    )
    parser_rm.add_argument(
        '-q', '--quiet',
        help='do not prompt for confirmation',
        action='store_true'
    )

    parser_sync = subparsers.add_parser('sync', help='synchronize config and repo files')
    parser_sync.set_defaults(func='sync')
    parser_sync.add_argument(
        '-f', '--force',
        help='overwrite possibly existing files',
        action='store_true'
    )

    parser_publish = subparsers.add_parser('publish', help='push files to remote repository')
    parser_publish.set_defaults(func='publish')
    parser_publish.add_argument(
        '-u', '--upstream',
        help='set new upstream repository'
    )
    parser_publish.add_argument(
        '-f', '--force',
        help='ignore possible conflicts and push anyway',
        action='store_true'
    )

    return parser.parse_args()


def main():
    repo = DotRepository()
    args = parse_args()
    if args.version:
        print(VERSION)
        exit(0)
    if args.verbose:
        logger.verbose = True
    method_name = 'cmd_{}'.format(args.func)
    method_obj = getattr(repo, method_name)
    method_obj(args)

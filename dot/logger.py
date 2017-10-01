# coding: utf-8

COLORS = {
    'green': '\033[22;32m',
    'boldblue': '\033[01;34m',
    'purple': '\033[22;35m',
    'red': '\033[22;31m',
    'boldred': '\033[01;31m',
    'normal': '\033[0;0m'
}


class Logger:
    def __init__(self):
        self.verbose = False

    @staticmethod
    def _print_msg(msg: str, color: str=None):
        if color is None or color not in COLORS:
            print(msg)
        else:
            print('{colorcode}{msg}\033[0;0m'.format(colorcode=COLORS[color], msg=msg))

    def debug(self, msg: str):
        if self.verbose:
            msg = '[DD] {}'.format(msg)
            self._print_msg(msg, 'normal')

    def info(self, msg: str):
        msg = '[II] {}'.format(msg)
        self._print_msg(msg, 'green')

    def warning(self, msg: str):
        msg = '[WW] {}'.format(msg)
        self._print_msg(msg, 'red')

    def error(self, msg: str, exitcode: int=255):
        msg = '[EE] {}'.format(msg)
        self._print_msg(msg, 'boldred')
        exit(exitcode)

    @staticmethod
    def ask(msg: str):
        msg = '[??] {}'.format(msg)
        question = '{colorcode}{msg} : \033[0;0m'.format(colorcode=COLORS['boldblue'], msg=msg)
        answer = input(question)
        return answer.strip()

    def ask_yesno(self, msg: str):
        valid_answers = {
            'y': True, 'yes': True,
            'n': False, 'no': False
        }
        question = '{} (y/n)'.format(msg)
        answer = ''
        while answer not in valid_answers:
            answer = self.ask(question).lower()
        return valid_answers[answer]


logger = Logger()

#! /usr/bin/env python3

#
#   pathcmd.py
#
#   Created by Kenta Suzuki on 7/9/18.
#   Copyright (c) 2018 Kenta Suzuki. Licensed under MIT.
#

'''
path completion for cmd module
'''

from cmd import Cmd
import os
import readline

name = 'pathcmd'

class PathCmd(Cmd):
    IGNORE = '-~'
    __hidden_methods = ('do_EOF',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        delims = readline.get_completer_delims()
        for i in self.IGNORE: delims = delims.replace(i, '', 1)
        readline.set_completer_delims(delims)

    # returns the directory of the argument being completed
    def _get_abspath(self, line, endidx):
        idx = line.rfind(' ', 0, endidx)
        abspath = os.path.abspath(line[idx+1:endidx])
        return (abspath + os.sep) if os.path.isdir(abspath) else abspath

    # returns list of completed file and directory names
    def _complete_path(self, text, line, begidx, endidx):
        if text == '..':
            return ['..' + os.sep]
        path = self._get_abspath(line, endidx)
        dir, rest = path.rsplit(os.sep, 1)
        dir += os.sep
        result = []
        for i in os.scandir(dir):
            if (i.name.startswith(rest)) if rest else (not i.name.startswith('.')):
                result.append(i.name + os.sep if i.is_dir() else i.name)
        return result

    # exits
    def do_EOF(self, args):
        print()
        return True

    # prevents completion of hidden methods
    def get_names(self):
        return [i for i in dir(self.__class__) if i not in self.__hidden_methods]

    # removes hidden methods from help
    def print_topics(self, header, cmds, cmdlen, maxcol):
        super().print_topics(header, [i for i in cmds if 'do_' + i not in self.__hidden_methods], cmdlen, maxcol)

    # do nothing when an emptyline is entered
    def emptyline(self):
        pass

if __name__ == '__main__':
    class Test(PathCmd):
        def do_shell(self, args):
            print('args =', args)

        def complete_test(self, *args):
            return self._complete_path(*args)

    test = Test()
    test.cmdloop()

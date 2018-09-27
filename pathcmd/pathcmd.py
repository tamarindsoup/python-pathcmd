
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
        for i in self.IGNORE:
            delims = delims.replace(i, '', 1)
        readline.set_completer_delims(delims)

    # returns the directory of the argument being completed
    def _get_fulltext(self, line, endidx):
        idx = line.rfind(' ', 0, endidx)
        return line[idx+1:endidx]

    # returns list of completed file and directory names
    def _complete_path(self, text, line, begidx, endidx):
        if text == '..':
            return ['..' + os.sep]
        path = self._get_fulltext(line, endidx)
        basename = os.path.basename(path)
        if not basename:
            dir = path
        else:
            dir = path.rsplit(basename, 1)[0]
        dir = os.path.abspath(dir)
        if dir[-1] != os.sep:
            dir += os.sep
        if not basename:
            return [
                i.name + os.sep if i.is_dir() else i.name
                for i in
                os.scandir(dir)
                if not i.name.startswith('.')
            ]
        else:
            return [
                i.name + os.sep if i.is_dir() else i.name
                for i in
                os.scandir(dir)
                if i.name.startswith(basename)
            ]

    # exits
    def do_EOF(self, args):
        print()
        return True

    # prevents completion of hidden methods
    def get_names(self):
        return [
            i
            for i in
            dir(self.__class__)
            if i not in self.__hidden_methods
        ]

    # removes hidden methods from help
    def print_topics(self, header, cmds, cmdlen, maxcol):
        super().print_topics(
            header,
            [
                i
                for i in
                cmds
                if 'do_' + i not in self.__hidden_methods
            ],
            cmdlen,
            maxcol
        )

    # do nothing when an emptyline is entered
    def emptyline(self):
        pass


if __name__ == '__main__':
    class Test(PathCmd):
        def do_test(self, args):
            print('args =', args)

        def complete_test(self, *args):
            return self._complete_path(*args)

    test = Test()
    test.cmdloop()

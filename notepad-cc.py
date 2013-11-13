#!/usr/bin/python

import sys
import getpass
import re
import requests
from optparse import OptionParser

class NotepadCC:
    def __init__(self, id, password=None):
        self.id = id
        self.password = password
        self.cookies = None
        self.note = None
        self.pattern = re.compile(
                '<textarea name="contents" id="contents" .*?>(.*)</textarea>', 
                re.IGNORECASE | re.MULTILINE | re.DOTALL)

    def get_note(self, refresh=False):
        if refresh or self.note is None:
            text = requests.get('http://notepad.cc/' + self.id, 
                    cookies=self.cookies).content
            m = self.pattern.findall(text)
            if len(m) > 0:
                self.note = m[0]
            else:
                # encrypted page, need password to login
                if self.password is None:
                    self.password = getpass.getpass()

                r = requests.post("http://notepad.cc/login/%s" % self.id,
                        data={'pad[name]':self.id, 'pad[password]':self.password})

                if r.status_code == 200:
                    if len(r.history) > 0:
                        # get the response cookie from redirection history
                        self.cookies = r.history[0].cookies.get_dict()

                    m = self.pattern.findall(r.text)
                    if len(m) > 0:
                        self.note = m[0]

        return self.note

    def set_note(self, note):
        requests.post('http://notepad.cc/ajax/update_contents/' + self.id,
                      data = {'contents': note}, cookies=self.cookies)
        self.note = note


if __name__ == '__main__':
    usage = "usage: %prog [options] [content]"
    parser = OptionParser(usage=usage)
    parser.add_option("-k", "--key", dest="key",
            help="http://notepad.cc/KEY", metavar="KEY")
    parser.add_option("-p", "--password", dest="password",
            help="password of the page", metavar="PASSWORD")
    parser.add_option("-a", "--append", dest="append", action="store_true", 
            default=False, help="append to current content instead of replace it")
    parser.add_option("-q", "--quite", dest="quite", action="store_true", 
            default=False, help="quite mode, no output")

    (options, args) = parser.parse_args()

    if not options.key:
        parser.print_help()
        sys.exit(0)

    # get content from cmd line or stdin
    content = None
    if len(args) > 0:
        content = " ".join(args)
    elif not sys.stdin.isatty():
        lines = sys.stdin.readlines()
        content = "".join(lines)


    notepad = NotepadCC(options.key, options.password)
    current_content = notepad.get_note()

    # update if content is available, otherwise just print the current content
    if content is not None:
        if options.append:
            content = current_content + content

        if not options.quite:
            print 'current: ', current_content
            print 'update: ', content

        notepad.set_note(content)
    else:
        print current_content

# vim: set et sw=4 ts=4:

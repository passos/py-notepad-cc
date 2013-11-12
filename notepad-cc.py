#!/usr/bin/python

import sys
import re
import requests
from optparse import OptionParser

class NotepadCC:
    def __init__(self, id):
        self.id = id
        self.note = None
        self.pattern = re.compile(
                '<textarea name="contents" id="contents" .*?>(.*)</textarea>', 
                re.IGNORECASE | re.MULTILINE | re.DOTALL)

    def get_note(self, refresh=False):
        if refresh or self.note is None:
            text = requests.get('http://notepad.cc/' + self.id).content
            m = self.pattern.findall(text)
            if len(m) > 0:
                self.note = m[0]

        return self.note

    def set_note(self, note):
        requests.post('http://notepad.cc/ajax/update_contents/' + self.id,
                      data = {'contents': note})
        self.note = note


if __name__ == '__main__':
    usage = "usage: %prog [options] [content]"
    parser = OptionParser(usage=usage)
    parser.add_option("-k", "--key", dest="key",
            help="http://notepad.cc/KEY", metavar="KEY")
    parser.add_option("-a", "--append", dest="append", action="store_true", 
            default=False, help="append to current content instead of replace it")
    parser.add_option("-q", "--quite", dest="quite", action="store_true", 
            default=False, help="quite mode, no output")

    (options, args) = parser.parse_args()

    if not options.key:
        print "Error: Need specify a key by -k option\n"
        parser.print_help()
        sys.exit(0)

    config = NotepadCC(options.key)

    current_content = config.get_note()

    if len(args) > 0:
        content = " ".join(args)
        if options.append:
            content = current_content + content

        if not options.quite:
            print 'current: ', current_content
            print 'update: ', content

        config.set_note(content)
    else:
        print current_content

# vim: set et sw=4 ts=4:

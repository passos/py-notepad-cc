py-notepad-cc
=============

A Python script to access http://notepad.cc

## Usage

    Usage: notepad-cc.py [options] [content]
    
    Options:
      -h, --help         show this help message and exit
      -k KEY, --key=KEY  http://notepad.cc/KEY
    
## Fetch
> Fetch the content of http://notepad.cc/ipaddress

    $ ./notepad-cc.py -k ipaddress
    192.168.1.100

## Update
> Update the content of http://notepad.cc/ipaddress

    $ ./notepad-cc.py -k ipaddress 192.168.1.101
    current:  192.168.1.100
    update:  192.168.1.101



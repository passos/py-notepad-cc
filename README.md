py-notepad-cc
=============

A Python script to access http://notepad.cc

## Usage

    Usage: notepad-cc.py [options] [content]
    
    Options:
      -h, --help         show this help message and exit
      -k KEY, --key=KEY  http://notepad.cc/KEY
      -p PASSWORD, --password=PASSWORD
                         password of the page
      -a, --append       append to current content instead of replace it
      -q, --quite        quite mode, no output
    
## Fetch
> Fetch the content of http://notepad.cc/ipaddress

    $ ./notepad-cc.py -k ipaddress
    192.168.1.100

## Update
> Update the content of http://notepad.cc/ipaddress

    $ ./notepad-cc.py -k ipaddress 192.168.1.101
    current:  192.168.1.100
    update:  192.168.1.101

## Append
> Update the content of http://notepad.cc/ipaddress

    $ ./notepad-cc.py -k ipaddress -a -q ' 192.168.1.102'
    $ ./notepad-cc.py -k ipaddress 
    192.168.1.101 192.168.1.102

## Access page by password
> update and fetch the page http://notepad.cc/test_password
    $ ./notepad-cc.py -k test_password 
    Password:  # input wrong password
    None
    $ ./notepad-cc.py -k test_password 
    Password:  # input right password
    ABC
    $ ./notepad-cc.py -k test_password -p 123456
    ABC
    $ ./notepad-cc.py -k test_password -p 123456 DEF
    current:  ABC
    update:  DEF
    $ ./notepad-cc.py -k test_password -p 123456 -a GHI
    current:  DEF
        update:  DEFGHI

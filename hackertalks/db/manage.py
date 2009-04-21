#!/usr/bin/env python
from migrate.versioning.shell import main

main(url='postgres://hackertalks@localhost/hackertalks',repository='db')

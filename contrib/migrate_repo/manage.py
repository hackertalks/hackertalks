#!/usr/bin/env python
from migrate.versioning.shell import main

main(repository='migrate_repo',url='postgres://hackertalks:hackertalks@localhost/hackertalks')
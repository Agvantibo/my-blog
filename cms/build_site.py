#!/usr/bin/env python3

builtin_metalist='./lists/site.mlist'
builtin_nav_path='./site/nav-units.html'

import os
import click

@click.command()
@click.option('-n', '--nav-units-path', type=click.Path(exists=True), required=False, help='Alternate existing nav elements file', metavar='file.html')
@click.argument('metalist', type=click.Path(exists=True), required=False)
def trunk(nav_units_path, metalist):
    if not nav_units_path:
        global builtin_nav_path
        nav_units_path = builtin_nav_path
    if os.path.exists(nav_units_path):
        click.confirm('A file at ' + nav_units_path +
                      ' already exists and will be overwritten, do you want to continue?', abort=True)
        nav_units = open(nav_units_path, 'w')
        nav_units.write('\n')
        nav_units.close()
    if not metalist:
        global builtin_metalist
        metalist = builtin_metalist
    cmds = open(metalist, 'r').readlines()
    for i in range(2):
        for i in cmds:
            os.system(i.rstrip('\n'))
            print('\n\n')

if __name__ == '__main__':
    trunk()

#!/usr/bin/env python3

from markdown import markdown as md
from os.path import exists, relpath
from htmlmin import minify
from html5print import HTMLBeautifier as hb
import yaml as ym
import click

builtin_elements = 'lists/post.list'
builtin_nav_units = 'site/nav-units.html'

@click.command()
@click.option('-t', '--title', required=True, help='Embedded title used for HTML generation and file naming', metavar='string')
@click.option('-y', '--assume-yes', type=click.BOOL, help='Automatically overwrites files, formats your hard drive and travels back in time to kill your grandma. Without confirmation.')
@click.option('-m/-r', '--minified-page/--readable-page', help='Toggle minification of page for development/ethical purposes', default=True)
@click.option('-e', '--elements-path', type=click.Path(exists=True), required=False, help='Alternative elements file to synthesize a different page', metavar='elements.list')
@click.option('-n', '--nav-units-path', type=click.Path(exists=True), required=False, help='Alternate existing nav elements file', metavar='file.html')
@click.argument('in_file', type=click.Path(exists=True))
@click.argument('out_file', type=click.Path(exists=True), required=False)
def trunk(in_file, out_file, title, assume_yes, elements_path, nav_units_path, minified_page):
    'Generate a sigle page from a markdown file IN_FILE using a template list and output the resulting HTML to OUT_FILE'
    if not exists('./.magic'): click.confirm('This script is supposed to be run from the website root. Are you sure you want to continue?', abort=True)
    if not out_file: out_file = 'site/posts/post_' + title + '.html'
    if not elements_path: global builtin_elements;    elements_path = builtin_elements
    if not nav_units_path: global builtin_nav_units;    nav_units_path = builtin_nav_units
    if exists(out_file) and not assume_yes: click.confirm('A file at ' + out_file + ' already exists, do you want to continue?', abort=True)
    
    in_md = open(in_file, 'r').read()
    out_html = open(out_file, 'w')
    elements = open(elements_path, 'r').readlines()
    nav_units = ''.join(open(nav_units_path, 'r').readlines())
    
    print('Synthesizing page using:\n    Elements at:', elements_path, '\n    Title:\t', '"' + title + '"', '\n    Content from:', in_file, '\n    Output:\t', out_file, '\n    Page is ', end='', sep='\t')
    if minified_page: print('minified')
    else: print('pretty-printed')
    print() 

    html_main = md(in_md)
    result_html = synthesize_page(elements, title, nav_units, nav_units_path, html_main, out_file)
    if minified_page: result_html = minify(result_html)
    else: result_html = hb.beautify(result_html, 2)
    out_html.write(result_html)


def synthesize_page(elements, title, nav_units, nav_units_path, html_main, out_file):
    result_html = ''
    for i in elements:
        wip_template = open(i.rstrip('\n'), 'r').read()
        print('Concatenating template:', i, end='')
        wip_template = wip_template.format(title=title, nav_units=synthesize_nav(nav_units, nav_units_path, title, out_file), main=html_main)
        result_html += wip_template + '\n'
    return result_html


def synthesize_nav(nav_units, nav_units_path, title, out_file):
    nav_nunit = '<li><span class="fa-li"><i class="fa-solid fa-angle-right"></i></span><h4><a href="{path}">{title}</a></h4></li>'.format(path=relpath(out_file, start='./site/'), title=title)
    if not  nav_nunit in nav_units:
        open(nav_units_path, 'w').write(nav_nunit + '\n' + nav_units + '\n')
    return open(nav_units_path, 'r').read().rstrip('\n')


if __name__ == '__main__':
    trunk()

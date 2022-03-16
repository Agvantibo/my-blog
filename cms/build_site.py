#!/usr/bin/env python3

import click
import os
import yaml as ym

@click.command()
@click.option('-r', '--override-root', help='Override the site generation root')
@click.option('-b', '--build-directory', help='Specifies the site build output directory')
@click.argument('site_config', type=click.Path(exists=True), required=False)
def trunk(override_root, build_directory, batch_config):
    

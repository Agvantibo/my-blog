#!/usr/bin/env python3

import click
import yaml as ym

@click.command()
@click.argument('batch_config', type=click.Path(exists=True), required=False)

def trunk(batch_config):
    pass

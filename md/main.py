import os
from contextlib import contextmanager
from pathlib import Path
import shutil
from tempfile import NamedTemporaryFile

import yaml
from invoke import Collection, Program, task

ns = Collection()


@contextmanager
def override_config_file(config_file, **kwargs):
    import pymdownx.superfences

    with open(config_file) as base:
        dd = yaml.load(base, Loader=yaml.FullLoader)

    dd.update(kwargs)
    with NamedTemporaryFile(mode='w', dir=config_file.parent) as fp:
        yaml.dump(dd, fp)
        yield fp.name


@task(
    name='serve',
    default=True,
    help={
        'docs-dir': 'path to directory containing markdown files',
        'dev-addr': '0.0.0.0:8000'
    },
)
def mkdocs_serve(ctx, docs_dir=None, dev_addr=None):
    """
    Serve some local markdown.
    """

    if docs_dir is None:
        docs_dir = '.'

    docs_dir_path = Path(docs_dir).absolute()

    if dev_addr is None:
        dev_addr = '0.0.0.0:8000'

    os.environ.setdefault('MKDOCS_PROJECT_DIR', str(Path(__file__).parent / 'mkdocs-example-tree'))
    os.environ.setdefault('MKDOCS_PROJECT_ENV', 'default')

    pp = Path(os.environ['MKDOCS_PROJECT_DIR'])
    unlink = []
    for ea in (
        pp / 'docs/css',
        pp / 'docs/js',
    ):
        link_name = docs_dir_path / ea.name
        link_name.unlink(missing_ok=True)
        link_name.symlink_to(ea)
        unlink.append(link_name)

    config_file = pp / 'mkdocs.yml'
    assert config_file.exists(), f'couldn\'t find {config_file}.'

    with override_config_file(config_file, docs_dir=str(docs_dir_path)) as tmp_config_file:
        ctx.run(f'mkdocs serve --dev-addr {dev_addr} --config-file {tmp_config_file}')

    for ea in unlink:
        ea.unlink(missing_ok=True)


ns.add_task(mkdocs_serve)

program = Program(namespace=ns)


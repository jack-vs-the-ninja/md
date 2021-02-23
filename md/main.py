import os
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile

import yaml
from invoke import Collection, Program, task

ns = Collection()


@contextmanager
def override_config_file(config_file, **kwargs):
    # TODO should use MKDOCS_PROJECT_ENV in the load stack. Reminder: 1. cli args 2. environ 3. yml merge

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

    os.environ.setdefault('MKDOCS_PROJECT_DIR', str(Path(__file__).parent.parent / 'example-config-dir'))
    os.environ.setdefault('MKDOCS_PROJECT_ENV', 'default')
    print(os.environ.get('MKDOCS_PROJECT_DIR') or 'NOT SET')

    config_file_basename = os.environ.get('MKDOCS_PROJECT_CONFIG_FILE_BASENAME') or 'mkdocs.yml'
    config_file = Path(os.environ['MKDOCS_PROJECT_DIR']) / config_file_basename
    assert config_file.exists(), f'couldn\'t find {config_file}. Create it or set MKDOCS_PROJECT_CONFIG_FILE_BASENAME'

    with override_config_file(config_file, docs_dir=str(docs_dir_path)) as tmp_config_file:
        ctx.run(f'mkdocs serve --dev-addr {dev_addr} --config-file {tmp_config_file}')


ns.add_task(mkdocs_serve)

program = Program(namespace=ns)


from setuptools import setup
from pathlib import Path


def glob_fix(package_name, glob):
    # this assumes setup.py lives in the folder that contains the package
    package_path = Path(f'./{package_name}').resolve()
    return [str(path.relative_to(package_path)) for path in package_path.glob(glob)]


setup(
    name='md',
    version='0.1.0',
    packages=['md'],
    install_requires=['invoke', 'mkdocs-material', 'mkdocs-exclude'],
    entry_points={
        'console_scripts': ['md = md.main:program.run']
    },
    package_data={'md': [*glob_fix('md', 'mkdocs-example-tree/**/*')]},
)

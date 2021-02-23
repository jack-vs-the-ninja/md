from setuptools import setup

setup(
    name='md',
    version='0.1.0',
    packages=['md'],
    install_requires=['invoke', 'mkdocs-material'],
    entry_points={
        'console_scripts': ['md = md.main:program.run']
    }
)

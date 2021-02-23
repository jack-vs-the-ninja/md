from setuptools import setup

setup(
    name='md',
    version='0.1.0',
    packages=['md'],
    install_requires=['invoke', 'mkdocs-material', 'mkdocs-exclude'],
    entry_points={
        'console_scripts': ['md = md.main:program.run']
    },
    include_package_data=True,  # use MANIFEST.in and copy those includes at install time. https://python-packaging.readthedocs.io/en/latest/non-code-files.html
)

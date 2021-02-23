# md

## What was done

I wrapped mkdocs serve in a python invoke program and installed it to the `md` virtualenv with `pip install -e <ABSOLUTE PATH TO MD PROJ>`.

Changes to this repo will affect the commands behavior.

To use it, you can simply `workon md` and then run `md serve ./my-docs-dir`.

Environment variables were set in ~/.bash_profile

MKDOCS_PROJECT_DIR
MKDOCS_PROJECT_ENV

but only MKDOCS_PROJECT_DIR is used at this time. The program uses the config file from MKDOCS_PROJECT_DIR and because the directories listed in mkdocs.yml are relative to the config file, we can "inherit" the themes and all the other overrides and just serve some markdown.

## TODOs

This repo should be hosted on cloud repositories and then we can install it to a virtualenv or any project by using the pip repo syntax.


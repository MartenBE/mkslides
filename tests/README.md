# README

Run in the root folder of the repo:

```bash
poetry run pytest
```

If you want to see the CLI output:

```bash
poetry run pytest --log-cli-level=INFO
```

Executing a single test:

```bash
poetry run pytest tests/navtree/test_navtree.py
```

## Simulate what a test does

The tests use a temporary directory (e.g. `/tmp` on Linux) to build the destination folder. This is to prevent cluttering your system with unnecessary files, and to improve speed and reduce SSD wear as these temporary directories are often stored by the OS in RAM.

However, sometimes you want to see what a test outputs. In that case, you can simulate the test by running following command from the root folder:

```bash
poetry run mkslides -s -d site -v build tests/navtree/docs -f tests/navtree/navtree-config.yml
```

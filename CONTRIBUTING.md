# Contributing guidelines

Thank you very much for contributing! Every help is welcome :slightly_smiling_face:.

## Workflow

If you have a bugfix, feel free to create a PR. If you have a feature request you can open an issue (or a PR if you already have code).

## Code guidelines

Here are some guidelines we ask to follow:

- The used language is English.
- Files should be UTF-8.
- Everything should come with as much [tests](./tests) as possible.
- The readability of code is very important.
- Formatting and linting is checked in the PR, please adhere to these checks. You can check the [CI/CD pipeline](./.github/workflows/test-deploy.yml) for the exact checks.
- If you create a new file, then you have to add the LICENSING annotation headers to adhere to the REUSE guidelines. If the file already exists and you just edited it, this is not necessary as the LICENSING annotation headers will already be present. The LICENSING annotation headers only name the creator and year of creation, other contributors are credited by the referral to https://github.com/MartenBE/mkslides/graphs/contributors.

    You can do this with the following command:

    ```bash
    uv run reuse annotate --recursive \
    --copyright "<your-name> and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)" \
    --copyright-prefix spdx-string-c \
    --license MIT \
    --year "<year-of-file-creation>" \
    "<file-or-folder>"
    ```

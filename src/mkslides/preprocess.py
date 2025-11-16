# SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

import importlib
import logging
from collections.abc import Callable

logger = logging.getLogger(__name__)

PREPROCESS_FUNCTION_NAME = "preprocess"


def load_preprocessing_function(script: str) -> Callable[[str], str] | None:
    spec = importlib.util.spec_from_file_location("preprocess_module", script)
    if spec is None:
        message = f"Could not create module spec from '{script}'"
        raise ImportError(message)

    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        message = f"Module spec for '{script}' has no loader"
        raise ImportError(message)

    spec.loader.exec_module(module)
    preprocess_func = getattr(module, PREPROCESS_FUNCTION_NAME, None)

    if not preprocess_func:
        message = f"Could not find '{PREPROCESS_FUNCTION_NAME}' function in '{script}'"
        raise ValueError(message)

    logger.debug(f"Loaded preprocessing function from '{script}'")

    return preprocess_func

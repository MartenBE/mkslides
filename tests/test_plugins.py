import re
from typing import Any

from tests.utils import (
    assert_html_contains,
    assert_html_contains_regexp,
    run_build_with_config,
)


def test_plugins(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    run_build_with_config(cwd, output_path, "test_plugins.yml")

    assert_html_contains(
        output_path / "someslides.html",
        [
            '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js-menu@2.1.0/menu.min.css" />',
            'menu: {"openButton": true, "openOnInit": true}',
            '<script src="https://cdn.jsdelivr.net/npm/reveal.js-menu@2.1.0/menu.min.js"></script>',
            '<script src="https://cdn.jsdelivr.net/npm/reveal.js-mermaid-plugin/plugin/mermaid/mermaid.min.js"></script>',
            '<script src="https://cdn.jsdelivr.net/npm/reveal-plantuml/dist/reveal-plantuml.min.js"></script>',
        ],
    )

    assert_html_contains_regexp(
        output_path / "someslides.html",
        re.compile(
            r"""Reveal\.initialize\({
                .*?
                plugins:\s+\[
                    .*?
                    RevealMermaid,
                    .*?
                    RevealMenu,
                    .*?
                \]
                .*?
            }\);
            """,
            re.VERBOSE | re.DOTALL,
        ),
    )

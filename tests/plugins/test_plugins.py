import re
from typing import Any

from tests.utils import (
    assert_html_contains,
    assert_html_contains_regexp,
    run_build_strict,
)


def test_plugins(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "plugins" / "slides"
    config_path = cwd / "plugins" / "plugins-config.yml"
    run_build_strict(cwd, input_path, output_path, config_path)

    assert_html_contains(
        output_path / "index.html",
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js-menu@2.1.0/menu.min.css" />',
    )
    assert_html_contains(
        output_path / "index.html",
        'menu: {"openButton": true, "openOnInit": true}',
    )
    assert_html_contains(
        output_path / "index.html",
        '<script src="https://cdn.jsdelivr.net/npm/reveal.js-menu@2.1.0/menu.min.js"></script>',
    )
    assert_html_contains(
        output_path / "index.html",
        '<script src="https://cdn.jsdelivr.net/npm/reveal.js-mermaid-plugin/plugin/mermaid/mermaid.min.js"></script>',
    )
    assert_html_contains(
        output_path / "index.html",
        '<script src="https://cdn.jsdelivr.net/npm/reveal-plantuml/dist/reveal-plantuml.min.js"></script>',
    )

    assert_html_contains_regexp(
        output_path / "index.html",
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

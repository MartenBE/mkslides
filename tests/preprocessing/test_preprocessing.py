# TODO: Fix this test
# def test_preprocessing(setup_paths: Any) -> None:
#     cwd, output_path = setup_paths
#     input_path = cwd / "preprocessing" / "slides"
#     config_path = cwd / "preprocessing" / "preprocessing-config.yml"
#     run_build_strict(cwd, input_path, output_path, config_path)

#     assert_html_contains_regexp(
#         output_path / "someslides-1.html",
#         re.compile(
#             r"""
#                 aaaaa-aaaa
#                 .*?
#                 aaa-aa
#                 .*?
#                 a
#             """,
#             re.VERBOSE | re.DOTALL,
#         ),
#     )

#     assert_html_contains_regexp(
#         output_path / "someslides-2.html",
#         re.compile(
#             r"""
#                 bbbbb-bbbb
#                 .*?
#                 bbb-bb
#                 .*?
#                 b
#             """,
#             re.VERBOSE | re.DOTALL,
#         ),
#     )

def preprocess(markdown_content: str) -> str:
    return markdown_content.replace("@", "b")

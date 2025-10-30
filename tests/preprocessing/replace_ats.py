import re


def preprocess(markdown_content: str) -> str:
    return re.sub(r"(@+)", r"atbegin\1atend", markdown_content)

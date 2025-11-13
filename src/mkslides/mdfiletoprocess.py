from dataclasses import dataclass
from pathlib import Path

from omegaconf import DictConfig


@dataclass
class MdFileToProcess:
    source_path: Path
    destination_path: Path
    slide_config: DictConfig
    markdown_content: str

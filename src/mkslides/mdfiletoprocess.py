from dataclasses import dataclass, field
from pathlib import Path

from omegaconf import DictConfig


@dataclass(unsafe_hash=True)
class MdFileToProcess:
    source_path: Path
    destination_path: Path
    slide_config: DictConfig = field(hash=False)
    markdown_content: str = field(hash=False)

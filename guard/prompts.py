from datetime import date
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field


class PromptConfig(BaseModel):
    model_config = ConfigDict(
        extra="forbid", 
        str_strip_whitespace=True)

    version: str = Field(pattern=r"^v[0-9]{3}$")
    created_at: date
    system_prompt: str = Field(min_length=1)


def load_prompt(path: str | Path) -> PromptConfig:
    prompt_path = Path(path)
    data = yaml.safe_load(prompt_path.read_text(encoding="utf-8"))

    if not isinstance(data, dict):
        raise ValueError(f"Prompt file must contain a YAML mapping: {prompt_path}")

    config = PromptConfig.model_validate(data)
    if prompt_path.stem != config.version:
        raise ValueError(
            f"Prompt version {config.version!r} does not match filename {prompt_path.name!r}"
        )

    return config

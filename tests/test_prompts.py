from datetime import date
from pathlib import Path

import pytest
from pydantic import ValidationError

from guard.prompts import load_prompt


PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "v001.yaml"


def test_load_versioned_prompt():
    config = load_prompt(PROMPT_PATH)

    assert config.version == "v001"
    assert config.created_at == date(2026, 9, 13)
    assert "billing" in config.system_prompt


@pytest.mark.parametrize(
    "contents",
    [
        'version: v001\ncreated_at: "2026-09-13"\n',
        'version: v001\ncreated_at: "2026-09-13"\nsystem_prompt: "   "\n',
        'version: v001\ncreated_at: "2026-09-13"\nsystem_prompt: Classify emails\nsystem_promt: typo\n',
        'version: v1\ncreated_at: "2026-09-13"\nsystem_prompt: Classify emails\n',
    ],
)
def test_reject_invalid_prompt_configuration(tmp_path, contents):
    path = tmp_path / "v001.yaml"
    path.write_text(contents, encoding="utf-8")

    with pytest.raises(ValidationError):
        load_prompt(path)


def test_reject_non_mapping_yaml(tmp_path):
    path = tmp_path / "v001.yaml"
    path.write_text("- not\n- a mapping\n", encoding="utf-8")

    with pytest.raises(ValueError, match="YAML mapping"):
        load_prompt(path)


def test_reject_filename_version_mismatch(tmp_path):
    path = tmp_path / "v002.yaml"
    path.write_text(
        'version: v001\ncreated_at: "2026-09-13"\nsystem_prompt: Classify emails\n',
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="does not match filename"):
        load_prompt(path)

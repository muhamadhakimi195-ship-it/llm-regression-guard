import pytest
from pydantic import ValidationError

from guard.feature import classify_email
from guard.contracts import EmailResult

class FakeBackend:
    def __init__(self, response_json):
        self.response_json = response_json
        self.calls= []

    def generate(self, *, email_text, system_prompt, model, output_schema):
        self.calls.append({
            "email_text": email_text,
            "system_prompt": system_prompt,
            "model": model,
            "output_schema": output_schema,
        })
        return self.response_json

def test_classify_email_uses_backend():
    fake= FakeBackend(
        '{"category":"billing","summary":"Customer requests a refund for a duplicate charge."}'
    )

    result= classify_email(
        email_text= "I was charge twice please refund the second charge",
        system_prompt="Test Prompt",
        model="fake-model",
        backend=fake,
    )

    assert isinstance(result, EmailResult)
    assert result.category == "billing"
    assert result.summary == "Customer requests a refund for a duplicate charge."
    assert len(fake.calls) == 1

def test_classify_email_rejects_invalid_backend_output():
    fake= FakeBackend(
        '{"category":"sales","summary":"Customer asks about pricing."}'
    )
    with pytest.raises(ValidationError):
        classify_email(
            email_text= "Can you explain your pricing?",
            system_prompt="Test Prompt",
            model="fake-model",
            backend=fake,
        )
    assert len(fake.calls) == 1
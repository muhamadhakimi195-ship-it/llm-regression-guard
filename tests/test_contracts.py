import pytest
from pydantic import ValidationError

from guard.contracts import EmailInput, EmailResult

def test_accept_valid_email():
    result= EmailResult(
        category="billing", 
        summary="Customer reports a duplicate charge"
        )

    assert result.category == "billing"

@pytest.mark.parametrize("text", ["", "   ", "\n\t"])
def test_rejects_blank_email(text):
    with pytest.raises(ValidationError):
        EmailInput(text=text)

def test_rejects_unknown_category():
    with pytest.raises(ValidationError):
        EmailResult(category="sales",
                     summary="Customer ask about pricing.",
        )

def test_rejects_unexpected_output_fields():
    with pytest.raises(ValidationError):
        EmailResult(
            category="billing",
            summary="Customer request a refund.",
            refund_approved=True,
        )

def test_rejects_blank_summary():
    with pytest.raises(ValidationError):
        EmailResult(category="billing", summary="  ") 

def test_rejects_summary_over_300_char():
    with pytest.raises(ValidationError):
        EmailResult(category="billing", summary="x"*301)


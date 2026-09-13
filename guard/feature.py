from guard.contracts import EmailInput, EmailResult


def classify_email(
    email_text: str,
    system_prompt: str,
    model: str,
    backend,
) -> EmailResult:
    email = EmailInput(text=email_text)

    raw_json = backend.generate(
        email_text=email.text,
        system_prompt=system_prompt,
        model=model,
        output_schema=EmailResult.model_json_schema(),
    )

    return EmailResult.model_validate_json(raw_json)

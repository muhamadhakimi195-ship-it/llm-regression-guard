from ollama import chat
from pathlib import Path

from guard.feature import classify_email
from guard.prompts import load_prompt


class OllamaBackend:
    def generate(self, *, email_text, system_prompt, model, output_schema):
        response = chat(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": email_text},
            ],
            format=output_schema,
            options={"temperature": 0, "num_ctx": 4096},
        )
        return response.message.content


MODEL = "qwen3:4b-instruct-2507-q4_K_M"
PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "v001.yaml"


def main():
    prompt_config = load_prompt(PROMPT_PATH)
    email_text = input("Enter your email message: ")
    result = classify_email(
        email_text=email_text,
        system_prompt=prompt_config.system_prompt,
        model=MODEL,
        backend=OllamaBackend(),
    )

    print("\nCategory:", result.category)
    print("Summary:", result.summary)


if __name__ == "__main__":
    main()

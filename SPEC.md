or Lesson 1, our eventual outcome is a function that accepts an email and returns a validated category and summary. We’ll reach it in three checkpoints:
1. Define the behavior and validate inputs and outputs.
2. Load a versioned prompt and test the feature with a fake model.
3. Connect your chosen provider and inspect eight real outputs.
Start with checkpoint 1 below. It should take roughly 45–90 minutes, depending on your Python experience.
1. Decide what “correct” means

        Consider this email:
        “I can’t log in after changing my password. Please help me recover my account.”

        Should it be technical or account?
        Both sound plausible without a rule. If we label it one way and prompt the model another way, our regression detector will report failures caused by an unclear specification.
        Use these initial routing rules:

    Category	Route here when the customer’s primary request concerns…
    billing	Charges, payments, invoices, or refunds
    account	Login, passwords, identity, profile, or account access
    technical	Broken product functionality, crashes, errors, or integrations, excluding account-access issues
    general	Product questions, feedback, or requests outside the other categories


For multiple issues, select the customer’s primary requested action. If there is no clear primary action, use the first explicit request as our initial tie-breaker.
That tie-breaker is a project decision. A real support team might prefer a different policy.
        Also define the summary:
        - One sentence in English.
        - Describe the customer’s problem or request.
        - Preserve key facts.
        - Do not invent causes, promises, or resolutions.

2. Prepare a small Python project
Create and open a new folder named model-regression-guard in your editor. Open its PowerShell terminal and check:
    py --version
Use Python 3.11 or newer. Then run:
    py -m venv .venv
    .\.venv\Scripts\python.exe -m pip install "pydantic>=2,<3" pytest

A virtual environment keeps this project’s dependencies separate from other projects. Using its Python executable directly also avoids needing to activate it. Python virtual environment documentation

Create these files manually in your editor:
model-regression-guard/
├── regression_guard/
│   ├── __init__.py
│   └── contracts.py
├── tests/
│   └── test_contracts.py
├── SPEC.md
└── .gitignore

3. Implement the input and output contracts

Understand each choice before continuing:
- Literal[...] describes the allowed category values.
- BaseModel makes Pydantic validate values when you create the object.
- extra="forbid" rejects unexpected fields, such as confidence or refund_approved.
- strict=True avoids accepting inappropriate values through automatic type conversion.
- str_strip_whitespace=True removes surrounding whitespace. Together with min_length=1, it rejects blank text.
- The length limits are our initial application limits, measured in characters. They are not token limits.
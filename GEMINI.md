# Project Conventions for Gemini CLI Agent

This document outlines the established coding styles, architectural patterns, and general conventions observed in the `blabla-tm` project. The Gemini CLI Agent should adhere to these guidelines when making any modifications or additions to the codebase.

## 1. General Project Structure

*   **Root Directory:** Contains `README.md`, `.gitignore`, and sub-project directories (`backend/`, `frontend/`).
*   **Configuration:** Environment variables are managed via `.env` files.
*   **Task Management:** Uses `.taskmaster/` for project tasks and reports.

## 2. Backend (Python/FastAPI)

*   **Language:** Python 3.10+
*   **Framework:** FastAPI
*   **Dependency Management:** `uv` (used for installing and managing Python dependencies).
*   **Database:** PostgreSQL
*   **ORM:** SQLAlchemy
*   **Migrations:** Alembic
*   **Authentication:** JWT (JSON Web Tokens)
*   **Password Hashing:** `passlib` (specifically bcrypt for password hashing).
*   **Type Hinting:** Extensive use of Python type hints for clarity and maintainability.
*   **Code Structure:**
    *   `backend/app/main.py`: Main FastAPI application instance, CORS configuration, and route inclusion.
    *   `backend/app/api/`: Contains API routers and endpoint definitions.
        *   `backend/app/api/endpoints/`: Specific API endpoints (e.g., `auth.py`, `users.py`).
        *   `backend/app/api/deps/`: Dependency injection functions.
    *   `backend/app/core/`: Core application components.
        *   `backend/app/core/config.py`: Application settings loaded from environment variables using `pydantic-settings`.
        *   `backend/app/core/database.py`: Database session management.
        *   `backend/app/core/security.py`: Security-related utilities (password hashing, JWT).
    *   `backend/app/models/`: SQLAlchemy declarative models defining database tables.
    *   `backend/app/schemas/`: Pydantic schemas for request body validation and response serialization.
*   **Naming Conventions:**
    *   Variables: `snake_case`
    *   Functions/Methods: `snake_case`
    *   Classes: `PascalCase`
    *   Constants: `UPPER_SNAKE_CASE` (e.g., `SECRET_KEY`, `PROJECT_NAME`)
*   **Docstrings:** Google-style docstrings are used for functions, methods, and classes, detailing arguments, return values, and exceptions.
*   **Imports:** Absolute imports are preferred (e.g., `from app.core.config import settings`).
*   **Linting/Formatting:** `ruff` is used for linting and formatting. After coding, run `ruff format` and `ruff check --fix`.
*   **Testing:** `pytest` is used for unit and integration tests.

## 3. Frontend (Svelte/Tailwind CSS)

*   **Framework:** Svelte
*   **Build Tool:** Vite
*   **Styling:** Tailwind CSS (utility-first approach).
*   **Language:** JavaScript (within Svelte components).
*   **Code Structure:**
    *   `frontend/src/App.svelte`: Main Svelte application component.
    *   `frontend/src/app.css`: Main CSS file, imports Tailwind directives.
    *   `frontend/src/lib/components/`: Directory for reusable Svelte components.
*   **Naming Conventions:**
    *   Svelte Components: `PascalCase` (e.g., `App.svelte`, `Layout.svelte`).
    *   Variables within `<script>` tags: `camelCase`.
*   **Styling Approach:** Primarily uses Tailwind CSS utility classes. Custom CSS is added in `app.css` if necessary, following a `@apply` pattern for Tailwind classes.
*   **Tailwind Plugins:** `@tailwindcss/forms` is in use.
*   **Linting/Formatting:** `eslint` and `prettier` are used for linting and formatting. After coding, run `npm run lint` and `npm run format`.

## 4. Git Conventions

*   `.gitignore` files are present in the root and sub-project directories to exclude unnecessary files from version control.

## 5. Tooling

*   **Backend Execution:** The backend is run using `uv`. For example, `uv run python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`.
*   **Frontend Execution:** Standard `npm` or `yarn` commands for Svelte/Vite projects (e.g., `npm install`, `npm run dev`).

## 6. General Guidelines for Agent

*   **Adherence:** Always prioritize adherence to the existing style and structure.
*   **Verification:** Before and after making changes, verify the project's build, linting, and testing commands.
*   **Clarity:** Ensure all changes are clear, concise, and maintain the project's readability.
*   **Testing:** For any new logic or significant changes, ensure corresponding unit or integration tests are added to maintain code quality and prevent regressions.
*   **Comments:** Add comments sparingly, focusing on *why* a piece of code exists or is complex, rather than *what* it does.

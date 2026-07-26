# CI / CD Guide — Smart Maintenance Assistant

## Single workflow

`.github/workflows/ci-cd.yml`

| Job | When | What it does |
|-----|------|--------------|
| **Test** | Every push / PR / manual run | Install deps, compile check, `pytest`, validate 20 benchmark questions (Python 3.11 & 3.12) |
| **Deploy Notes** | After tests on `main`/`master` | Prints Streamlit Cloud deploy reminders |

```text
Push / PR / manual
        │
        ▼
   Test (pytest)
        │
        ▼
   Deploy Notes (main only)
```

## One-time GitHub setup

```bash
git init
git add .
git commit -m "Initial commit: Smart Maintenance Assistant"
git branch -M main
git remote add origin https://github.com/<YOUR_USER>/<YOUR_REPO>.git
git push -u origin main
```

Open **Actions** → workflow **CI/CD** should run automatically.

> Never commit `.env`. Put API keys in Streamlit Cloud secrets.

## Streamlit Community Cloud

1. Connect the repo at [share.streamlit.io](https://share.streamlit.io)
2. Main file: `app.py`
3. Add secrets (`GROQ_API_KEY`, `LLM_PROVIDER`)

## Local checks (same as CI)

```bash
venv\Scripts\activate
pytest tests -q
```

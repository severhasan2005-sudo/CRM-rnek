# Racing Sponsor AI — Sponsorship CRM Prototype

A working **human-in-the-loop sponsorship CRM demo** for Formula Student teams, built with Streamlit and fictional data.

## What works
- Sponsor CRM dashboard
- Sample weekly meeting notes
- Pre-generated example suggestions with evidence and recommended next actions
- Human approval before updating sponsor status
- Session-based change history with CSV export

## What is not implemented yet
- Live AI inference (the suggestions are **pre-generated**, not AI-generated in real time)
- Word/PDF upload and automatic extraction
- Persistent SQLite storage (the demo uses Streamlit session state)

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy

1. Create a GitHub repository and upload `app.py`, `requirements.txt`, and `README.md`.
2. Visit https://share.streamlit.io/ and sign in with GitHub.
3. Choose your repository, branch, and `app.py`, then deploy.
4. Test the resulting public URL before submitting it.

All companies, people, dates, and meeting notes in this demo are fictional.

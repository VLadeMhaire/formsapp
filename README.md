# Forms App

A minimal Google-Forms-style app: FastAPI backend, PostgreSQL storage,
server-rendered HTML (no separate frontend build/deploy needed).

- `/` — form builder (create a form, get a shareable link)
- `/f/{form_id}` — the public fillable form (this is the link you share)
- `/f/{form_id}/results` — response table (add auth before sharing this widely)

## Run locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy .env.example to .env and fill in your real connection string.
# This only needs to be done once — it's picked up automatically on every run.
cp .env.example .env             # Windows: copy .env.example .env

uvicorn main:app --reload
```

Visit http://127.0.0.1:8000

**Note:** `.env` holds your database password — never commit it to git. If you
push this to GitHub, make sure `.env` is listed in `.gitignore` (it already is
in this project).

## Deploy for free (Render + Neon)

**1. Database — Neon (free Postgres, no credit card)**
1. Go to https://neon.tech, sign up, create a project.
2. Copy the connection string it gives you (starts with `postgresql://`).

**2. Code — push this folder to a GitHub repo**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/<you>/<repo>.git
git push -u origin main
```

**3. App hosting — Render (free web service)**
1. Go to https://render.com, sign up, click "New +" → "Web Service".
2. Connect your GitHub repo.
3. Settings:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Under "Environment", add `DATABASE_URL` = the Neon connection string from step 1.
5. Deploy. Render gives you a free URL like `https://your-app.onrender.com`.

That URL is your shareable base — forms look like:
`https://your-app.onrender.com/f/<form-id>`

**Note on the free tier:** Render's free web services spin down after ~15
minutes of inactivity and take a few seconds to wake back up on the next
request. Fine for casual sharing; if you need it always-on, look at Railway's
free trial credit or Fly.io's free allowances instead.

## Alternatives to this stack

- **Supabase** instead of Neon — also free Postgres, plus a built-in
  auth/storage layer if you outgrow this later.
- **Fly.io** instead of Render — free allowances, no forced spin-down, but a
  slightly more involved CLI-based deploy.
- **Railway** — very easy deploys, but the free tier is a limited monthly
  credit rather than an always-free tier.

## Where to take this next

- Add auth (e.g. a simple API key or Google login) so only you can see
  `/results` and `/` (the builder).
- Move `Base.metadata.create_all` to proper Alembic migrations once the
  schema stabilizes.
- Add form editing/deleting, response CSV export, and validation rules
  (min/max length, email format, etc.) if you need Forms-parity.

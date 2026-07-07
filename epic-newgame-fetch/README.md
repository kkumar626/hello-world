# Epic Free Games Notifier

Emails you the current week's free Epic Games Store game(s) every Friday
at 8:00 AM Malaysia time — completely free to run, using GitHub Actions.

## How it works
- A GitHub Actions "cron job" wakes up every Friday at 00:00 UTC (= 8:00 AM MYT)
- It runs `notify_free_games.py`, which calls Epic's own free-games API
  (the same one the store website uses) to find what's currently free
- It emails you the result via Gmail SMTP

## Setup (10 minutes, one-time)

### 1. Create a GitHub repo
- Go to github.com → New repository (can be private)
- Upload these files, keeping the folder structure:
  - `epic-newgame-fetch/notify_free_games.py`
  - `epic-newgame-fetch/README.md`
  - `.github/workflows/notify.yml` (must be in this exact path — GitHub Actions requires it)

### 2. Get a Gmail "App Password"
You can't use your normal Gmail password for this — Google requires an
App Password for scripts:
1. Go to https://myaccount.google.com/apppasswords
2. Sign in, create a new app password (name it "Epic Notifier")
3. Copy the 16-character password it gives you

(If you don't use Gmail, any SMTP provider works — just change the
`smtp.gmail.com` line in the script to your provider's SMTP server.)

### 3. Add secrets to your GitHub repo
In your repo: Settings → Secrets and variables → Actions → New repository secret.
Add these three:

| Secret name      | Value                                   |
|-------------------|------------------------------------------|
| `EMAIL_ADDRESS`   | The Gmail address sending the email      |
| `EMAIL_PASSWORD`  | The 16-character App Password from step 2 |
| `TO_EMAIL`        | The email address you want to receive it |

### 4. Test it
Go to the "Actions" tab in your repo → "Epic Free Games Notifier" →
"Run workflow" (this is the `workflow_dispatch` trigger) to send yourself
a test email immediately, without waiting for Friday.

### 5. Done
It will now run automatically every Friday at 8:00 AM Malaysia time.

## Notes
- GitHub Actions free tier gives you 2,000 minutes/month — this uses
  about 10 seconds/week, so it's effectively unlimited for this use case.
- If Epic changes their API structure in the future, the script may need
  a small tweak — the API has been stable for years, so this is unlikely
  to happen often.

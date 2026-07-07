"""
Checks Epic Games Store's free games API and emails the current week's
free game(s) to a recipient. Designed to run on a schedule (see the
GitHub Actions workflow in .github/workflows/notify.yml).
"""

import os
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EPIC_API = (
    "https://store-site-backend-static.ak.epicgames.com/"
    "freeGamesPromotions?locale=en-US&country=US&allowCountries=US"
)


def get_current_free_games():
    resp = requests.get(EPIC_API, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    elements = data["data"]["Catalog"]["searchStore"]["elements"]
    current_free = []

    for game in elements:
        promotions = game.get("promotions")
        if not promotions:
            continue
        offers = promotions.get("promotionalOffers") or []
        # A game is CURRENTLY free if promotionalOffers (not upcoming) is non-empty
        if offers:
            title = game.get("title", "Unknown title")
            slug = (
                game.get("catalogNs", {}).get("mappings", [{}])[0].get("pageSlug")
                or game.get("productSlug")
                or game.get("urlSlug")
            )
            url = (
                f"https://store.epicgames.com/en-US/p/{slug}"
                if slug
                else "https://store.epicgames.com/en-US/free-games"
            )
            current_free.append((title, url))

    return current_free


def build_email_body(games):
    if not games:
        return (
            "Couldn't find any currently-free games on Epic's API this run. "
            "Check https://store.epicgames.com/en-US/free-games manually."
        )
    lines = ["This week's free games on Epic Games Store:\n"]
    for title, url in games:
        lines.append(f"- {title}\n  {url}")
    return "\n\n".join(lines)


def send_email(subject, body):
    sender = os.environ["EMAIL_ADDRESS"]
    password = os.environ["EMAIL_PASSWORD"]
    recipient = os.environ["TO_EMAIL"]

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())


def main():
    games = get_current_free_games()
    body = build_email_body(games)
    subject = "🎮 This Week's Free Games on Epic Games Store"
    send_email(subject, body)
    print("Email sent.")
    print(body)


if __name__ == "__main__":
    main()

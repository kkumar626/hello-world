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

IMAGE_TYPES = ["DieselStoreFrontWide", "OfferImageWide", "Thumbnail"]


def get_cover_image(key_images):
    for preferred in IMAGE_TYPES:
        for img in key_images:
            if img.get("type") == preferred:
                return img.get("url")
    return None


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
            image_url = get_cover_image(game.get("keyImages", []))
            current_free.append((title, url, image_url))

    return current_free


def build_email_html(games):
    if not games:
        return """
        <html><body style="font-family:sans-serif;padding:24px;">
          <p>Couldn't find any currently-free games on Epic's API this run.</p>
          <p><a href="https://store.epicgames.com/en-US/free-games">Check manually →</a></p>
        </body></html>
        """

    cards = ""
    for title, url, image_url in games:
        img_tag = (
            f'<img src="{image_url}" alt="{title}" width="100%" '
            f'style="display:block;border-radius:8px 8px 0 0;">'
            if image_url
            else ""
        )
        cards += f"""
        <div style="background:#1a1a2e;border-radius:10px;margin-bottom:24px;overflow:hidden;max-width:480px;">
          {img_tag}
          <div style="padding:16px 20px 20px;">
            <h2 style="margin:0 0 12px;color:#ffffff;font-size:18px;">{title}</h2>
            <a href="{url}"
               style="display:inline-block;background:#0078f2;color:#ffffff;
                      text-decoration:none;padding:10px 20px;border-radius:6px;
                      font-weight:bold;font-size:14px;">
              Claim on Epic Games →
            </a>
          </div>
        </div>
        """

    return f"""
    <html>
    <body style="margin:0;padding:0;background:#0f0f1a;font-family:Arial,sans-serif;">
      <div style="max-width:560px;margin:0 auto;padding:32px 16px;">
        <div style="text-align:center;margin-bottom:28px;">
          <h1 style="color:#ffffff;font-size:22px;margin:0;">
            🎮 Free Games on Epic This Week
          </h1>
          <p style="color:#aaaaaa;margin:8px 0 0;font-size:14px;">
            Grab them before they're gone!
          </p>
        </div>
        {cards}
        <p style="text-align:center;color:#666666;font-size:12px;margin-top:32px;">
          <a href="https://store.epicgames.com/en-US/free-games"
             style="color:#0078f2;text-decoration:none;">
            View all free games on Epic →
          </a>
        </p>
      </div>
    </body>
    </html>
    """


def build_email_plaintext(games):
    if not games:
        return (
            "Couldn't find any currently-free games on Epic's API this run. "
            "Check https://store.epicgames.com/en-US/free-games manually."
        )
    lines = ["This week's free games on Epic Games Store:\n"]
    for title, url, _ in games:
        lines.append(f"- {title}\n  {url}")
    return "\n\n".join(lines)


def send_email(subject, html_body, plain_body):
    sender = os.environ["EMAIL_ADDRESS"]
    password = os.environ["EMAIL_PASSWORD"]
    recipient = os.environ["TO_EMAIL"]

    msg = MIMEMultipart("alternative")
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(plain_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())


def main():
    games = get_current_free_games()
    subject = "🎮 This Week's Free Games on Epic Games Store"
    send_email(subject, build_email_html(games), build_email_plaintext(games))
    print("Email sent.")
    print(build_email_plaintext(games))


if __name__ == "__main__":
    main()

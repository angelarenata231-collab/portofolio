import os

from dotenv import load_dotenv

load_dotenv()


def send_contact_email(name, email, subject, message):
    api_key = os.getenv("RESEND_API_KEY")
    if not api_key:
        print(f"[EMAIL MOCK] Message from {name} <{email}>: {subject}\n{message}")
        return True

    try:
        import resend

        resend.api_key = api_key
        resend.Emails.send(
            {
                "from": "Portfolio <onboarding@resend.dev>",
                "to": [os.getenv("CONTACT_EMAIL", "angelarenata231@gmail.com")],
                "subject": f"New inquiry: {subject}",
                "html": f"<p><strong>Name:</strong> {name}</p><p><strong>Email:</strong> {email}</p><p>{message}</p>",
            }
        )
        return True
    except Exception:
        print(f"[EMAIL MOCK] Message from {name} <{email}>: {subject}\n{message}")
        return False

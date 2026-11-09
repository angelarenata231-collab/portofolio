from flask import Blueprint, flash, redirect, request, url_for

from models import ContactMessage, db
from services.email_service import send_contact_email

contact_bp = Blueprint("contact", __name__)


@contact_bp.route("/contact", methods=["POST"])
def submit_contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    subject = request.form.get("subject", "Portfolio inquiry").strip()
    message = request.form.get("message", "").strip()

    if not all([name, email, message]):
        flash("Please complete all required fields before sending your message.", "error")
        return redirect(url_for("portfolio.home", _anchor="contact"))

    message_entry = ContactMessage(name=name, email=email, subject=subject, message=message)
    db.session.add(message_entry)
    db.session.commit()

    send_contact_email(name=name, email=email, subject=subject, message=message)

    flash("Your message has been sent. I will get back to you soon.", "success")
    return redirect(url_for("portfolio.home", _anchor="contact"))

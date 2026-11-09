
from io import BytesIO
from qrcode.image.svg import SvgPathImage

import qrcode

from flask import (
    Blueprint,
    render_template,
    redirect,
    send_file,
)

from sqlalchemy import or_

from models import Certificate, Experience, Profile, Project, Skill


portfolio_bp = Blueprint("portfolio", __name__)


# ==============================
# HALAMAN UTAMA PORTFOLIO
# ==============================

@portfolio_bp.route("/")
def home():

    profile = Profile.query.order_by(
        Profile.id.desc()
    ).first()

    skills = Skill.query.order_by(
        Skill.sort_order.asc(),
        Skill.id.asc()
    ).all()

    projects = Project.query.order_by(
        Project.featured.desc(),
        Project.created_at.desc()
    ).all()

    experiences = Experience.query.order_by(
        Experience.created_at.desc()
    ).all()

    # FILTER 4 SERTIFIKAT
    certificates = Certificate.query.filter(
        or_(
            Certificate.name.ilike(
                "%Oracle Academy Award of Completion - Database Design%"
            ),
            Certificate.name.ilike(
                "%Oracle Academy Award of Completion - Database Programming with SQL%"
            ),
            Certificate.name.ilike(
                "%Sertifikat Kompetensi Digital Marketing Sosial Media%"
            ),
            Certificate.name.ilike(
                "%Google for Education - Gemini Certified Student%"
            ),
        )
    ).order_by(
        Certificate.id.asc()
    ).all()

    return render_template(
        "index.html",
        profile=profile,
        skills=skills,
        projects=projects,
        experiences=experiences,
        certificates=certificates,

        linkedin_url=(
            profile.linkedin if profile
            else "https://linkedin.com"
        ),

        instagram_url=(
            profile.instagram if profile
            else "https://instagram.com"
        ),
    )


# ==============================
# HALAMAN CERTIFICATES
# REDIRECT KE SECTION DI HOME
# ==============================

@portfolio_bp.route("/certified")
def certified():

    return redirect("/#certificates")


# ==============================
# QR CODE SOCIAL MEDIA
# ==============================

@portfolio_bp.route("/qr/<platform>.png")
def qr_code(platform):

    profile = Profile.query.order_by(
        Profile.id.desc()
    ).first()

    url_map = {
        "linkedin": (
            profile.linkedin if profile and profile.linkedin
            else "https://linkedin.com"
        ),

        "instagram": (
            profile.instagram if profile and profile.instagram
            else "https://instagram.com"
        ),

        "github": (
            profile.github if profile and profile.github
            else "https://github.com/672023033-hub"
        ),
    }

    target_url = url_map.get(platform)

    if not target_url:
        return "Platform tidak ditemukan", 404

    qr = qrcode.QRCode(
        version=1,
        box_size=8,
        border=2
    )

    qr.add_data(target_url)
    qr.make(fit=True)

    img = qr.make_image(
    image_factory=SvgPathImage,
    fill_color="#0b1220",
    back_color="#ffffff"
    )

    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    return send_file(
    buffer,
    mimetype="image/svg+xml"
    )


# ==============================
# REDIRECT KE WEBSITE PROJECT
# ==============================

@portfolio_bp.route("/project/<int:project_id>")
def project_detail(project_id):

    project = Project.query.get_or_404(project_id)

    project_title = (project.title or "").lower()

    if "seminar" in project_title or "kafka" in project_title:
        return redirect(
            "https://uksw-workshop-platform-final.672023033.workers.dev/"
        )

    elif "peminjaman" in project_title or "laboratorium" in project_title:
        return redirect(
            "https://program-peminjaman-atmi-lvm5.vercel.app/login"
        )

    if project.link and project.link.startswith(
        ("https://", "http://")
    ):
        return redirect(project.link)

    return "Link project belum tersedia.", 404

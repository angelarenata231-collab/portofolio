from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from models import Certificate, ContactMessage, Experience, Profile, Project, Skill, db

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/")
@login_required
def dashboard():
    profile = Profile.query.first()
    projects = Project.query.count()
    skills = Skill.query.count()
    experience_count = Experience.query.count()
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    unread_messages = ContactMessage.query.filter_by(is_read=False).count()

    return render_template(
        "admin/dashboard.html",
        profile=profile,
        project_count=projects,
        skill_count=skills,
        experience_count=experience_count,
        messages=messages,
        unread_messages=unread_messages,
    )


@admin_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    profile = Profile.query.first()
    if request.method == "POST":
        profile.name = request.form.get("name", profile.name)
        profile.title = request.form.get("title", profile.title)
        profile.email = request.form.get("email", profile.email)
        profile.phone = request.form.get("phone", profile.phone)
        profile.location = request.form.get("location", profile.location)
        profile.bio = request.form.get("bio", profile.bio)
        profile.github = request.form.get("github", profile.github)
        profile.linkedin = request.form.get("linkedin", profile.linkedin)
        profile.instagram = request.form.get("instagram", profile.instagram)
        profile.profile_image = request.form.get("profile_image", profile.profile_image)
        profile.hero_image = request.form.get("hero_image", profile.hero_image)
        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("admin.profile"))

    return render_template("admin/profile.html", profile=profile)


@admin_bp.route("/skills", methods=["GET", "POST"])
@login_required
def skills():
    if request.method == "POST":
        skill = Skill(
            name=request.form.get("name", "").strip(),
            category=request.form.get("category", "Core").strip(),
            level=request.form.get("level", "Advanced").strip(),
            icon=request.form.get("icon", "sparkle").strip(),
            sort_order=int(request.form.get("sort_order", 1) or 1),
        )
        if skill.name:
            db.session.add(skill)
            db.session.commit()
            flash("Skill added.", "success")
        return redirect(url_for("admin.skills"))

    items = Skill.query.order_by(Skill.sort_order.asc(), Skill.id.asc()).all()
    return render_template("admin/skills.html", skills=items)


@admin_bp.route("/projects", methods=["GET", "POST"])
@login_required
def projects():
    if request.method == "POST":
        project = Project(
            title=request.form.get("title", "").strip(),
            category=request.form.get("category", "Branding").strip(),
            summary=request.form.get("summary", "").strip(),
            description=request.form.get("description", "").strip(),
            stack=request.form.get("stack", "").strip(),
            image=request.form.get("image", "").strip(),
            link=request.form.get("link", "#").strip(),
            featured=request.form.get("featured") == "on",
        )
        if project.title:
            db.session.add(project)
            db.session.commit()
            flash("Project added.", "success")
        return redirect(url_for("admin.projects"))

    items = Project.query.order_by(Project.created_at.desc()).all()
    return render_template("admin/projects.html", projects=items)


@admin_bp.route("/experiences", methods=["GET", "POST"])
@login_required
def experiences():
    if request.method == "POST":
        item = Experience(
            role=request.form.get("role", "").strip(),
            company=request.form.get("company", "").strip(),
            period=request.form.get("period", "").strip(),
            description=request.form.get("description", "").strip(),
        )
        if item.role and item.company:
            db.session.add(item)
            db.session.commit()
            flash("Experience added.", "success")
        return redirect(url_for("admin.experiences"))

    items = Experience.query.order_by(Experience.created_at.desc()).all()
    return render_template("admin/experiences.html", experiences=items)


@admin_bp.route("/certificates", methods=["GET", "POST"])
@login_required
def certificates():
    if request.method == "POST":
        item = Certificate(
            name=request.form.get("name", "").strip(),
            issuer=request.form.get("issuer", "").strip(),
            year=request.form.get("year", "").strip(),
            description=request.form.get("description", "").strip(),
        )
        if item.name:
            db.session.add(item)
            db.session.commit()
            flash("Certificate added.", "success")
        return redirect(url_for("admin.certificates"))

    items = Certificate.query.order_by(Certificate.year.desc(), Certificate.id.desc()).all()
    return render_template("admin/certificates.html", certificates=items)


@admin_bp.route("/contacts")
@login_required
def contacts():
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template("admin/contacts.html", messages=messages)


@admin_bp.route("/contacts/<int:message_id>/read", methods=["POST"])
@login_required
def mark_message_read(message_id):
    message = ContactMessage.query.get_or_404(message_id)
    message.is_read = True
    db.session.commit()
    flash("Message marked as read.", "success")
    return redirect(url_for("admin.contacts"))

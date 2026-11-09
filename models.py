
from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, default="Angela Renata Evlyne")
    title = db.Column(db.String(180), default="Mahasiswa Teknik Informatika")
    email = db.Column(db.String(120), default="angelarenata231@gmail.com")
    phone = db.Column(db.String(50), default="")
    location = db.Column(db.String(120), default="Salatiga, Indonesia")
    bio = db.Column(db.Text, default="")
    profile_image = db.Column(db.String(255), default="/static/images/profile-portrait.png")
    hero_image = db.Column(db.String(255), default="/static/images/hero-landing.svg")
    cv_url = db.Column(db.String(255), default="#")
    github = db.Column(db.String(255), default="https://github.com/672023033-hub")
    linkedin = db.Column(db.String(255), default="https://www.linkedin.com/in/angela-renata-evlyne-259766344")
    instagram = db.Column(db.String(255), default="https://www.instagram.com/angela.rntaa")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(80), default="Core")
    level = db.Column(db.String(40), default="Intermediate")
    icon = db.Column(db.String(80), default="sparkle")
    sort_order = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(80), default="Web Application")
    summary = db.Column(db.String(220), nullable=False)
    description = db.Column(db.Text, default="")
    stack = db.Column(db.String(200), default="")
    image = db.Column(db.String(255), default="/static/images/project-bloom.svg")
    link = db.Column(db.String(255), default="#")
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Experience(db.Model):
    __tablename__ = "experiences"

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(120), nullable=False)
    company = db.Column(db.String(120), nullable=False)
    period = db.Column(db.String(80), default="")
    description = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Certificate(db.Model):
    __tablename__ = "certificates"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(180), nullable=False)
    issuer = db.Column(db.String(120), default="")
    year = db.Column(db.String(20), default="")
    description = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(160), default="")
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class PortfolioSetting(db.Model):
    __tablename__ = "portfolio_settings"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80), unique=True, nullable=False)
    value = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


def get_default_profile():
    return Profile(
        name="Angela Renata Evlyne",
        title="Mahasiswa Teknik Informatika | Software Engineering",
        email="angelarenata231@gmail.com",
        location="Salatiga, Indonesia",
        bio=(
            "Mahasiswa S1 Teknik Informatika Universitas Kristen Satya Wacana "
            "dengan minat pada Rekayasa Perangkat Lunak. Memiliki pengalaman "
            "dalam asistensi dosen, organisasi, dan pengembangan aplikasi."
        ),
        profile_image="/static/images/profile-portrait.png",
        hero_image="/static/images/hero-landing.svg",
        github="https://github.com/672023033-hub",
        linkedin="https://www.linkedin.com/in/angela-renata-evlyne-259766344",
        instagram="https://www.instagram.com/angela.rntaa",
    )


def seed_data():
    if Profile.query.first() is None:
        db.session.add(get_default_profile())

    if User.query.filter_by(username="admin").first() is None:
        db.session.add(
            User(
                username="admin",
                password_hash=generate_password_hash("admin123"),
            )
        )

    skills = [
        ("Python", "Bahasa Pemrograman", "Intermediate"),
        ("Java", "Bahasa Pemrograman", "Intermediate"),
        ("PHP", "Bahasa Pemrograman", "Intermediate"),
        ("Kotlin", "Bahasa Pemrograman", "Intermediate"),
        ("HTML & CSS", "Bahasa Pemrograman", "Intermediate"),
        ("SQL", "Bahasa Pemrograman", "Intermediate"),
        ("Laravel", "Framework & Teknologi", "Intermediate"),
        ("Apache Kafka", "Framework & Teknologi", "Beginner"),
        ("Redis", "Framework & Teknologi", "Beginner"),
        ("Android Studio", "Tools", "Intermediate"),
        ("VS Code", "Tools", "Intermediate"),
        ("Postman", "Tools", "Intermediate"),
        ("Figma", "Tools", "Intermediate"),
        ("Microsoft Office", "Tools", "Intermediate"),
        ("Problem Solving", "Soft Skill", "Intermediate"),
        ("Communication", "Soft Skill", "Intermediate"),
        ("Teamwork", "Soft Skill", "Intermediate"),
    ]

    for index, (name, category, level) in enumerate(skills, start=1):
        skill = Skill.query.filter_by(name=name).first()

        if skill is None:
            db.session.add(
                Skill(
                    name=name,
                    category=category,
                    level=level,
                    sort_order=index,
                )
            )

    projects = [
        {
            "title": "Perancangan dan Implementasi Sistem Antrean Pendaftaran Seminar Menggunakan Apache Kafka dan Redis",
            "category": "Web Application",
            "summary": "Sistem antrean pendaftaran seminar menggunakan Kafka dan Redis.",
            "description": "Perancangan sistem antrean registrasi seminar dengan Apache Kafka dan Redis.",
            "stack": "Apache Kafka, Redis, Python, SQL",
            "featured": True,
        },
        {
            "title": "Website Peminjaman Barang Laboratorium",
            "category": "Web Application",
            "summary": "Website administrasi peminjaman barang laboratorium.",
            "description": "Pengembangan website pengelolaan data inventaris dan peminjaman.",
            "stack": "Laravel, PHP, SQL, HTML & CSS",
            "featured": True,
        },
    ]

    for item in projects:
        if Project.query.filter_by(title=item["title"]).first() is None:
            db.session.add(Project(**item))

    experiences = [
        {
            "role": "Asisten Dosen Pengantar Teknologi Informasi",
            "company": "Universitas Kristen Satya Wacana",
            "period": "2025",
            "description": "Mendampingi pembelajaran konsep dasar Teknologi Informasi.",
        },
        {
            "role": "Asisten Dosen Matematika Diskrit",
            "company": "Universitas Kristen Satya Wacana",
            "period": "2024-2025",
            "description": "Membimbing mahasiswa memahami materi Matematika Diskrit.",
        },
    ]

    for item in experiences:
        if Experience.query.filter_by(role=item["role"]).first() is None:
            db.session.add(Experience(**item))

    db.session.commit()

import os

from dotenv import load_dotenv

load_dotenv()


try:
    import cloudinary
    import cloudinary.uploader
    import cloudinary.api
except Exception:  # pragma: no cover
    cloudinary = None


def upload_to_cloudinary(file_storage, folder="portfolio"):
    if cloudinary is None:
        return {"secure_url": "", "error": "Cloudinary library not configured."}

    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME", ""),
        api_key=os.getenv("CLOUDINARY_API_KEY", ""),
        api_secret=os.getenv("CLOUDINARY_API_SECRET", ""),
    )

    if not all([os.getenv("CLOUDINARY_CLOUD_NAME"), os.getenv("CLOUDINARY_API_KEY"), os.getenv("CLOUDINARY_API_SECRET")]):
        return {"secure_url": "", "error": "Cloudinary environment is not configured."}

    result = cloudinary.uploader.upload(file_storage, folder=folder)
    return {"secure_url": result.get("secure_url"), "public_id": result.get("public_id")}

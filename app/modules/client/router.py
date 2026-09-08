from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    UploadFile,
    File,
    Form,
)
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import get_current_user
from app.modules.auth.models import User

from app.modules.client.schema import (
    ClientProfileResponse,
    ClientProfileUpdate,
)

from app.modules.client import crud


router = APIRouter(
    prefix="/client/profile",
    tags=["Client Profile"],
)


# =========================================================
# UPLOAD DIRECTORIES
# =========================================================

UPLOAD_DIR = Path("uploads/client")

PROFILE_DIR = UPLOAD_DIR / "profile"
COVER_DIR = UPLOAD_DIR / "cover"

PROFILE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

COVER_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# =========================================================
# IMAGE SETTINGS
# =========================================================

ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB


# =========================================================
# SAVE IMAGE
# =========================================================

async def save_image(
    file: UploadFile,
    directory: Path,
) -> str:

    # Check content type
    if not file.content_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file.",
        )

    # Check image type
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPG, PNG and WEBP images are allowed.",
        )

    extension = ALLOWED_IMAGE_TYPES[
        file.content_type
    ]

    # Read file
    contents = await file.read()

    # Check size
    if len(contents) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image size must be less than 5 MB.",
        )

    # Unique filename
    filename = (
        f"{uuid4().hex}{extension}"
    )

    filepath = directory / filename

    # Save file
    with filepath.open("wb") as buffer:
        buffer.write(contents)

    # Return URL/path
    return (
        f"/uploads/client/"
        f"{directory.name}/"
        f"{filename}"
    )


# =========================================================
# DELETE OLD IMAGE FILE
# =========================================================

def delete_image(
    image_url: str | None,
):
    if not image_url:
        return

    try:
        # URL:
        # /uploads/client/profile/abc.jpg
        #
        # Convert to:
        # uploads/client/profile/abc.jpg

        image_path = Path(
            image_url.lstrip("/")
        )

        if image_path.exists():
            image_path.unlink()

    except Exception as error:
        print(
            "Image delete error:",
            error,
        )


# =========================================================
# CREATE MY PROFILE
# =========================================================

@router.post(
    "/",
    response_model=ClientProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_profile(
    company_name: str = Form(""),
    bio: str = Form(""),
    location: str = Form(""),

    website: str | None = Form(None),
    industry: str | None = Form(None),
    company_size: str | None = Form(None),
    founded_year: int | None = Form(None),

    phone: str | None = Form(None),
    country: str | None = Form(None),
    timezone: str | None = Form(None),

    profile_image: UploadFile | None = File(None),
    cover_image: UploadFile | None = File(None),

    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # -----------------------------------------------------
    # CHECK EXISTING PROFILE
    # -----------------------------------------------------

    existing_profile = (
        crud.get_profile_by_user_id(
            db=db,
            user_id=current_user.id,
        )
    )

    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Client profile already exists.",
        )

    # -----------------------------------------------------
    # PROFILE IMAGE
    # -----------------------------------------------------

    profile_image_url = None

    if profile_image:
        profile_image_url = await save_image(
            profile_image,
            PROFILE_DIR,
        )

    # -----------------------------------------------------
    # COVER IMAGE
    # -----------------------------------------------------

    cover_image_url = None

    if cover_image:
        cover_image_url = await save_image(
            cover_image,
            COVER_DIR,
        )

    # -----------------------------------------------------
    # CREATE DATABASE PROFILE
    # -----------------------------------------------------

    return crud.create_profile(
        db=db,
        user_id=current_user.id,

        company_name=company_name,
        bio=bio,
        location=location,

        profile_image_url=profile_image_url,
        cover_image_url=cover_image_url,

        website=website,
        industry=industry,
        company_size=company_size,
        founded_year=founded_year,

        phone=phone,
        country=country,
        timezone=timezone,
    )


# =========================================================
# GET MY PROFILE
# =========================================================

@router.get(
    "/",
    response_model=ClientProfileResponse,
)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    profile = crud.get_profile_by_user_id(
        db=db,
        user_id=current_user.id,
    )

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client profile not found.",
        )

    return profile


# =========================================================
# UPDATE MY PROFILE
# =========================================================

@router.put(
    "/",
    response_model=ClientProfileResponse,
)
async def update_my_profile(
    company_name: str | None = Form(None),
    bio: str | None = Form(None),
    location: str | None = Form(None),

    website: str | None = Form(None),
    industry: str | None = Form(None),
    company_size: str | None = Form(None),
    founded_year: int | None = Form(None),

    phone: str | None = Form(None),
    country: str | None = Form(None),
    timezone: str | None = Form(None),

    profile_image: UploadFile | None = File(None),
    cover_image: UploadFile | None = File(None),

    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # -----------------------------------------------------
    # GET EXISTING PROFILE
    # -----------------------------------------------------

    existing_profile = (
        crud.get_profile_by_user_id(
            db=db,
            user_id=current_user.id,
        )
    )

    if not existing_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client profile not found.",
        )

    # -----------------------------------------------------
    # PREPARE UPDATE DATA
    # -----------------------------------------------------

    update_data: dict = {}

    if company_name is not None:
        update_data["company_name"] = company_name

    if bio is not None:
        update_data["bio"] = bio

    if location is not None:
        update_data["location"] = location

    if website is not None:
        update_data["website"] = website

    if industry is not None:
        update_data["industry"] = industry

    if company_size is not None:
        update_data["company_size"] = company_size

    if founded_year is not None:
        update_data["founded_year"] = founded_year

    if phone is not None:
        update_data["phone"] = phone

    if country is not None:
        update_data["country"] = country

    if timezone is not None:
        update_data["timezone"] = timezone

    # -----------------------------------------------------
    # NEW PROFILE IMAGE
    # -----------------------------------------------------

    if profile_image:

        new_profile_image = await save_image(
            profile_image,
            PROFILE_DIR,
        )

        # Delete old image
        delete_image(
            existing_profile.profile_image_url
        )

        update_data[
            "profile_image_url"
        ] = new_profile_image

    # -----------------------------------------------------
    # NEW COVER IMAGE
    # -----------------------------------------------------

    if cover_image:

        new_cover_image = await save_image(
            cover_image,
            COVER_DIR,
        )

        # Delete old image
        delete_image(
            existing_profile.cover_image_url
        )

        update_data[
            "cover_image_url"
        ] = new_cover_image

    # -----------------------------------------------------
    # UPDATE DATABASE
    # -----------------------------------------------------

    updated_profile = crud.update_profile(
        db=db,
        profile_id=existing_profile.id,
        profile=ClientProfileUpdate(
            **update_data
        ),
    )

    return updated_profile


# =========================================================
# DELETE MY PROFILE
# =========================================================

@router.delete("/")
def delete_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    existing_profile = (
        crud.get_profile_by_user_id(
            db=db,
            user_id=current_user.id,
        )
    )

    if not existing_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client profile not found.",
        )

    # Delete profile image
    delete_image(
        existing_profile.profile_image_url
    )

    # Delete cover image
    delete_image(
        existing_profile.cover_image_url
    )

    # Delete database profile
    crud.delete_profile(
        db=db,
        profile_id=existing_profile.id,
    )

    return {
        "message": "Client profile deleted successfully."
    }

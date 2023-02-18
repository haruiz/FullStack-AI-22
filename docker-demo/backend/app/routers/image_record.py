import os
from io import BytesIO
from typing import Optional

from PIL import Image as PILImage
from PIL import UnidentifiedImageError
from fastapi import Form, Depends, File, UploadFile, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session

import app.crud as crud
import app.schemas as schemas
from app.deps import get_db
from app.utils import ImageUtils
from app.utils.gcp_utils import GCPUtils

router = InferringRouter()


@cbv(router)
class ImageRecordRouter:
    # dependency injection
    db: Session = Depends(get_db)

    @router.get("/home")
    def home(self):
        """
        status endpoint
        :return:
        """
        return "ImageRecordRouter ready"

    @router.get("/")
    def get_images(self):
        """
        Get all images
        :return:
        """
        return crud.image_record.fetch_all(self.db)

    @router.post("/", response_model=schemas.ImageRecord)
    async def record_image(
        self,
        image: UploadFile = File(...),
        label: int = Form(),
        lat: Optional[float] = Form(default=None),
        lng: Optional[float] = Form(default=None),
    ):
        """
        Record an image
        :param label: the label for the image
        :param image: the image file
        :param lat: latitude
        :param lng: longitude
        :return:
        """
        # get the image from the request and convert it to a PIL image
        try:
            filename = image.filename
            image_in_db_already = crud.image_record.check_if_exists(self.db, filename)
            if image_in_db_already:
                raise Exception(f"Image with filename {filename} already exists")

            image_bytes: bytes = await image.read()
            if not image_bytes:
                raise Exception("No image provided")

            pil_image = PILImage.open(BytesIO(image_bytes))
            width, height = pil_image.size
            image_format = pil_image.format
            image_mode = pil_image.mode
            size = ImageUtils.human_readable_size(len(image_bytes))

            # upload the image to GCP
            bucket_name = os.getenv("GCP_BUCKET_NAME")
            blob_url = GCPUtils.upload_file_to_bucket(
                bucket_name, image_bytes, filename
            )
            image_record = schemas.ImageRecord(
                filename=filename,
                size=len(image_bytes),
                size_str=size,
                width=width,
                height=height,
                fmt=image_format,
                mode=image_mode,
                label_id=label,
                lat=lat,
                lng=lng,
                bucket=bucket_name,
                blob_name=filename,
            )
            print(f"Uploaded image to {blob_url}")
            image_record = crud.image_record.create(self.db, entity=image_record)
            return image_record
        except UnidentifiedImageError as e:
            raise HTTPException(status_code=400, detail="Invalid image provided")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

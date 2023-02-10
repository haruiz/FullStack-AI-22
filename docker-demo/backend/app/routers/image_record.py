import math
import os

from fastapi_utils.cbv import cbv
from typing import Optional

from fastapi import Form, Depends, File, UploadFile, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session
import app.crud as crud
import app.schemas as schemas
from app.deps import get_db
from PIL import Image as PILImage
from PIL import UnidentifiedImageError
from io import BytesIO

from app.utils import ImageUtils
from app.utils.gcp_utils import GCPUtils

router = InferringRouter()


@cbv(router)
class ImageRecordRouter:
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
        label: str = Form(),
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
            image_bytes: bytes = await image.read()
            if not image_bytes:
                raise HTTPException(status_code=400, detail="No image data")
            pil_image = PILImage.open(BytesIO(image_bytes))
            width, height = pil_image.size
            image_format = pil_image.format
            image_mode = pil_image.mode
            filename = image.filename
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
                label=label,
                lat=lat,
                lng=lng,
                bucket=bucket_name,
                blob_name=filename,
            )
            print(f"Uploaded image to {blob_url}")
            image_record = crud.image_record.create(self.db, entity=image_record)
            return image_record
        except UnidentifiedImageError as e:
            raise HTTPException(status_code=400, detail="Invalid image provided") from e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

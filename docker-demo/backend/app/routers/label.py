from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session

import app.crud as crud
import app.schemas as schemas
from app.deps import get_db
from fastapi import Depends, HTTPException

router = InferringRouter()


@cbv(router)
class LabelRouter:
    # dependency injection
    db: Session = Depends(get_db)

    @router.get("/home")
    def home(self):
        """
        status endpoint
        :return:
        """
        return "LabelRouter ready"

    @router.get("/")
    def get_labels(self):
        """
        Get all labels
        :return:
        """
        return crud.label.fetch_all(self.db)

    @router.post("/", response_model=schemas.Label)
    def create_label(self, label: schemas.LabelCreate):
        """
        Create a new label
        :param label:
        :return:
        """
        try:
            return crud.label.create(self.db, entity=label)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

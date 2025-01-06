from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api import dependencies
import crud
from schemas.stock_detail import StockDetailsCreate


router = APIRouter()


@router.post("/create", status_code=201)
def create_stock_details(
    obj_in: StockDetailsCreate, db: Session = Depends(dependencies.get_db)
):
    try:
        stock_details = crud.stock_details.create(db=db, obj_in=obj_in)
        return stock_details
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

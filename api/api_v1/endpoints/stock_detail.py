from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api import dependencies
import crud
from schemas.stock_detail import StockDetailsCreate


router = APIRouter()


@router.get("", status_code=201)
def create_stock_details(db: Session = Depends(dependencies.get_db)):
    """
    Create stock details for all items.
    """
    try:
        stock_details = crud.stock_details.create(db=db)
        return stock_details
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

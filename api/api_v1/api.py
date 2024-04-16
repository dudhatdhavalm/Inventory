from fastapi import APIRouter, Depends
from core.security import reusable_oauth2
from api.api_v1.endpoints import auth , user, supplier, bank_detail, contact_detail, item, inward

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/user",
                          tags=["user"], dependencies=[Depends(reusable_oauth2)])
api_router.include_router(supplier.router, prefix="/supplier",
                          tags=["supplier"], dependencies=[Depends(reusable_oauth2)])
api_router.include_router(bank_detail.router, prefix="/bank_detail",
                          tags=["bank_detail"], dependencies=[Depends(reusable_oauth2)])
api_router.include_router(contact_detail.router, prefix="/contact_detail",
                          tags=["contact_detail"], dependencies=[Depends(reusable_oauth2)])
api_router.include_router((item.router), prefix='/item', tags=['item'],dependencies=[Depends(reusable_oauth2)])
api_router.include_router((inward.router), prefix='/inward', tags=['inward'],dependencies=[Depends(reusable_oauth2)])

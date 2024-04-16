from fastapi import APIRouter
from .endpoints import auth , user , supplier, bank_detail , contact_detail, item, inward, outward
route_v1 = APIRouter()
route_v1.include_router((auth.router), prefix='/auth', tags=['auth'])
route_v1.include_router((user.router), prefix='/user', tags=['user'])
route_v1.include_router((supplier.router), prefix='/supplier', tags=['supplier'])
route_v1.include_router((bank_detail.router), prefix='/bank_detail', tags=['bank_detail'])
route_v1.include_router((contact_detail.router), prefix='/contact_detail', tags=['contact_detail'])
route_v1.include_router((item.router), prefix='/item', tags=['item'])
route_v1.include_router((inward.router), prefix='/inward', tags=['inward'])
route_v1.include_router((outward.router), prefix='/outward', tags=['outward'])
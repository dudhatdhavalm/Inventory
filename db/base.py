# Import all the models, so that Base has them before being
# imported by Alembic
from db.base_class import Base  # noqa
from db.base_class import BaseDefault  # noqa
from models.user import User
from models.supplier import Supplier
from models.bank_detail import BankDetail
from models.contact_detail import ContactDetail
from models.item import Item
from models.inward import Inward
from models.inward_return import InwardReturn
from models.outward import Outward
from models.outward_return import OutwardReturn
from models.roles import Roles
from models.permission import Permission
from models.role_permission import RolePermission
from models.stock import StockDetails
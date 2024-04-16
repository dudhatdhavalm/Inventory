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
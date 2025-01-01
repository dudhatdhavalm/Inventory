from typing import Any, Dict, List, Optional, Union, TypeVar
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from core.security import get_password_hash
from sqlalchemy import func, or_
from crud.base import CRUDBase
from models.bank_detail import BankDetail
from models.contact_detail import ContactDetail
from models.supplier import Supplier
from models.inward import Inward, InwardItem
from models.outward import Outward, OutwardItem
from db.base_class import Base
from schemas.supplier import SupplierCreate, SupplierUpdate
ModelType = TypeVar("ModelType", bound=Base)


class CRUDSupplier(CRUDBase[Supplier, SupplierCreate, SupplierUpdate]):
    def get(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Supplier]:
        return db.query(Supplier).filter(Supplier.status == 1).offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, *, id: int) -> Optional[Supplier]:
        return db.query(Supplier).filter(Supplier.id == id).first()

    # def get_by_bank_contact_id(self, db: Session, *, id: int):
    #     obj = db.query(Supplier.id,Supplier.name,Supplier.address,Supplier.city,Supplier.distance,Supplier.pincode,Supplier.station,Supplier.transport,BankDetail.IFSC_code,BankDetail.account_no,BankDetail.branch,BankDetail.bank,ContactDetail.contact_name,ContactDetail.mobile_number,ContactDetail.phone_number,ContactDetail.email,ContactDetail.pan_no,ContactDetail.gstin).join(BankDetail,BankDetail.supplier_id == Supplier.id).join(ContactDetail,ContactDetail.supplier_id == Supplier.id).filter(
    #             Supplier.id == id
    #             ).first()
    #     return obj

    def get_by_bank_contact_id(self, db: Session, *, id: int):
        supplier_data = db.query(Supplier.id,Supplier.name,Supplier.address,Supplier.city,Supplier.distance,Supplier.pincode,Supplier.station,Supplier.transport).filter(
                Supplier.id == id,Supplier.status == 1
                ).first()
        
        bank_detail = bank_detail = db.query(BankDetail.IFSC_code,BankDetail.account_no,BankDetail.branch,BankDetail.bank).filter(
                BankDetail.supplier_id == id,BankDetail.status == 1
                ).first()

        contact_detail = contact_detail = db.query(ContactDetail.contact_name,ContactDetail.mobile_number,ContactDetail.phone_number,ContactDetail.email,ContactDetail.pan_no,ContactDetail.gstin).filter(
                ContactDetail.supplier_id == id,ContactDetail.status == 1
                ).first()
                
        supplier_dict = {
            "id": supplier_data.id,
            "name": supplier_data.name,
            "address": supplier_data.address,
            "city": supplier_data.city,
            "distance": supplier_data.distance,
            "pincode": supplier_data.pincode,
            "station": supplier_data.station,
            "transport": supplier_data.transport,
            "account_no": bank_detail.account_no if bank_detail else None,
            "branch": bank_detail.branch if bank_detail else None,
            "IFSC_code": bank_detail.IFSC_code if bank_detail else None,
            "bank": bank_detail.bank if bank_detail else None,
            "contact_name": contact_detail.contact_name if contact_detail else None,
            "mobile_number": contact_detail.mobile_number if contact_detail else None,
            "phone_number": contact_detail.phone_number if contact_detail else None,
            "email": contact_detail.email if contact_detail else None,
            "pan_no": contact_detail.pan_no if contact_detail else None,
            "gstin": contact_detail.gstin if contact_detail else None,
        }

        return supplier_dict
    
    def create(self, db: Session, *, obj_in: SupplierCreate, created_by=None) -> Supplier:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Supplier(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Supplier, obj_in: Union[Supplier, Dict[str, Any]], modified_by=None
    ) -> Supplier:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data, modified_by=modified_by)


    def get_all_supplier_items(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[dict]:
            # Query to fetch suppliers and their items (without aggregation)
            inward_results = (
                db.query(Supplier.name, InwardItem.name, InwardItem.quantity)
                .join(
                    Inward, Supplier.id == Inward.supplier_id, isouter=True
                )  # LEFT JOIN for Inward
                .join(
                    InwardItem, Inward.id == InwardItem.inward_id, isouter=True
                )  # LEFT JOIN for InwardItem
                .filter(Supplier.status == 1)
                .offset(skip)
                .limit(limit)
                .all()
            )

            # Fetch outward items and quantities
            outward_results = (
                db.query(Supplier.name, OutwardItem.name, OutwardItem.quantity)
                .join(
                    Outward, Supplier.id == Outward.supplier_id, isouter=True
                )  # LEFT JOIN for Outward
                .join(
                    OutwardItem, Outward.id == OutwardItem.outward_id, isouter=True
                )  # LEFT JOIN for OutwardItem
                .filter(Supplier.status == 1)
                .offset(skip)
                .limit(limit)
                .all()
            )

            # Debugging: print raw query results to check what is being fetched
            print("Inward Query Results:", inward_results)
            print("Outward Query Results:", outward_results)

            # Dictionary to store suppliers and their inward and outward items
            suppliers_with_items = {}

            # Process inward items
            for supplier_name, item_name, item_quantity in inward_results:
                print(
                    f"Processing Inward - Supplier: {supplier_name}, Item: {item_name}, Quantity: {item_quantity}"
                )

                if supplier_name not in suppliers_with_items:
                    suppliers_with_items[supplier_name] = {
                        "inward_items": [],
                        "outward_items": [],
                        "inward_stock": 0,  # Initialize inward total quantity
                        "outward_stock": 0,  # Initialize outward total quantity
                    }

                # Validate and add inward items for the supplier
                if (
                    item_name
                    and isinstance(item_quantity, (int, float))
                    and item_quantity >= 0
                ):
                    suppliers_with_items[supplier_name]["inward_items"].append(
                        {"name": item_name, "quantity": item_quantity}
                    )

                    # Add the item quantity to the inward total
                    suppliers_with_items[supplier_name]["inward_stock"] += item_quantity
                else:
                    print(
                        f"Invalid inward item quantity for {supplier_name} - Item: {item_name}, Quantity: {item_quantity}"
                    )

            # Process outward items
            for supplier_name, item_name, item_quantity in outward_results:
                print(
                    f"Processing Outward - Supplier: {supplier_name}, Item: {item_name}, Quantity: {item_quantity}"
                )

                if supplier_name not in suppliers_with_items:
                    suppliers_with_items[supplier_name] = {
                        "inward_items": [],
                        "outward_items": [],
                        "inward_stock": 0,  # Initialize inward total quantity
                        "outward_stock": 0,  # Initialize outward total quantity
                    }

                # Validate and add outward items for the supplier
                if (
                    item_name
                    and isinstance(item_quantity, (int, float))
                    and item_quantity >= 0
                ):
                    suppliers_with_items[supplier_name]["outward_items"].append(
                        {"name": item_name, "quantity": item_quantity}
                    )

                    # Add the item quantity to the outward total
                    suppliers_with_items[supplier_name]["outward_stock"] += item_quantity
                else:
                    print(
                        f"Invalid outward item quantity for {supplier_name} - Item: {item_name}, Quantity: {item_quantity}"
                    )

            # Preparing the final response
            formatted_results = []
            for supplier_name, supplier_data in suppliers_with_items.items():
                formatted_results.append(
                    {
                        "supplier_name": supplier_name,
                        "inward_items": (
                            supplier_data["inward_items"]
                            if supplier_data["inward_items"]
                            else None
                        ),
                        "inward_stock": supplier_data["inward_stock"],
                        "outward_items": (
                            supplier_data["outward_items"]
                            if supplier_data["outward_items"]
                            else None
                        ),
                        "outward_stock": supplier_data["outward_stock"],
                    }
                )

            return formatted_results


supplier = CRUDSupplier(Supplier)

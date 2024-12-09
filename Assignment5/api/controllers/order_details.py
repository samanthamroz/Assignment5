from sqlalchemy.orm import Session
from fastapi import status, Response
from Assignment5.api.models import models


def create(db: Session, order_detail):
    # Create a new instance of the Order model with the provided data
    db_order_details = models.OrderDetail(
        id=order_detail.id,
        amount=order_detail.amount
    )
    # Add the newly created Order object to the database session
    db.add(db_order_details)
    # Commit the changes to the database
    db.commit()
    # Refresh the Order object to ensure it reflects the current state in the database
    db.refresh(db_order_details)
    # Return the newly created Order object
    return db_order_details


def read_all(db: Session):
    return db.query(models.OrderDetail).all()


def read_one(db: Session, order_details_id):
    return db.query(models.OrderDetail).filter(models.OrderDetail.id == order_details_id).first()


def update(db: Session, order_details_id, order_details):
    # Query the database for the specific order to update
    db_order_details = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_details_id)
    # Extract the update data from the provided 'order' object
    update_data = order_details.model_dump(exclude_unset=True)
    # Update the database record with the new data, without synchronizing the session
    db_order_details.update(update_data, synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return the updated order record
    return db_order_details.first()


def delete(db: Session, order_details_id):
    # Query the database for the specific order to delete
    db_order_details = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_details_id)
    # Delete the database record without synchronizing the session
    db_order_details.delete(synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return a response with a status code indicating success (204 No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
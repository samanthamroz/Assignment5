from sqlalchemy.orm import Session
from fastapi import status, Response
from Assignment5.api.models import models


def create(db: Session, order_details):
    # Create a new instance of the Order model with the provided data
    db_order_details = models.OrderDetail(
        id=order_details.id,
        amount=order_details.amount
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


def read_one(db: Session, order_id):
    return db.query(models.OrderDetail).filter(models.OrderDetail.id == order_id).first()


def update(db: Session, order_id, sandwich):
    # Query the database for the specific order to update
    db_sandwich = db.query(models.OrderDetail).filter(models.OrderDetail.order_id == order_id)
    # Extract the update data from the provided 'order' object
    update_data = sandwich.model_dump(exclude_unset=True)
    # Update the database record with the new data, without synchronizing the session
    db_sandwich.update(update_data, synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return the updated order record
    return db_sandwich.first()


def delete(db: Session, order_id):
    # Query the database for the specific order to delete
    db_sandwich = db.query(models.OrderDetail).filter(models.OrderDetail.order_id == order_id)
    # Delete the database record without synchronizing the session
    db_sandwich.delete(synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return a response with a status code indicating success (204 No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
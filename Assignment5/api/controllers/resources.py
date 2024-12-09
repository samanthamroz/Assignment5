from sqlalchemy.orm import Session
from fastapi import status, Response
from Assignment5.api.models import models


def create(db: Session, resources):
    # Create a new instance of the Order model with the provided data
    db_resources = models.Resource(
        id=resources.id,
        item=resources.item,
        amount=resources.amount
    )
    # Add the newly created Order object to the database session
    db.add(db_resources)
    # Commit the changes to the database
    db.commit()
    # Refresh the Order object to ensure it reflects the current state in the database
    db.refresh(db_resources)
    # Return the newly created Order object
    return db_resources


def read_all(db: Session):
    return db.query(models.Resource).all()


def read_one(db: Session, order_id):
    return db.query(models.Resource).filter(models.Resource.id == order_id).first()


def update(db: Session, resource_id, resource):
    # Query the database for the specific order to update
    db_resources = db.query(models.Resource).filter(models.Resource.id == resource_id)
    # Extract the update data from the provided 'order' object
    update_data = resource.model_dump(exclude_unset=True)
    # Update the database record with the new data, without synchronizing the session
    db_resources.update(update_data, synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return the updated order record
    return db_resources.first()


def delete(db: Session, resource_id):
    # Query the database for the specific order to delete
    db_resources = db.query(models.Resource).filter(models.Resource.id == resource_id)
    # Delete the database record without synchronizing the session
    db_resources.delete(synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return a response with a status code indicating success (204 No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
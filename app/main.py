# Building REST APIs using FastAPI, SQLAlchemy & Uvicorn
# https://medium.com/@dassum/building-rest-apis-using-
# fastapi-sqlalchemy-uvicorn-8a163ccf3aa1
# By Suman Das
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.models import models, schemas
from app.models.db import get_db, engine
from app.models.repositories import ItemRepo, StoreRepo
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn


# Create FastAPI Instance
app = FastAPI(
    title='Sample FastAPI Application',
    description='Sample FastAPI Application with Swagger and SQLAlchemy',
    version='0.0.1',
)

# Create all the tables
models.Base.metadata.create_all(bind=engine)


# Add an Exception Handler for application
@app.exception_handler(Exception)
def validation_exception_handler(request: Request, err: str):
    base_error_message = f'Failed to execute: {request.method}: {request.url}'
    return JSONResponse(
        status_code=400,
        content={
            'message': f'{base_error_message}. Detail: {err}'
        }
    )

###############################################################################


# Start of Item's Endpoints
@app.post(
    '/items',
    tags=['Item'],
    response_model=schemas.Item,
    status_code=201
)
async def create_item(
        item_request: schemas.ItemCreate,
        db: Session = Depends(get_db),
):
    """
    Create an Item and store it in the database
    """
    db_item = ItemRepo.fetch_by_name(db, name=item_request.name)
    if db_item:
        raise HTTPException(status_code=400, detail='Item already exists!')

    return await ItemRepo.create(db=db, item=item_request)


@app.get(
    '/items',
    tags=['Item'],
    response_model=List[schemas.Item],
)
def get_all_items(name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all the Items stored in database
    """
    if name:
        items = []
        db_item = ItemRepo.fetch_by_name(db, name)
        items.append(db_item)
        return items
    else:
        return ItemRepo.fetch_all(db)


@app.get(
    '/items/{item_id}',
    tags=['Item'],
    response_model=schemas.Item,
)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """
    Get the Item with the given ID provided by User stored in database
    """
    db_item = ItemRepo.fetch_by_id(db, item_id)
    if db_item is None:
        raise HTTPException(
            status_code=404,
            detail='Item not found with the given ID'
        )

    return db_item


@app.delete(
    '/items/{item_id}',
    tags=['Item'],
)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    Delete the Item with the given ID provided by User stored in database
    """
    db_item = ItemRepo.fetch_by_id(db, item_id)
    if db_item is None:
        raise HTTPException(
            status_code=404,
            detail='Item not found with the given ID'
        )

    await ItemRepo.delete(db, item_id)

    return 'Item deleted successfully!'


@app.put(
    '/items/{item_id}',
    tags=['Item'],
    response_model=schemas.Item,
)
async def update_item(
        item_id: int,
        item_request: schemas.Item,
        db: Session = Depends(get_db)
):
    """
    Update an Item stored in database
    """
    db_item = ItemRepo.fetch_by_id(db, item_id)
    if db_item:
        update_item_encoded = jsonable_encoder(item_request)
        db_item.name = update_item_encoded['name']
        db_item.price = update_item_encoded['price']
        db_item.description = update_item_encoded['description']
        db_item.store_id = update_item_encoded['store_id']

        return await ItemRepo.update(db=db, item_data=db_item)
    else:
        raise HTTPException(
            status_code=404,
            detail='Item not found with the given ID'
        )
# End of Item's Endpoints

###############################################################################


# Start of Store's Endpoints
@app.post(
    '/stores',
    tags=['Store'],
    response_model=schemas.Store,
    status_code=201
)
async def create_store(
        store_request: schemas.StoreCreate,
        db: Session = Depends(get_db)
):
    """
    Create a Store and save it in the database
    """
    db_store = StoreRepo.fetch_by_name(db, name=store_request.name)

    if db_store:
        raise HTTPException(
            status_code=400,
            detail='Store already exists!'
        )

    return await StoreRepo.create(db=db, store=store_request)


@app.get(
    '/stores',
    tags=['Store'],
    response_model=List[schemas.Store],
)
def get_all_stores(name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all the Stores stored in database
    """
    if name:
        stores = []
        db_store = StoreRepo.fetch_by_name(db, name)
        stores.append(db_store)
        return stores
    else:
        return StoreRepo.fetch_all(db)


@app.get(
    '/stores/{store_id}',
    tags=['Store'],
    response_model=schemas.Store
)
def get_store(store_id: int, db: Session = Depends(get_db)):
    """
    Get the Store with the given ID provided by User stored in database
    """
    db_store = StoreRepo.fetch_by_id(db, store_id)

    if db_store is None:
        raise HTTPException(
            status_code=404,
            detail='Store not found with the given ID',
        )

    return db_store


@app.delete(
    '/stores/{store_id}',
    tags=['Store'],
)
async def delete_store(store_id: int, db: Session = Depends(get_db)):
    """
    Delete the Store with the given ID provided by User in database
    """
    db_store = StoreRepo.fetch_by_id(db, store_id)

    if db_store is None:
        raise HTTPException(
            status_code=404,
            detail='Store not found with the given ID'
        )

    await StoreRepo.delete(db, store_id)

    return 'Store deleted successfully!'
# End of Store's Endpoints

###############################################################################


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)

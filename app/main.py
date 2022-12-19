# Building REST APIs using FastAPI, SQLAlchemy & Uvicorn
# https://medium.com/@dassum/building-rest-apis-using-
# fastapi-sqlalchemy-uvicorn-8a163ccf3aa1
# By Suman Das
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app import models

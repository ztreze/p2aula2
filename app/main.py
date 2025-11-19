from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, column, integer, String
from sqlalchemy.orm import sessionmaker
import re

app = FastAPI(title="Sistema de Padronização de Nomes e Emails")

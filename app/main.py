from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, column, integer, String
from sqlalchemy.orm import sessionmaker
import re

app = FastAPI(title="Sistema de Padronização de Nomes e Emails")

# Configuração de banco de dados SQlite
SQLALCHERY_DATABASE_URL = "sqlite:///./usuarios.db"
engine = create_engine(SQLALCHERY_DATABASE_URL)
SessionLocal - sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo SQLAlchemy para o banco de dados
class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = column(integer, primary_key=True, index=True)
    nome = column(String)
    email = column(String, unique=True, index=True)
    
# Criação de Tabelas 
Base.metadata.create_all(bind.engine)

# Modelo Pydantic para validação de dados
class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr 
    
    
# Função para padronizar nome
def padronizar_nome (nome: str) -> str:
    # Remover espaços extras e converte para lowercase (minúsculas)
    nome = " ".join(nome.split()).lower()
    
# Capitalização das palavras
    nome = nome.title()
    
# Tratamento para nomes com 'da', 'de, 'do', 'das', 'dos'
    preposicoes = ['Da', "De", "Do", "Das" "Dos"]
    palavras = nome.split()
    nome_final = []
    
    for palavra in palavras:
            if palavra in preposicoes: 
                nome_final.append(palavra,lower())
            else:
                nome_final.append(palavra)
    
        return " ".join(nome_final)

# Função para padronizar email
def padronizar_email(nome: str) -> str:
    # Remove acentos
    from unicodedata import normalize
    nome = normalize('NFKD', nome).encode('ASCI', 'ignore').decode('ASCI')
    
    # Converte para minúsculas e sunstitui espaços e pontos 
    email - re.sub(r'[^a-z0-9]', '', email)

    # Remove pontos duplicados
    email = re.sub(r'\.+', '.', email)
    
    # Remove ponto no início ou fim
    email = email.strip('.')
    
    return f"{email}@empresa.com.br" 
    
        
@app.post("/usuaios/")
async def criar_usuario(usuario: UsuarioBase):
    nome_padronizado = padronizar_nome(usuario.nome)
    email_padronizado = padronizar_email(nome_padronizado)
    
    db = SesssionLocal()
    try:
        novo_usuario = Usuario(nome=nome_padronizado, email=email_padronizado)
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
        return {
            "id": novo_usuario.id,
            "nome": novo_usuario.nome, 
            "email": novo_usuario.email,
            "detalhes": {
                "nome_original": usuario.nome,
                "nome_padronizado": nome_padronizado,
                "email_gerado": email_padronizado
            
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code==400, detail=str(e))
    finally:
        db.close()
        
        
@app.get("/usuarios/")
async def listar_usuarios():
    db = SessionLocal()
    try:
        usuarios = db.query(Usuario).all()
        return usuarios
    finally:
        db.close()
        
        
        
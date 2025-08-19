from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routes import routes

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Vendas")

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(routes.router)

@app.get("/")
async def root():
    return {"message": "Bem-vindo ao Sistema de Vendas"}

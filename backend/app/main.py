from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine, SessionLocal
from .routes import routes
from .seed import seed_data

# Criar tabelas
Base.metadata.create_all(bind=engine)

# Inserir dados iniciais
db = SessionLocal()
try:
    # Verificar se já existem produtos
    if db.query(Base.metadata.tables["products"]).count() == 0:
        seed_data(db)
finally:
    db.close()

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

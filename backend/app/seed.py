from sqlalchemy.orm import Session
from .models.models import Product

def seed_data(db: Session):
    produtos = [
        {
            "nome": "Caderno Universitário 10 Matérias",
            "descricao": "Caderno com 200 folhas, capa dura e espiral",
            "preco": 25.90,
            "estoque": 50,
            "categoria": "papelaria",
            "sku": "CAD-UNI-10"
        },
        {
            "nome": "Estojo Escolar Completo",
            "descricao": "Kit com lápis, canetas, borracha e apontador",
            "preco": 35.50,
            "estoque": 30,
            "categoria": "papelaria",
            "sku": "EST-COMP-01"
        },
        {
            "nome": "Mochila Escolar Resistente",
            "descricao": "Mochila com compartimento para notebook",
            "preco": 129.90,
            "estoque": 20,
            "categoria": "mochilas",
            "sku": "MOC-ESC-01"
        },
        {
            "nome": "Kit Canetas Coloridas",
            "descricao": "Conjunto com 12 canetas em cores diferentes",
            "preco": 22.90,
            "estoque": 45,
            "categoria": "papelaria",
            "sku": "CAN-COL-12"
        },
        {
            "nome": "Livro Matemática Fundamental",
            "descricao": "Livro didático para ensino fundamental",
            "preco": 89.90,
            "estoque": 25,
            "categoria": "livros",
            "sku": "LIV-MAT-01"
        },
        {
            "nome": "Uniforme Escolar - Camiseta",
            "descricao": "Camiseta em algodão com logo da escola",
            "preco": 45.00,
            "estoque": 100,
            "categoria": "uniforme",
            "sku": "UNI-CAM-01"
        },
        {
            "nome": "Agenda Escolar 2025",
            "descricao": "Agenda com calendário e planejador",
            "preco": 28.90,
            "estoque": 40,
            "categoria": "papelaria",
            "sku": "AGE-2025"
        },
        {
            "nome": "Kit Arte Escolar",
            "descricao": "Kit com lápis de cor, giz de cera e canetinhas",
            "preco": 48.90,
            "estoque": 35,
            "categoria": "papelaria",
            "sku": "ART-KIT-01"
        },
        {
            "nome": "Dicionário Português",
            "descricao": "Dicionário completo da língua portuguesa",
            "preco": 75.90,
            "estoque": 30,
            "categoria": "livros",
            "sku": "LIV-DIC-01"
        },
        {
            "nome": "Uniforme Escolar - Calça",
            "descricao": "Calça em tactel com logo da escola",
            "preco": 65.00,
            "estoque": 80,
            "categoria": "uniforme",
            "sku": "UNI-CAL-01"
        },
        {
            "nome": "Calculadora Científica",
            "descricao": "Calculadora com funções científicas",
            "preco": 45.90,
            "estoque": 25,
            "categoria": "papelaria",
            "sku": "CAL-CIE-01"
        },
        {
            "nome": "Atlas Geográfico",
            "descricao": "Atlas completo com mapas atualizados",
            "preco": 68.90,
            "estoque": 20,
            "categoria": "livros",
            "sku": "LIV-ATL-01"
        },
        {
            "nome": "Lancheira Térmica",
            "descricao": "Lancheira com isolamento térmico",
            "preco": 42.90,
            "estoque": 30,
            "categoria": "mochilas",
            "sku": "LAN-TER-01"
        },
        {
            "nome": "Kit Réguas Geométricas",
            "descricao": "Kit com régua, esquadro e transferidor",
            "preco": 15.90,
            "estoque": 60,
            "categoria": "papelaria",
            "sku": "REG-GEO-01"
        },
        {
            "nome": "Livro História do Brasil",
            "descricao": "Livro didático de história",
            "preco": 82.90,
            "estoque": 25,
            "categoria": "livros",
            "sku": "LIV-HIS-01"
        },
        {
            "nome": "Uniforme Escolar - Agasalho",
            "descricao": "Casaco de moletom com logo da escola",
            "preco": 89.90,
            "estoque": 50,
            "categoria": "uniforme",
            "sku": "UNI-AGA-01"
        },
        {
            "nome": "Pasta Organizadora A4",
            "descricao": "Pasta com divisórias e fechamento",
            "preco": 32.90,
            "estoque": 40,
            "categoria": "papelaria",
            "sku": "PAS-ORG-01"
        },
        {
            "nome": "Mochila com Rodinhas",
            "descricao": "Mochila escolar com rodinhas resistentes",
            "preco": 159.90,
            "estoque": 15,
            "categoria": "mochilas",
            "sku": "MOC-ROD-01"
        },
        {
            "nome": "Kit Cadernos 5 Matérias",
            "descricao": "Kit com 3 cadernos de 5 matérias",
            "preco": 59.90,
            "estoque": 30,
            "categoria": "papelaria",
            "sku": "CAD-KIT-01"
        },
        {
            "nome": "Livro Ciências Naturais",
            "descricao": "Livro didático de ciências",
            "preco": 79.90,
            "estoque": 25,
            "categoria": "livros",
            "sku": "LIV-CIE-01"
        }
    ]
    
    for produto in produtos:
        db_produto = Product(**produto)
        db.add(db_produto)
    
    db.commit()

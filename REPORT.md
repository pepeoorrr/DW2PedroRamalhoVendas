# Relatório Técnico

## Descrição do Projeto
Este sistema é uma aplicação web de vendas de produtos escolares, composta por um front-end em HTML, CSS e JavaScript, e um back-end em Python (FastAPI) com banco de dados SQLite via SQLAlchemy.

## Estrutura de Pastas
- frontend/
  - index.html
  - css/styles.css
  - js/main.js
- backend/
  - app/
    - main.py
    - database.py
    - seed.py
    - models/models.py
    - routes/routes.py
  - requirements.txt
- README.md
- REPORT.md

## Funcionalidades
- Catálogo de produtos com busca, ordenação e filtro por categoria
- Carrinho de compras com persistência no localStorage
- Formulário de cadastro/edição de produtos (admin)
- Confirmação de pedido com validação de estoque e cupom
- API RESTful com endpoints para CRUD de produtos e confirmação de pedido

## Tecnologias Utilizadas
- Front-end: HTML5, CSS3 (Flex/Grid), JavaScript (ES6+)
- Back-end: Python 3, FastAPI, SQLAlchemy, SQLite

## Regras de Negócio
- Não permite adicionar ao carrinho se estoque = 0
- Cupom “ALUNO10” dá 10% de desconto
- Ao confirmar pedido, estoque é atualizado e pedido registrado

## Acessibilidade
- Uso de aria-label, contraste mínimo, navegação por teclado

## Testes Manuais
- Testes realizados via Thunder Client/Insomnia (ver arquivo de testes)

## Observações
- O banco de dados é gerado automaticamente ao rodar o back-end
- O seed.py insere produtos de exemplo

---

*Autor: Pedro Ramalho*
*Data: Setembro/2025*

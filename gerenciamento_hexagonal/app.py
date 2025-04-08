from fastapi import FastAPI

from gerenciamento_hexagonal.entrypoint.routerGerenciamentoComentario import router as gerenciamento_comentario_router
from gerenciamento_hexagonal.entrypoint.routerGerenciamentoProposta import router as gerenciamento_proposta_router

app = FastAPI()

app.include_router(gerenciamento_proposta_router, prefix='/GerenciamentoProposta', tags=['Gerenciamento Proposta'])

app.include_router(gerenciamento_comentario_router, prefix='/GerenciamentoComentario', tags=['Gerenciamento Comentario'])


@app.get('/')
async def read_root():
    return {'message': 'Bem-vindo à API de Gerenciamento!'}

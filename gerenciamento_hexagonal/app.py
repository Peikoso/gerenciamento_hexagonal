from fastapi import FastAPI

from gerenciamento_hexagonal.entrypoint.routerRelatorio import router as relatorio_router
from gerenciamento_hexagonal.entrypoint.routerGerenciamentoComentario import router as gerenciamento_comentario_router
from gerenciamento_hexagonal.entrypoint.routerGerenciamentoMeta import router as gerenciamento_meta_router
from gerenciamento_hexagonal.entrypoint.routerGerenciamentoProposta import router as gerenciamento_proposta_router

app = FastAPI()

app.include_router(relatorio_router, prefix='/Relatorio', tags=['Relatorio'])

app.include_router(gerenciamento_proposta_router, prefix='/GerenciamentoProposta', tags=['Gerenciamento Proposta'])

app.include_router(gerenciamento_comentario_router, prefix='/GerenciamentoComentario', tags=['Gerenciamento Comentario'])

app.include_router(gerenciamento_meta_router, prefix='/GerenciamentoMeta', tags=['Gerenciamento Meta'])


@app.get('/')
async def read_root():
    return {'message': 'Bem-vindo à API de Gerenciamento!'}

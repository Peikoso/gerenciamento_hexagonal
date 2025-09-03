from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from gerenciamento_hexagonal.infrastructure.handler.fastapi.routes.arquivo import router as arquivo_router
from gerenciamento_hexagonal.infrastructure.handler.fastapi.routes.gerenciamento_caracterizacao import router as gerenciamento_caracterizacao_router
from gerenciamento_hexagonal.infrastructure.handler.fastapi.routes.gerenciamento_comentario import router as gerenciamento_comentario_router
from gerenciamento_hexagonal.infrastructure.handler.fastapi.routes.gerenciamento_contrapartida import router as gerenciamento_contrapartida_router
from gerenciamento_hexagonal.infrastructure.handler.fastapi.routes.gerenciamento_contrapartida_admin import router as gerenciamento_contrapartida_admin_router
from gerenciamento_hexagonal.infrastructure.handler.fastapi.routes.gerenciamento_meta import router as gerenciamento_meta_router
from gerenciamento_hexagonal.infrastructure.handler.fastapi.routes.gerenciamento_proposta import router as gerenciamento_proposta_router
from gerenciamento_hexagonal.infrastructure.handler.fastapi.routes.gerenciamento_qualitativo import router as gerenciamento_qualitativo_router
from gerenciamento_hexagonal.infrastructure.handler.fastapi.routes.gerenciamento_quantitativo import router as gerenciamento_quantitativo_router
from gerenciamento_hexagonal.infrastructure.handler.fastapi.routes.relatorio import router as relatorio_router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000', 'http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router(relatorio_router, prefix='/Relatorio', tags=['Relatorio'])
app.include_router(gerenciamento_proposta_router, prefix='/GerenciamentoProposta', tags=['Gerenciamento Proposta'])
app.include_router(gerenciamento_comentario_router, prefix='/GerenciamentoComentario', tags=['Gerenciamento Comentario'])
app.include_router(gerenciamento_meta_router, prefix='/GerenciamentoMeta', tags=['Gerenciamento Meta'])
app.include_router(gerenciamento_quantitativo_router, prefix='/GerenciamentoQuantitativo', tags=['Gerenciamento Quantitativo'])
app.include_router(gerenciamento_qualitativo_router, prefix='/GerenciamentoQualitativo', tags=['Gerenciamento Qualitativo'])
app.include_router(gerenciamento_caracterizacao_router, prefix='/GerenciamentoCaracterizacao', tags=['Gerenciamento Caracterizacao'])
app.include_router(gerenciamento_contrapartida_router, prefix='/GerenciamentoContrapartida', tags=['Gerenciamento Contrapartida'])
app.include_router(gerenciamento_contrapartida_admin_router, prefix='/GerenciamentoContrapartidaAdmin', tags=['Gerenciamento Contrapartida Admin'])
app.include_router(arquivo_router, prefix='/Arquivo', tags=['Arquivo'])


@app.get('/')
async def read_root():
    return {'message': 'Bem-vindo à API de Gerenciamento!'}

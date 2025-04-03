from entrypoint.router import router as gerenciamento_proposta_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(gerenciamento_proposta_router, prefix='/gerenciamento', tags=['Gerenciamento'])


@app.get('/')
async def read_root():
    return {'message': 'Bem-vindo à API de Gerenciamento Propostas!'}

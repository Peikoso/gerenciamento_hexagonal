from quart import Quart
from gerenciamento_hexagonal.infrastructure.handler.quart.routes.gerenciamento_proposta import proposta_bp

def create_app():
    app = Quart(__name__)
    app.register_blueprint(proposta_bp)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

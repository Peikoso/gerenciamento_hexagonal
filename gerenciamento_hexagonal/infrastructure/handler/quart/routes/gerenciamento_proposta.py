from quart import Blueprint, request, jsonify
from http import HTTPStatus
from pydantic import ValidationError

from gerenciamento_hexagonal.domain.exceptions.gerenciamentoExceptions import (
    DomainValidationError,
    NotFoundError,
    NotNullViolationError,
)
from gerenciamento_hexagonal.domain.models.gerenciamento_dto_response import (
    GerenciamentoComentarioDTO,
    GerenciamentoPropostaDTO,
)
from gerenciamento_hexagonal.infrastructure.handler.quart.container import get_service_gerenciamento_proposta

proposta_bp = Blueprint("GerenciamentoProposta", __name__, url_prefix="/GerenciamentoProposta/")


@proposta_bp.route("/", methods=["POST"])
async def create_gerenciamento_proposta():
    service = get_service_gerenciamento_proposta()
    try:
        data = await request.get_json()
        dto = GerenciamentoPropostaDTO(**data)
        result = await service.create_gerenciamento_proposta(dto)
        return jsonify(result.dict()), HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({"detail": e.errors()}), HTTPStatus.UNPROCESSABLE_ENTITY


@proposta_bp.route("/Comentario/<int:gerenciamento_proposta_id>", methods=["POST"])
async def create_gerenciamento_proposta_comentario(gerenciamento_proposta_id):
    service = get_service_gerenciamento_proposta()
    try:
        data = await request.get_json()
        dto = GerenciamentoComentarioDTO(**data)
        result = await service.create_gerenciamento_proposta_comentario(gerenciamento_proposta_id, dto)
        return jsonify(result.dict()), HTTPStatus.CREATED
    except NotFoundError as e:
        return jsonify({"detail": str(e)}), HTTPStatus.NOT_FOUND
    except DomainValidationError as e:
        return jsonify({"detail": str(e)}), HTTPStatus.UNPROCESSABLE_ENTITY


@proposta_bp.route("/", methods=["GET"])
async def get_gerenciamento_propostas():
    service = get_service_gerenciamento_proposta()
    result = await service.get_gerenciamento_proposta()
    return jsonify([p.dict() for p in result]), HTTPStatus.OK


@proposta_bp.route("/<int:gerenciamento_proposta_id>", methods=["GET"])
async def get_by_id_gerenciamento_proposta(gerenciamento_proposta_id):
    service = get_service_gerenciamento_proposta()
    try:
        result = await service.get_gerenciamento_proposta_by_id(gerenciamento_proposta_id)
        return jsonify(result.dict()), HTTPStatus.OK
    except NotFoundError as e:
        return jsonify({"detail": str(e)}), HTTPStatus.NOT_FOUND


@proposta_bp.route("/<int:gerenciamento_proposta_id>", methods=["PUT"])
async def update_gerenciamento_proposta(gerenciamento_proposta_id):
    service = get_service_gerenciamento_proposta()
    try:
        data = await request.get_json()
        dto = GerenciamentoPropostaDTO(**data)
        result = await service.update_gerenciamento_proposta(gerenciamento_proposta_id, dto)
        return jsonify(result.dict()), HTTPStatus.OK
    except NotFoundError as e:
        return jsonify({"detail": str(e)}), HTTPStatus.NOT_FOUND


@proposta_bp.route("/<int:gerenciamento_proposta_id>", methods=["DELETE"])
async def delete_gerenciamento_proposta(gerenciamento_proposta_id):
    service = get_service_gerenciamento_proposta()
    try:
        result = await service.delete_gerenciamento_proposta(gerenciamento_proposta_id)
        return jsonify({"success": True, "deleted": result}), HTTPStatus.OK
    except NotFoundError as e:
        return jsonify({"detail": str(e)}), HTTPStatus.NOT_FOUND
    except NotNullViolationError as e:
        return jsonify({"detail": str(e)}), HTTPStatus.CONFLICT

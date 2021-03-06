
import datetime

from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import  Resource
from flask_restful_swagger import swagger

from covidbed.serializer.orga import OrganizationSearchRequestSerializer, OrganizationSearchResponseSerializer

from covidbed.repository import orga as orga_repository
from covidbed.validator import orga as orga_validator

from sqlalchemy.orm.exc import NoResultFound

class OrganizationSearchAPI(Resource):
    method_decorators = [jwt_required]

    @swagger.operation(
        notes='Organizations',
        responseClass=OrganizationSearchResponseSerializer.__name__,
        nickname='organizations search',
        parameters=[
            {
                "name": "body",
                "description": "organisations which might provide resources. It could be a company or a finess instutition.",
                "required": True,
                "allowMultiple": False,
                "dataType": OrganizationSearchRequestSerializer.__name__,
                "paramType": "body",
            }
        ]
    )

    def get(self):
        params = request.json
        print(params)
        validator = orga_validator.OrganizationSearchRequest()
        errors = validator.validate(params, many=False)
        if errors:
            return {"errors": [{"code": f"BAD_PARAM_{k.upper()}", "message": "\n".join(v)} for k, v in
                               errors.items()]}, 400
        params = validator.load(params)
        errors = []
        
        # First we evaluate if the organization already exists
        orga = None
        get_func_dict = {
            "id": orga_repository.get_organization_by_id,
            "siret": orga_repository.get_organization_by_siret,
            "finess_et": orga_repository.get_organization_by_finess_et,
            "finess_ej": orga_repository.get_organization_by_finess_ej
        }
        result = {field: get_func_dict[field](param) for field, param in params.items()}
        if len(set(result.values())) != 1:
            errors.append({
                "code": f"MISMATCHING_RETRIEVAL",
                "message": "finess_et and finess_ej don't correspond to the same entity"
            })
            return {"errors": errors}, 400

        key, orga = next(iter(result.items()))
        
        if orga is None:
            errors.append({
                "code": f"NOT_FOUND",
                "message": "The entity you are looking for doesn't exist yet"
            })
            return {"errors": errors}, 400

        return {"organization": orga.json, "retrived_key": key}, 200

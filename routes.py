from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Route, Building
from app.auth.jwt import jwt_required

routes_bp = Blueprint("routes", __name__)

@routes_bp.route("/", methods=["GET"])
def get_routes():
    routes = Route.query.all()

    return jsonify([
        {
            "id": r.id,
            "origin_building_id": r.origin_building_id,
            "destination_building_id": r.destination_building_id
        } for r in routes
    ])

@routes_bp.route("/<int:route_id>", methods=["GET"])
def get_route(route_id):
    route = Route.query.get(route_id)

    if not route:
        return jsonify({"error": "Route not found"}), 404

    return jsonify({
        "id": route.id,
        "origin_building_id": route.origin_building_id,
        "destination_building_id": route.destination_building_id
    })

@routes_bp.route("/", methods=["POST"])
@jwt_required
def create_route():
    data = request.get_json()

    origin = data.get("origin_building_id")
    destination = data.get("destination_building_id")

    if not origin or not destination:
        return jsonify({"error": "Missing building IDs"}), 400

    if origin == destination:
        return jsonify({"error": "Origin and destination cannot be the same"}), 400

    if not Building.query.get(origin) or not Building.query.get(destination):
        return jsonify({"error": "Invalid building ID"}), 400

    route = Route(
        origin_building_id=origin,
        destination_building_id=destination
    )

    db.session.add(route)
    db.session.commit()

    return jsonify({"message": "Route created", "id": route.id}), 201

@routes_bp.route("/<int:route_id>", methods=["PUT"])
@jwt_required
def update_route(route_id):
    route = Route.query.get(route_id)

    if not route:
        return jsonify({"error": "Route not found"}), 404

    data = request.get_json()

    origin = data.get("origin_building_id")
    destination = data.get("destination_building_id")

    if origin:
        if not Building.query.get(origin):
            return jsonify({"error": "Invalid origin building"}), 400
        route.origin_building_id = origin

    if destination:
        if not Building.query.get(destination):
            return jsonify({"error": "Invalid destination building"}), 400
        route.destination_building_id = destination

    if route.origin_building_id == route.destination_building_id:
        return jsonify({"error": "Origin and destination cannot match"}), 400

    db.session.commit()
    return jsonify({"message": "Route updated"})

@routes_bp.route("/<int:route_id>", methods=["DELETE"])
@jwt_required
def delete_route(route_id):
    route = Route.query.get(route_id)

    if not route:
        return jsonify({"error": "Route not found"}), 404

    db.session.delete(route)
    db.session.commit()

    return jsonify({"message": "Route deleted"})

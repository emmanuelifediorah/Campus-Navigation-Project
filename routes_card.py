from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Route, RouteCard
from app.auth.jwt import jwt_required

route_cards_bp = Blueprint("route_cards", __name__)

@route_cards_bp.route("/<int:route_id>/cards", methods=["GET"])
def get_route_cards(route_id):
    route = Route.query.get(route_id)

    if not route:
        return jsonify({"error": "Route not found"}), 404

    cards = RouteCard.query.filter_by(
        route_id=route_id
    ).order_by(RouteCard.step_number).all()

    return jsonify([
        {
            "id": c.id,
            "step_number": c.step_number,
            "instruction": c.instruction,
            "image_url": c.image_url
        } for c in cards
    ])

@route_cards_bp.route("/<int:route_id>/cards", methods=["POST"])
@jwt_required
def create_route_card(route_id):
    route = Route.query.get(route_id)

    if not route:
        return jsonify({"error": "Route not found"}), 404

    data = request.get_json()

    step = data.get("step_number")
    instruction = data.get("instruction")
    image_url = data.get("image_url")

    if not step or not instruction:
        return jsonify({"error": "Missing required fields"}), 400

    existing = RouteCard.query.filter_by(
        route_id=route_id,
        step_number=step
    ).first()

    if existing:
        return jsonify({"error": "Step number already exists for this route"}), 400

    card = RouteCard(
        route_id=route_id,
        step_number=step,
        instruction=instruction,
        image_url=image_url
    )

    db.session.add(card)
    db.session.commit()

    return jsonify({"message": "Route card created", "id": card.id}), 201

@route_cards_bp.route("/<int:route_id>/navigation", methods=["GET"])
def get_route_navigation(route_id):
    route = Route.query.get(route_id)
    if not route:
        return jsonify({"error": "Route not found"}), 404
    
    cards = RouteCard.query.filter_by(route_id=route_id).order_by(RouteCard.step_number).all()
    
    return jsonify({
        "route": {
            "id": route.id,
            "origin_building_id": route.origin_building_id,
            "destination_building_id": route.destination_building_id
        },
        "cards": [{
            "id": c.id,
            "step_number": c.step_number,
            "instruction": c.instruction,
            "image_url": c.image_url
        } for c in cards]
    })
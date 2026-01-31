from flask import Flask
from app.routes.routes import routes_bp
from app.routes.route_cards import route_cards_bp

def register_routes(app):
    app.register_blueprint(routes_bp, url_prefix="/api/routes")
    app.register_blueprint(route_cards_bp, url_prefix="/api/routes")
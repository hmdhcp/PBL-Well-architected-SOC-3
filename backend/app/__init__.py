from flask import Flask
from flask_smorest import Api, Blueprint as SmorestBlueprint
from flask_cors import CORS
from app.extensions import db, migrate, jwt, limiter

health_bp = SmorestBlueprint("health", __name__, url_prefix="/api/v1", description="Cek status server")


@health_bp.route("/health")
def health():
    """Cek apakah API berjalan"""
    return {"status": "ok"}


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    #tambahan configurasi untuk Swagger
    app.config['API_TITLE'] = 'E-Commerce PBL API'
    app.config['API_VERSION'] = 'v1'
    app.config['OPENAPI_VERSION'] = '3.0.2'
    app.config['OPENAPI_URL_PREFIX'] = '/'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/apidocs'
    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/'

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)
    

    api = Api(app)
    api.register_blueprint(health_bp)

    from routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app
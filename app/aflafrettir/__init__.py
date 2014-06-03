from flask import Blueprint

aflafrettir = Blueprint('aflafrettir', __name__)

from .import routes

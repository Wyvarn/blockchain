from flask import Blueprint

block = Blueprint(name="block", import_name=__name__, url_prefix="/block", static_folder="static",
                  template_folder="templates"
                  )

from . import views

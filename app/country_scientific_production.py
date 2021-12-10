import base64
from io import BytesIO

from flask import render_template

from app import app
from techminer.world_map import world_map


@app.route("/country_scientific_production")
def country_scientific_production():

    return render_template(
        "country_scientific_production.html", title="Country", user=user
    )

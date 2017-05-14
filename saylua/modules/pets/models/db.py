from saylua import db
from ..soul_names import soul_name
import os
from saylua.utils import get_static_version_id
from flask import url_for


# Pets are divided into species and species are divided into variations
class Species(db.Model):

    __tablename__ = "species"

    name = db.Column(db.String(80), primary_key=True)
    description = db.Column(db.Text)


class SpeciesCoat(db.Model):

    __tablename__ = "species_coats"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    species_name = db.Column(db.String(80), db.ForeignKey("species.name"))
    species = db.relationship("Species")
    description = db.Column(db.Text)


class Pet(db.Model):

    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True)
    soul_name = db.Column(db.String(80), unique=True)

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    owner = db.relationship("User", foreign_keys=[owner_id], back_populates="pets")
    # Only set if the pet is a variation
    coat_id = db.Column(db.Integer, db.ForeignKey("species_coats.id"))
    coat = db.relationship("SpeciesCoat")
    species_name = db.Column(db.String(80), db.ForeignKey("species.name"))
    species = db.relationship("Species")

    # Which way is the pet's image facing
    facing_right = db.Column(db.Boolean, default=True)

    # Personal profile information for the pet
    name = db.Column(db.String(80))
    description = db.Column(db.Text)
    date_bonded = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    # If either of these is set to a number other than 0, the pet is for sale
    ss_price = db.Column(db.Integer, default=0)
    cc_price = db.Column(db.Integer, default=0)

    def image(this):
        subpath = ("img" + os.sep + "pets" + os.sep + this.species_name + os.sep + this.coat.name +
            ".png")
        return url_for("static", filename=subpath) + "?v=" + str(get_static_version_id())

    # Generate a new unique soul name
    @classmethod
    def new_soul_name(cls):
        min_length = 5
        new_name = soul_name(min_length)
        found = db.session.query(cls).filter(cls.soul_name == new_name).one_or_none()
        while found:
            min_length += 1
            new_name = soul_name(min_length)
            found = db.session.query(cls).filter(cls.soul_name == new_name).one_or_none()
        return new_name

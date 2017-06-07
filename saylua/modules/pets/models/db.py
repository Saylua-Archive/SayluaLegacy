from saylua import app, db
from ..soul_names import soul_name
import os
from saylua.utils import get_static_version_id, is_devserver
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
    name = db.Column(db.String(80), default="")
    description = db.Column(db.Text, default="")
    pronouns = db.Column(db.String(80), default="They/them")
    date_bonded = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    # If either of these is set to a number other than 0, the pet is for sale
    ss_price = db.Column(db.Integer, default=0)
    cc_price = db.Column(db.Integer, default=0)

    def image(self):
        if is_devserver():
            subpath = ("img" + os.sep + "pets" + os.sep + self.species_name + os.sep + self.coat.name +
            ".png")
            image_path = (os.path.join( # The joys of going up five levels
                os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(
                            os.path.dirname(__file__)))), "static", subpath))
            if os.path.isfile(image_path):
                return url_for("static", filename=subpath) + "?v=" + str(get_static_version_id())
        return (app.config['IMAGE_BUCKET_ROOT'] + "/pets/" + self.species_name + "/" +
            self.coat.name + ".png?v=" + str(get_static_version_id()))

    def url(self):
        return '/pet/' + self.soul_name

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

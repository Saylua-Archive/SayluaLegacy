from saylua import db


# Pets are divided into species and species are divided into variations
class Species(db.Model):

    __tablename__ = "species"

    name = db.Column(db.String(80), primary_key=True)
    description = db.Column(db.Text)


class SpeciesCoat(db.Model):

    __tablename__ = "species_coats"

    id = db.Column(db.Integer, primary_key=True)
    species_name = db.Column(db.String(80), db.ForeignKey("species.name"))
    name = db.Column(db.Text)
    description = db.Column(db.Text)


class Pet(db.Model):

    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True)
    soulname = db.Column(db.String(80), unique=True)

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Only set if the pet is a variation
    coat_id = db.Column(db.Integer, db.ForeignKey("species_coats.id"))
    coat = db.relationship("SpeciesCoat")
    species_name = db.Column(db.String(80), db.ForeignKey("species.name"))
    species = db.relationship("Species")

    # Personal profile information for the pet
    name = db.Column(db.String(80))
    description = db.Column(db.Text)

    # If either of these is set to a number other than 0, the pet is for sale
    ss_price = db.Column(db.Integer, default=0)
    cc_price = db.Column(db.Integer, default=0)

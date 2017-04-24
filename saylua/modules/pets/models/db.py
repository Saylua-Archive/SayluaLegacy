from saylua import db


# This is to store alternate linart versions of the same pets
class SpeciesVersion(db.Model):

    __tablename__ = "species_versions"

    id = db.Column(db.Integer, primary_key=True)
    species_name = db.Column(db.String, db.ForeignKey("species.name"))
    name = db.Column(db.String(80), unique=True)
    base_image = db.Column(db.String(200))
    base_psd = db.Column(db.String(200))
    default_image = db.Column(db.String(200))
    species = db.relationship("Species", back_populates="species_versions")


# Pets are divided into species and species are divided into variations
class Species(db.Model):

    __tablename__ = "species"

    name = db.Column(db.String, primary_key=True)
    description = db.Column(db.Text)
    versions = db.relationship("SpeciesVersion", back_populates="species")


class SpeciesVariation(db.Model):

    __tablename__ = "species_variations"

    id = db.Column(db.Integer, primary_key=True)
    species_name = db.Column(db.String, db.ForeignKey("species.name"))
    name = db.Column(db.Text)
    description = db.Column(db.Text)


class Pet(db.Model):

    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True)
    soulname = db.Column(db.String(80), unique=True)

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Only set if the pet is a variation
    variation_key = db.Column(db.Integer, db.ForeignKey("users.id"))
    species_name = db.Column(db.String(80), unique=True) # Note the denormalization

    # Personal profile information for the pet
    name = db.Column(db.String(80))
    css = db.Column(db.Text)
    description = db.Column(db.Text)

    # If either of these is set to a number other than 0, the pet is for sale
    ss_price = db.Column(db.Integer, default=0)
    cc_price = db.Column(db.Integer, default=0)

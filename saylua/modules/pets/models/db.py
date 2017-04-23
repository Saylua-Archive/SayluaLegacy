from saylua import db


# This is to store alternate linart versions of the same pets
class SpeciesVersion(db.Model):

    __tablename__ = "species_version"

    name = ndb.StringProperty()
    base_image = ndb.StringProperty()
    base_psd = ndb.StringProperty()
    default_image = ndb.StringProperty()


# Pets are divided into species and species are divided into variations
class Species(db.Model):

    __tablename__ = "species"

    name = db.Column(db.String, primary_key=True)
    versions = ndb.StructuredProperty(SpeciesVersion)
    description = db.Column(db.Text)


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

from google.appengine.ext import ndb

# This is to store alternate linart versions of the same pets
class SpeciesVersion(ndb.Model):
    name = ndb.StringProperty()
    base_image = ndb.StringProperty()
    base_psd = ndb.StringProperty()
    default_image = ndb.StringProperty()

# Pets are divided into species and species are divided into variations
class Species(ndb.Model):
    name = ndb.StringProperty()
    versions = ndb.StructuredProperty(SpeciesVersion)
    description = ndb.TextProperty()

class SpeciesVariation(ndb.Model):
    species_id = ndb.StringProperty()
    name = ndb.StringProperty()
    description = ndb.TextProperty()

class Pet(ndb.Model):
    pet_id = ndb.StringProperty()
    owner_id = ndb.IntegerProperty()
    variation_key = ndb.KeyProperty() # Only set if the pet is a variation
    species_name = ndb.StringProperty() # Note the denormalization

    # Personal profile information for the pet
    name = ndb.StringProperty()
    css = ndb.TextProperty(indexed=False)
    description = ndb.TextProperty(indexed=False)

    # If either of these is set to a number other than 0, the pet is for sale
    ss_price = ndb.IntegerProperty(default=0)
    cc_price = ndb.IntegerProperty(default=0)

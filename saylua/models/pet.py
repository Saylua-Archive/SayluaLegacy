from google.appengine.ext import ndb

# This is to store alternate linart versions of the same pets
class SpeciesVersion(ndb.Model):
    name = ndb.StringProperty()
    base_image = ndb.StringProperty()
    base_psd = ndb.StringProperty()
    default_image = ndb.StringProperty()

# Pets are divided into species and species are divided into variations
class Species(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    versions = ndb.StructuredProperty(SpeciesVersion, repeated=True)
    description = ndb.StringProperty()

class SpeciesVariation(ndb.Model):
    species_key = ndb.KeyProperty(indexed=True)
    name = ndb.StringProperty(indexed=True)
    description = ndb.StringProperty()

class Pet(ndb.Model):
    user_key = ndb.KeyProperty(indexed=True)
    variation_key = ndb.KeyProperty(indexed=True) # Only set if the pet is a variation
    species_name = ndb.StringProperty(indexed=True) # Note the denormalization

    # Personal profile information for the pet
    name = ndb.StringProperty()
    css = ndb.StringProperty()
    description = ndb.StringProperty()

    # If either of these is set to a number other than 0, the pet is for sale
    ss_price = ndb.IntegerProperty(default=0, indexed=True)
    cc_price = ndb.IntegerProperty(default=0, indexed=True)

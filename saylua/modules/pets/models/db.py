from saylua import app, db
from ..soul_names import soul_name

from saylua.modules.items.models.db import Item

from saylua.utils import get_static_version_id, is_devserver, go_up_path, canonize

from sqlalchemy.ext.hybrid import hybrid_property

from flask import url_for
import os


# Pets are divided into species and species are divided into variations.
class Species(db.Model):

    __tablename__ = "species"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), unique=True)
    canon_name = db.Column(db.String(80), unique=True)

    description = db.Column(db.Text)

    date_discovered = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, *args, **kwargs):
        super(Species, self).__init__(*args, **kwargs)
        if not self.canon_name:
            self.canon_name = canonize(self.name)

    @property
    def default_coat(self):
        coat = db.session.query(SpeciesCoat).filter(SpeciesCoat.coat_canon_name == 'common',
            SpeciesCoat.species_id == self.id).one_or_none()
        if not coat:
            coat = db.session.query(SpeciesCoat).filter(
                SpeciesCoat.species_id == self.id).limit(1).one_or_none()
        return coat

    def url(self):
        return '/species/' + self.canon_name + '/'

    def image_url(self):
        return self.default_coat.image_url()

    @classmethod
    def by_canon_name(cls, name):
        return db.session.query(cls).filter(cls.canon_name == name.lower()).one_or_none()


class SpeciesCoat(db.Model):

    __tablename__ = "species_coats"

    id = db.Column(db.Integer, primary_key=True)
    canon_name = db.Column(db.String(256), unique=True)

    coat_name = db.Column(db.String(80))
    coat_canon_name = db.Column(db.String(80))

    species_id = db.Column(db.Integer, db.ForeignKey("species.id"))
    species = db.relationship("Species")
    description = db.Column(db.Text)

    date_discovered = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, *args, **kwargs):
        super(SpeciesCoat, self).__init__(*args, **kwargs)
        if not self.canon_name:
            self.canon_name = self.species.canon_name + '_' + canonize(self.coat_name)

        if not self.coat_canon_name:
            self.coat_canon_name = canonize(self.coat_name)

    @property
    def name(self):
        return self.coat_name + ' ' + self.species.name

    def url(self):
        return '/coat/' + self.coat_canon_name + '/' + self.species.canon_name + '/'

    def image_url(self):
        if is_devserver():
            subpath = ("img" + os.sep + "pets" + os.sep + self.species.canon_name + os.sep + self.coat_name +
            ".png")
            image_path = (os.path.join(go_up_path(4, (__file__)), "static", subpath))
            if os.path.isfile(image_path):
                return url_for("static", filename=subpath) + "?v=" + str(get_static_version_id())
        return (app.config['IMAGE_BUCKET_ROOT'] + "/pets/" + self.species.canon_name + "/" +
            self.coat_name + ".png?v=" + str(get_static_version_id()))

    @classmethod
    def by_canon_name(cls, name):
        return db.session.query(cls).filter(cls.canon_name == name.lower()).one_or_none()


class Pet(db.Model):

    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True)
    soul_name = db.Column(db.String(80), unique=True)

    guardian_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    guardian = db.relationship("User", foreign_keys=[guardian_id], back_populates="pets")

    favorites = db.relationship("Item", secondary="pet_favorites")

    # Only set if the pet is a variation
    coat_id = db.Column(db.Integer, db.ForeignKey("species_coats.id"))
    coat = db.relationship("SpeciesCoat")

    # The pet's current mini.
    mini_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    mini = db.relationship("Item", foreign_keys=[mini_id])

    # Which way is the pet's image facing
    facing_right = db.Column(db.Boolean, default=True)

    # Personal profile information for the pet
    name = db.Column(db.String(80), default="")
    description = db.Column(db.Text, default="")
    pronouns = db.Column(db.String(80), default="They/them")
    date_created = db.Column(db.DateTime, server_default=db.func.now())

    # If either of these is set to a number other than 0, the pet is for sale
    ss_price = db.Column(db.Integer, default=0)
    cc_price = db.Column(db.Integer, default=0)

    def __init__(self, *args, **kwargs):
        super(Pet, self).__init__(*args, **kwargs)

        # Populate pet favorites.
        if not self.favorites:
            self.favorites = db.session.query(Item).order_by(db.func.rand()).limit(4).all()

        if not self.soul_name:
            self.soul_name = Pet.new_soul_name()

        if not self.name:
            self.name = self.soul_name.capitalize()

    @hybrid_property
    def bonding_day(self):
        if not self.friendship:
            return None
        return self.friendship.bonding_day

    @bonding_day.setter
    def set_bonding_day(self, date):
        if not self.friendship:
            return None
        self.friendship.bonding_day = date
        return self.friendship

    @property
    def friendship(self):
        return db.session.query(PetFriendship).get((self.id, self.guardian_id))

    @property
    def mini_friendship(self):
        return db.session.query(MiniFriendship).get((self.id, self.mini_id))

    @property
    def species(self):
        return self.coat.species

    def image_url(self):
        return self.coat.image_url()

    def url(self):
        return '/pet/' + self.soul_name + '/'

    def to_dict(self):
        data = {
            'name': self.name,
            'id': self.id,
            'image_url': self.image_url(),
            'url': self.url(),
        }
        return data

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


class PetFriendship(db.Model):
    """
    A table that stores metadata on the relationship between users and their
    pets. Note that even if a pet is transferred, it maintains "memory" of
    their old user.
    """
    __tablename__ = "pet_friendships"

    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), primary_key=True)
    guardian_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)

    pet = db.relationship("Pet")
    guardian = db.relationship("User")

    bonding_day = db.Column(db.DateTime, server_default=db.func.now())
    happiness = db.Column(db.Integer, default=0)


class MiniFriendship(db.Model):
    """
    A relationship between a pet and their mini. Note that although a pet can
    only have one mini equipped at a time, it keeps a memory of its past minis.
    """
    __tablename__ = "mini_friendships"

    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), primary_key=True)
    mini_id = db.Column(db.Integer, db.ForeignKey("items.id"), primary_key=True)

    pet = db.relationship("Pet")
    mini = db.relationship("Item")

    nickname = db.Column(db.String(80))
    description = db.Column(db.String(512))

    @property
    def name(self):
        if self.nickname:
            return self.nickname
        return self.mini.name


class PetFavorite(db.Model):
    __tablename__ = "pet_favorites"

    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), primary_key=True)

    pet = db.relationship("Pet")
    item = db.relationship("Item")

    discovered = db.Column(db.Boolean, default=False)

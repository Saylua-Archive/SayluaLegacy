from saylua import db
from collections import OrderedDict

# Fool! Avert your gaze! If you should meet them eye to eye... you will be lost forever!
# Abandon hope all ye' who enter here
#
# (These relationships are necessary for Many to Many relationships to function properly)

r_entity_to_wrapper = db.Table('r_entity_to_wrapper',
    db.Column('wrapper_id', db.Integer, db.ForeignKey('dungeon_script_wrappers.id')),
    db.Column('entity_id', db.Integer, db.ForeignKey('dungeon_entities.id'))
)

r_entity_to_trait = db.Table('r_entity_to_trait',
    db.Column('trait_id', db.Integer, db.ForeignKey('dungeon_traits.id')),
    db.Column('entity_id', db.Integer, db.ForeignKey('dungeon_entities.id'))
)

r_tile_to_wrapper = db.Table('r_tile_to_wrapper',
    db.Column('wrapper_id', db.Integer, db.ForeignKey('dungeon_script_wrappers.id')),
    db.Column('tile_id', db.Integer, db.ForeignKey('dungeon_tiles.id'))
)

r_tile_to_trait = db.Table('r_tile_to_trait',
    db.Column('trait_id', db.Integer, db.ForeignKey('dungeon_traits.id')),
    db.Column('tile_id', db.Integer, db.ForeignKey('dungeon_tiles.id'))
)

r_wrapper_to_script = db.Table('r_wrapper_to_script',
    db.Column('script_id', db.Integer, db.ForeignKey('dungeon_scripts.id')),
    db.Column('wrapper_id', db.Integer, db.ForeignKey('dungeon_script_wrappers.id'))
)

r_trait_to_wrapper = db.Table('r_trait_to_wrapper',
    db.Column('wrapper_id', db.Integer, db.ForeignKey('dungeon_script_wrappers.id')),
    db.Column('trait_id', db.Integer, db.ForeignKey('dungeon_traits.id'))
)



class SerializerBase:
    """Provide JSON (dict) serialization to our Tile and Entity objects for ease of use.
    """

    def to_dict(self):
        # Define base dict, set defaults
        base_dict = OrderedDict()

        # Fill in base data
        base_dict['id'] = self.name
        base_dict['name'] = self.display_name
        base_dict['description'] = self.description
        base_dict['type'] = self.type
        base_dict['events'] = {}
        base_dict['meta'] = self.meta if self.meta else {}
        base_dict['traits'] = []

        # Normalize event items into dict values
        for event in self.events:
            # TODO: In the future, check if the is_devserver() flag is set
            # and serve a minified version instead.
            name = event.event_name
            content = event.event_script[0].content

            base_dict['events'][name] = content

        # Inherit events / dict items from traits
        for trait in self.traits:
            base_dict.traits.append(trait.display_name)

            # Trait events override local event values.
            for event in trait.events:
                name = event.event_name
                content = event.event_script[0].content

                base_dict['events'][name] = content

            # Merge our two meta dictionaries.
            # Unlike events, local dict values override trait dict values.
            if trait.meta:
                # The use of 'list' here is redundant unless you are using Python 3.
                # Future proofing is important, kids.
                base_dict['meta'] = dict(
                    list(base_dict['meta'].items()) +
                    list(trait.meta.items())
                )

        return base_dict


class DungeonScript(db.Model):
    """Basic blob container for Dungeons JS scripting.
    """

    __tablename__ = 'dungeon_scripts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    content = db.Column(db.Text())
    # content_minified = db.Column(db.Text())


class DungeonScriptWrapper(db.Model):
    """This allows multiple actors to refer to the same script
    when doing a JOIN, preserving the event type that the script is bound to.
    """
    __tablename__ = 'dungeon_script_wrappers'

    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(128), unique=True)

    event_script = db.relationship(
        DungeonScript,
        secondary=r_wrapper_to_script,
        backref='wrappers',
        lazy='joined',
        innerjoin=True
    )


class DungeonTrait(db.Model):
    """Extends actor functionality, allowing Entities & Tiles
    to share pools of events / metadata.
    """

    __tablename__ = 'dungeon_traits'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    display_name = db.Column(db.String(128))
    description = db.Column(db.Text())
    events = db.relationship(
        DungeonScriptWrapper,
        secondary=r_trait_to_wrapper,
        backref='traits',
        lazy='joined'
    )

    meta = db.Column(db.JSON())


class DungeonEntity(db.Model, SerializerBase):
    """Entity schema. Used for anything that
    is not a tile that would rest on a tile.
    """

    __tablename__ = 'dungeon_entities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    display_name = db.Column(db.String(128))
    description = db.Column(db.Text())
    type = db.Column(db.String(128))

    events = db.relationship(
        DungeonScriptWrapper,
        secondary=r_entity_to_wrapper,
        backref='entities',
        lazy='joined'
    )

    traits = db.relationship(
        DungeonTrait,
        secondary=r_entity_to_trait,
        backref='entities',
        lazy='joined'
    )

    meta = db.Column(db.JSON())


class DungeonTile(db.Model, SerializerBase):
    """If it looks like a tile, and it quacks like a tile...
    """

    __tablename__ = 'dungeon_tiles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    display_name = db.Column(db.String(128))
    description = db.Column(db.Text())
    type = db.Column(db.String(128))

    events = db.relationship(
        DungeonScriptWrapper,
        secondary=r_tile_to_wrapper,
        backref='tiles',
        lazy='joined'
    )

    traits = db.relationship(
        DungeonTrait,
        secondary=r_tile_to_trait,
        backref='tiles',
        lazy='joined'
    )

    meta = db.Column(db.JSON())

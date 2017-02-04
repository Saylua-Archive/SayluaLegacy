from saylua import db

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
    def to_json(self):
        pass


class DungeonScript(db.Model):
    __tablename__ = 'dungeon_scripts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    content = db.Column(db.Text())
    # content_minified = db.Column(db.Text())


class DungeonScriptWrapper(db.Model):
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

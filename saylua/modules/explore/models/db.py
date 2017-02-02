from saylua import db

class DungeonScript(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    content = db.Column(db.Text())
    # content_minified = db.Column(db.Text())

    wrapper = db.Column(db.Integer, db.ForeignKey('dungeon_script_wrapper.id'))


class DungeonScriptWrapper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(128), unique=True)

    event_script = db.relationship(
        'DungeonScript',
        backref='dungeon_script_wrapper',
        lazy='joined',
        innerjoin=True
    )

    entities = db.relationship('DungeonEntity', back_populates='events', lazy=True)
    traits = db.relationship('DungeonTrait', back_populates='events', lazy=True)
    tiles = db.relationship('DungeonTile', back_populates='events', lazy=True)


class DungeonTrait(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.Text())
    events = db.relationship(
        'DungeonScriptWrapper',
        back_populates='traits',
        lazy='joined',
        innerjoin=True
    )

    meta = db.Column(db.JSON())
    entity_id = db.Column(db.Integer, db.ForeignKey('dungeon_entity.id'))
    tile_id = db.Column(db.Integer, db.ForeignKey('dungeon_tile.id'))


class DungeonEntity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.Text())
    type = db.Column(db.String(128))

    events = db.relationship(
        'DungeonScriptWrapper',
        back_populates='entities',
        lazy='joined',
        innerjoin=True
    )

    traits = db.relationship(
        'DungeonTrait',
        backref='dungeon_entity',
        lazy='joined',
        innerjoin=True
    )

    meta = db.Column(db.JSON())


class DungeonTile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.Text())
    type = db.Column(db.String(128))

    events = db.relationship(
        'DungeonScriptWrapper',
        back_populates='tiles',
        lazy='joined',
        innerjoin=True
    )

    traits = db.relationship(
        'DungeonTrait',
        backref='dungeon_tile',
        lazy='joined',
        innerjoin=True
    )

    meta = db.Column(db.JSON())

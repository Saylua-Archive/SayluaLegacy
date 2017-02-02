from saylua import db

class DungeonScript(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    content = db.Column(db.Text())
    # minified_content = db.Column(db.Text())

    entities = db.relationship('DungeonEntity', back_populates='events', lazy=True)
    traits = db.relationship('DungeonTrait', back_populates='events', lazy=True)


class DungeonEntity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.Text())
    type = db.Column(db.String(128))

    events = db.relationship(
        'DungeonScript',
        back_populates='entities',
        lazy='joined',
        innerjoin=True
    )

    traits = db.relationship(
        'DungeonScript',
        backref='dungeon_entity',
        lazy='joined',
        innerjoin=True
    )

    meta = db.Column(db.JSON())


class DungeonTrait(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.Text())
    events = db.relationship(
        'DungeonScript',
        back_populates='traits',
        lazy='joined',
        innerjoin=True
    )

    meta = db.Column(db.JSON())
    entity_id = db.Column(db.Integer, db.ForeignKey('dungeon_entity.id'))

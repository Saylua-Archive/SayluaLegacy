from saylua import db

class DungeonScript(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    content = db.Column(db.Text())
    # minified_content = db.Column(db.Text())
    owner_id = db.Column(db.Integer, db.ForeignKey('Owner.id'))

class DungeonEntity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.Text())
    type = db.Column(db.String(128))

    events = db.relationship(
        'DungeonScript',
        backref='Owner',
        lazy='joined',
        innerjoin=True
    )

    meta = db.Column(db.JSON())

#class DungeonTrait(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String(128))
#    description = db.Column(db.Text())
#    events = db.relationship(
#        'DungeonScript',
#        backref='Owner',
#        lazy='joined',
#        innerjoin=True
#    )
#
#    meta = db.Column(db.JSON())
#    entity_id = db.Column(db.Integer, db.ForeignKey('DungeonEntity.id'))

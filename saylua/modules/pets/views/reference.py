from flask import render_template, abort

from saylua import db
from saylua.modules.pets.models.db import Species, SpeciesCoat


def species_guide():
    species_list = db.session.query(Species).all()
    return render_template('reference/species_guide.html', species_list=species_list)


def species_view(canon_name):
    species = Species.by_canon_name(canon_name)
    coats = db.session.query(SpeciesCoat).filter(
        SpeciesCoat.species_name == species.name).order_by(
        SpeciesCoat.date_discovered.desc()).limit(10)
    return render_template('reference/species_view.html', species=species, coats=coats)


def coat_guide():
    coats = db.session.query(SpeciesCoat).all()
    return render_template('reference/coat_guide.html', coats=coats)


def coat_view_all(coat_canon_name):
    coats = db.session.query(SpeciesCoat).filter(
        SpeciesCoat.coat_canon_name == coat_canon_name).order_by(
        SpeciesCoat.date_discovered.desc()).limit(10)

    if coats.count() < 1:
        abort(404)

    coat_name = coats[0].coat_name

    return render_template('reference/coat_view_all.html', coats=coats,
        coat_name=coat_name)


def coat_view(coat_canon_name, species_canon_name):
    coat = db.session.query(SpeciesCoat).join(SpeciesCoat.species).filter(
        SpeciesCoat.coat_canon_name == coat_canon_name,
        Species.canon_name == species_canon_name).first()
    if not coat:
        abort(404)
    return render_template('reference/coat_view.html', coat=coat)

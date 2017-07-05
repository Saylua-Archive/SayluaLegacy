from saylua.routing import url
from . import views

urlpatterns = [
    # Pet profiles and actions.
    url('/pet/<name>/', view_func=views.general.pet_profile, name="profile", methods=['GET', 'POST']),
    url('/edit_pet/<name>/', view_func=views.general.edit_pet, name="edit_pet", methods=['GET', 'POST']),
    url('/accompany/<soul_name>/', view_func=views.general.pet_accompany, name="accompany", methods=['POST']),
    url('/abandon/', view_func=views.general.pet_abandon, name="abandon", methods=['POST']),

    url('/reserve/', view_func=views.reserve.pet_reserve, name="reserve", methods=['GET']),
    url('/reserve/', view_func=views.reserve.pet_reserve_post, name="reserve_post", methods=['POST']),

    url('/species/', view_func=views.reference.species_guide, name="species_guide"),
    url('/species/<canon_name>/', view_func=views.reference.species_view, name="species_view"),

    url('/coats/', view_func=views.reference.coat_guide, name="coat_guide"),
    url('/coats/<coat_canon_name>/', view_func=views.reference.coat_view_all, name="coat_view_all"),
    url('/coat/<coat_canon_name>/<species_canon_name>/', view_func=views.reference.coat_view,
        name="coat_view"),
]

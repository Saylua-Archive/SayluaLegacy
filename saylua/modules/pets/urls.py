from saylua.routing import url
from . import views

urlpatterns = [
    url('/pets/', view_func=views.reference.species_guide, name="species"),

    # Pet profiles and actions.
    url('/pet/<name>/', view_func=views.general.pet_profile, name="profile", methods=['GET', 'POST']),
    url('/edit_pet/<name>/', view_func=views.general.edit_pet, name="edit_pet", methods=['GET', 'POST']),
    url('/accompany/<soul_name>/', view_func=views.general.pet_accompany, name="accompany", methods=['POST']),
    url('/abandon/', view_func=views.general.pet_abandon, name="abandon", methods=['POST']),

    url('/den/', view_func=views.den.pet_den, name="den", methods=['GET', 'POST']),

    url('/reserve/', view_func=views.reserve.pet_reserve, name="reserve", methods=['GET']),
    url('/reserve/', view_func=views.reserve.pet_reserve_post, name="reserve_post", methods=['POST']),

    url('/species/', view_func=views.reference.species_guide, name="species_guide"),
]

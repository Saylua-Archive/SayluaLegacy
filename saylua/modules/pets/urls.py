from saylua.routing import url
from . import views

urlpatterns = [
    url('/pet/<name>/', view_func=views.pet_profile, name="profile", methods=['GET', 'POST']),
    url('/edit_pet/<name>/', view_func=views.pet_profile, name="profile", methods=['GET', 'POST']),
    url('/reserve/', view_func=views.pet_reserve, name="reserve", methods=['GET']),
    url('/reserve/', view_func=views.pet_reserve_post, name="reserve_post", methods=['POST']),
    url('/abandon/', view_func=views.pet_abandon, name="abandon", methods=['POST']),
    url('/accompany/<soul_name>/', view_func=views.pet_accompany, name="accompany", methods=['POST']),
    url('/species/', view_func=views.species_guide, name="species_guide"),
]

from saylua.routing import url
from . import views

urlpatterns = [
    url('/pet/<name>/', view_func=views.pet_profile, name="pets_profile", methods=['GET', 'POST']),
    url('/reserve/', view_func=views.pet_reserve, name="pets_reserve", methods=['GET', 'POST']),
    url('/abandon/', view_func=views.pet_abandon, name="pets_abandon", methods=['POST']),
    url('/accompany/', view_func=views.pet_accompany, name="pets_accompany", methods=['POST'])
]

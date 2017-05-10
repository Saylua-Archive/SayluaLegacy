from saylua.routing import url
from . import views

urlpatterns = [
    url('/pet/<name>/', view_func=views.pet_profile, name="pets_profile", methods=['GET', 'POST']),
    url('/reserve/', view_func=views.pet_reserve, name="pets_reserve", methods=['GET', 'POST'])
]

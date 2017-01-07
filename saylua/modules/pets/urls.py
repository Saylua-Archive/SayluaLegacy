from saylua.routing import url
from . import views

urlpatterns = [
    url('/pet/<name>/', view_func=views.pet_profile, name="pets_profile"),
    url('/room/<name>/', view_func=views.pet_room, name="pets_room"),
    url('/adopt/', view_func=views.pet_adoption, name="pets_adoption"),
    url('/den/', view_func=views.pet_collection_default, name="pets_collection_default"),
    url('/den/<username>', view_func=views.pet_collection, name="pets_collection"),
]

from saylua.routing import url
from . import views

urlpatterns = [
    url('/adventure/', view_func=views.home, name='adventure_home', methods=['GET']),

    # API routes
    url('/adventure/api/generate_dungeon',
        view_func=views.generate_dungeon,
        methods=['POST']
    ),
    url('/adventure/api/list_entities',
        view_func=views.api_entity_list,
        methods=['POST']
    ),
    url('/adventure/api/list_tiles',
        view_func=views.api_tile_list,
        methods=['POST']
    )
]

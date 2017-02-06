from saylua.routing import url
from . import views

urlpatterns = [
    url('/explore/', view_func=views.home, name='explore_home', methods=['GET']),
    url('/battle/', view_func=views.battle, name='explore_battle', methods=['GET']),

    # API routes
    url('/explore/api/generate_dungeon',
        view_func=views.generate_dungeon,
        methods=['POST']
    ),
    url('/explore/api/list_entities',
        view_func=views.api_entity_list,
        methods=['POST']
    ),
    url('/explore/api/list_tiles',
        view_func=views.api_tile_list,
        methods=['POST']
    )
]

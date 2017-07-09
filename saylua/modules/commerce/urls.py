from saylua.routing import url
from . import views


urlpatterns = [
    # Bank URls
    url('/bank/', view_func=views.bank.bank_main, name='bank', methods=['GET', 'POST']),
    url('/bank/transfer/', view_func=views.bank.bank_transfer, name='bank_transfer', methods=['GET', 'POST']),

    # Market URls
    url('/market/', view_func=views.market.market_main, name='market', methods=['GET', 'POST']),

    # Shop URLs
    url('/shop/<name>/', view_func=views.shops.npc_shop_view, name='view_shop', methods=['GET', 'POST']),
]

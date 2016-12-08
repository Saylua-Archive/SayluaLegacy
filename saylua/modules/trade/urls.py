from saylua.routing import url
from . import views


urlpatterns = [
  # Bank URls
  url('/bank/', view_func=views.bank.bank_main, name='bank', methods=['GET', 'POST']),
  url('/bank/transfer/', view_func=views.bank.bank_transfer, name='bank_transfer', methods=['GET', 'POST']),

  # Shop URLs
  url('/shop/<name>/', view_func=views.shops.npc_shop_view, name='shops_npc_view'),
  url('/usershop/<username>/', view_func=views.shops.user_shop_view, name='shops_user_view')
]

from saylua.routing import url
from . import views

urlpatterns = [
    url('/avatar/', view_func=views.customize, name='avatar_customize', methods=['GET', 'POST'])
]

import api # noqa

from saylua.wrappers import login_required


@login_required()
def pet_den():
    return "Hello World"

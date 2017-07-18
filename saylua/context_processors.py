from saylua import app

from saylua.utils import get_static_version_id


# Injected functions.

@app.context_processor
def inject_include_static():
    def include_static(file_path):
        return '/static' + '/' + file_path + '?v=' + str(get_static_version_id())

    return dict(include_static=include_static)

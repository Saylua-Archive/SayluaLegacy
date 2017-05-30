from flask import Markup, request, render_template


class Pagination:
    def __init__(self, per_page=10, query=None, current_page=None,
            url_base="?page=", url_end=""):
        if current_page is None:
            try:
                current_page = int(request.args.get('page', 1))
            except (TypeError, ValueError):
                current_page = 1
        current_page = max(current_page, 1)
        self.current_page = current_page
        self.per_page = per_page
        self.url_base = url_base
        self.url_end = url_end
        if query is not None:
            self.items = query.limit(per_page).offset((current_page - 1) * per_page).all()
            self.item_count = query.count()
            self.page_count = (per_page + self.item_count - 1) // per_page
        else:
            # Use placeholder if there's no query.
            self.page_count = 10

    def render(self):
        return Markup(render_template("pagination.html", current_page=self.current_page,
            page_count=self.page_count, url_base=self.url_base, url_end=self.url_end,
            page_buffer=2))

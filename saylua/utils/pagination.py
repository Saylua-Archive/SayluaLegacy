from flask import Markup


class PageData:
    def __init__(self, model, per_page, page_number=1):
        self.model = model
        self.per_page = per_page
        self.page_number = page_number
        self.pagination = Markup()

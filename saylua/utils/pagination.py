from flask import Markup


class PageData:
    def __init__(self, model, per_page, page_number=1):
        self.model = model
        self.per_page = per_page
        self.page_number = page_number
        self.pagination = Markup()


def pagination(current_page=1, page_count=10, url_base="?page=", url_end="", page_buffer=2):
    if page_count > 1:
        start_page_range = current_page - page_buffer
        end_page_range = current_page + page_buffer
        if start_page_range < 1:
            end_page_range = end_page_range - (start_page_range - 1)
            start_page_range = 1
        if end_page_range > page_count:
            start_page_range = start_page_range - (end_page_range - page_count)
            if start_page_range < 1:
                start_page_range = 1
            end_page_range = page_count

        result = "<div class=\"pagination\">"

        if current_page > 1:
            result += "<a href=\""
            result += url_base
            result += str(current_page - 1) + url_end + "\">&#8592; Prev</a>"
        else:
            result += "<span>&#8592; Prev</span>"

        if start_page_range > 1:
            result += "<a href=\"" + url_base + "1" + url_end + "\">1</a>"
            result += "<span>...</span>"

        for i in range(start_page_range, end_page_range + 1):
            if i == current_page:
                result += "<span class=\"active\">" + str(i) + "</span>"
            else:
                result += "<a href=\"" + url_base + str(i) + url_end + "\">" + str(i) + "</a>"

        if end_page_range < page_count:
            result += "<span>...</span>"
            result += "<a href=\"" + url_base + str(page_count) + url_end + "\">" + str(page_count)
            result += "</a>"

        if current_page < page_count:
            result += "<a href=\"" + url_base + str(current_page + 1) + url_end + "\">Next &#8594;</a>"
        else:
            result += "<span>Next &#8594;</span>"
        result += "</div>"
        return result

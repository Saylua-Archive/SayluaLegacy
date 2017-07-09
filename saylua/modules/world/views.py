from flask import render_template


def town_main():
    return render_template("town.html")

def free_items():
    return render_template("free_items.html")

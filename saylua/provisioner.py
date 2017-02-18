from saylua import db
from saylua.models.role import Role
from saylua.utils import is_devserver
from saylua.modules.forums.models.db import Board, BoardCategory, ForumThread, ForumPost
from saylua.models.user import User, DisplayName
from saylua.modules.pets.soulnames import soulname
from saylua.modules.explore.dungeons.provision import provision_dungeon_schema


# To run this import setup in the interactive console and run it as such
# After that, edit a user's role to be admin to create the first admin
# Then, flush the memcache to make sure the user's role is updated
#
# from saylua.provisioner import setup
# setup()

def generate_admin_user():
    display_name = "admin"
    role_name = "admin"
    phash = User.hash_password("password")  # Yes, the default password is password
    email = "admin@saylua.wizards"

    yield User(
        display_name=display_name,
        phash=phash,
        email=email,
        role_name=role_name,
        star_shards=15,
        cloud_coins=50000
    )


def generate_boards():
    categories = ["Saylua Talk", "Help", "Real Life", "Your Pets"]

    for category in categories:
        category = BoardCategory(title=category)
        yield category

        for n in range(4):
            title = soulname(7)
            url_slug = title
            description = "A board for talking about " + title

            yield Board(
                title=title,
                url_slug=url_slug,
                categories=[category],
                description=description
            )


def generate_threads():
    for board in db.session.query(Board).all():
        for i in range(3):
            title = "I really, really like {}!".format(soulname(24))
            author = 1

            yield ForumThread(title=title, author=author, board=board)


def generate_posts():
    from random import randrange, choice

    content_phrases = [
        "I'm a big fan of {}.",
        "This post fills me with determination.",
        "Don't forget about the power of {}!",
        "Wow! I've never heard that before!",
        "{} is how I remember to smile at night.",
        "Calm down.",
        "Why isn't anyone talking about {}?",
        "I was thinking the same thing, actually."
        "Is {} even real?",
        "Why would you say that???",
        "Absolutely phenomenal!!!! Did you guys see {} last night?!?",
        "Look, do you even know what that means?",
        "This is all meaningless. {} is just a societal construct.",
        "That sounds great, but I don't know if I can trust your opinion.",
        "I really, really like {}!"
    ]

    for thread in db.session.query(ForumThread).all():
        for i in range(randrange(1, 15)):
            body = choice(content_phrases).format(soulname(24))
            author = 1

            yield ForumPost(body=body, author=author, thread=thread)


def generate_users():
    for i in range(4):
        display_name = soulname(7)
        phash = User.hash_password("password")  # Yes, the default password is password
        email = "{0}@dongs.{0}.biz".format(display_name)

        yield User(
            display_name=display_name,
            phash=phash,
            email=email,
            star_shards=15,
            cloud_coins=50000
        )


def purge(absolutely_sure_about_this=False):
    """Removes existing models from the database."""

    if is_devserver() or absolutely_sure_about_this:
        db.drop_all()
        db.session.commit()
        db.session.flush()
        db.create_all()

    else:
        raise Exception("Get out of here.")


def setup():
    # Create the role "admin" with all privileges
    admin_role = Role(name="admin")
    role_columns = [column.key for column in admin_role.__table__.columns]

    for key in role_columns:
        if key.startswith("can"):
            setattr(admin_role, key, True)

    db.session.add(admin_role)
    print("Admin Role Created")

    # Add the "user" role
    user_role = Role(name="user")
    user_role.can_post_threads = True
    user_role.can_comment = True
    db.session.add(user_role)
    print("User Role Created")

    # Add the "moderator" role
    moderator_role = Role(name="moderator")
    moderator_role.can_post_threads = True
    moderator_role.can_move_threads = True
    moderator_role.can_comment = True
    db.session.add(moderator_role)
    print("Moderator Role Created")

    # Turn dungeon schemas into models
    for model in provision_dungeon_schema():
        db.session.add(model)

    db.session.commit()

    # Add placeholders if on the dev server
    if is_devserver():
        print("Adding Initial Admin User")
        for item in generate_admin_user():
            db.session.add(item)

        print("Adding Placeholder Users")
        for item in generate_users():
            db.session.add(item)

        print("Adding Placeholder Boards")
        for item in generate_boards():
            db.session.add(item)

        print("Adding Placeholder Threads")
        for item in generate_threads():
            db.session.add(item)

        print("Adding Placeholder Posts")
        for item in generate_posts():
            db.session.add(item)

        db.session.commit()

    print("Database Setup Complete")

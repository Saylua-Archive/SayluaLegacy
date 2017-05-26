from saylua import app, db
from saylua.utils import is_devserver
from saylua.modules.forums.models.db import Board, BoardCategory, ForumThread, ForumPost
from saylua.models.user import User, Role
from saylua.modules.items.models.db import Item, InventoryItem
from saylua.modules.pets.models.db import Pet, Species, SpeciesCoat
from saylua.modules.pets.soul_names import soul_name
from saylua.modules.explore.dungeons.provision import provision_dungeon_schema

import os


# To run this import setup in the interactive console and run it as such
# After that, edit a user's role to be admin to create the first admin
# Then, flush the memcache to make sure the user's role is updated
#
# from saylua.provisioner import setup
# setup()

def generate_admin_user():
    username = "admin"
    role_name = "admin"
    password_hash = User.hash_password("password")  # Yes, the default password is password.
    email = "admin@saylua.wizards"

    yield User(
        username=username,
        password_hash=password_hash,
        email=email,
        role_name=role_name,
        star_shards=15,
        cloud_coins=50000
    )


def generate_items():
    subpath = 'img' + os.sep + 'items' + os.sep
    path = os.path.join(app.static_folder, subpath)
    admin = db.session.query(User).filter(User.active_username == 'admin').one()
    for img in os.listdir(path):
        item_name, ext = os.path.splitext(img)
        if ext.lower() == '.png':
            item = Item(
                name=item_name,
                canon_name=item_name,
                description='A lovely little ' + item_name + ' for you to much on,'
            )

            yield item

            # Give admin lots of items.
            yield InventoryItem(
                user=admin,
                item=item,
                count=99
            )


def generate_pets():
    subpath = 'img' + os.sep + 'pets' + os.sep
    path = os.path.join(app.static_folder, subpath)
    for species_name in os.listdir(path):
        species_path = path + species_name + os.sep
        if os.path.isdir(species_path):
            new_species = Species(name=species_name, description="A species of great beauty.")
            yield new_species
            for img_name in os.listdir(species_path):
                coat_name, ext = os.path.splitext(img_name)
                if ext.lower() == '.png':
                    new_coat = SpeciesCoat(
                        name=coat_name,
                        species_name=species_name,
                        description=("A beautiful " + species_name))
                    yield new_coat
                    soul_name = Pet.new_soul_name()
                    new_pet = Pet(
                        soul_name=soul_name,
                        coat_id=new_coat.id,
                        species_name=species_name,
                        name=soul_name.capitalize()
                    )
                    yield new_pet


def generate_boards():
    categories = ["Saylua Talk", "Help", "Real Life", "Your Pets"]

    for category in categories:
        category = BoardCategory(title=category)
        yield category

        for n in range(4):
            title = soul_name(7)
            description = "A board for talking about " + title

            yield Board(
                title=title,
                canon_name=title,
                category=category,
                description=description,
                order=(n + 1)
            )

    title = soul_name(7)
    yield Board(
        title=title + " announcements",
        canon_name='news',
        category=category,
        description="Announcements for " + title,
        order=0
    )


def generate_threads():
    for board in db.session.query(Board).all():
        for i in range(3):
            title = "I really, really like {}!".format(soul_name(24))
            author = 1

            yield ForumThread(title=title, author_id=author, board=board)


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
        "I was thinking the same thing, actually.",
        "Is {} even real?",
        "Why would you say that???",
        "Absolutely phenomenal!!!! Did you guys see {} last night?!?",
        "Look, do you even know what that means?",
        "This is all meaningless. {} is just a societal construct.",
        "That sounds great, but I don't know if I can trust your opinion.",
        "I really, really like {}!"
    ]

    users = db.session.query(User).all()

    for thread in db.session.query(ForumThread).all():
        for i in range(randrange(1, 15)):
            body = choice(content_phrases).format(soul_name(24))
            author = choice(users).id

            yield ForumPost(body=body, author_id=author, thread=thread)


def generate_users():
    for i in range(4):
        username = soul_name(7)
        password_hash = User.hash_password("password")  # Yes, the default password is password

        email = "{0}@dongs.{0}.biz".format(username)

        yield User(
            username=username,
            password_hash=password_hash,
            email=email,
            star_shards=15,
            cloud_coins=50000
        )


def purge(absolutely_sure_about_this=False):
    """Removes existing models from the database."""
    with app.app_context():
        if is_devserver() or absolutely_sure_about_this:
            db.drop_all()
            db.session.commit()
            db.session.flush()
            db.create_all()

        else:
            raise Exception("Get out of here.")


def setup():
    with app.app_context():
        db.create_all()

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
        db.session.add(user_role)
        print("User Role Created")

        # Add the "moderator" role
        moderator_role = Role(name="moderator")
        moderator_role.can_moderate = True
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

            print("Adding Placeholder Items")
            for item in generate_items():
                db.session.add(item)

            print("Adding Placeholder Pets, Coats, and Species")
            for pet_coat_species in generate_pets():
                db.session.add(pet_coat_species)

            db.session.commit()

        print("Database Setup Complete")

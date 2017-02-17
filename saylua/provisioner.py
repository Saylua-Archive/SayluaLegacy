from saylua import db
from saylua.models.role import Role
from saylua.utils import is_devserver
from saylua.modules.forums.models.db import Board, BoardCategory
from saylua.models.user import User
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
    username = "admin"
    phash = User.hash_password("password")  # Yes, the default password is password
    email = "admin@saylua.wizards"
    role = "admin"

    admin_user = User(display_name=display_name, usernames=[username], phash=phash,
        email=email, role_id=role)

    return admin_user


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
    admin_role = Role(id="admin")
    admin_dict = admin_role.to_dict()
    for entry in admin_dict:
        setattr(admin_role, entry, True)
    admin_role.put()
    print("Admin Role Created")

    # Add the "user" role
    user_role = Role(id="user")
    user_role.can_post_threads = True
    user_role.can_comment = True
    user_role.put()
    print("User Role Created")

    # Add the "moderator" role
    moderator_role = Role(id="moderator")
    moderator_role.can_post_threads = True
    moderator_role.can_move_threads = True
    moderator_role.can_comment = True
    moderator_role.put()
    print("Moderator Role Created")

    # Turn dungeon schemas into models
    for model in provision_dungeon_schema():
        db.session.add(model)

    db.session.commit()

    # Add placeholders if on the dev server
    if is_devserver():
        print("Adding Initial Admin User")
        admin_user = generate_admin_user()
        admin_user.put()

        print("Adding Placeholder Users")
        users = []

        for i in range(4):
            display_name = soulname(7)
            username = display_name
            phash = User.hash_password("password")  # Yes, the default password is password
            email = username + "@" + username + ".biz"
            new_user = User(display_name=display_name, usernames=[username], phash=phash,
                email=email, star_shards=15, cloud_coins=50000)
            users.append(new_user.put().id())  # Add users to database, and their IDs to a list

        print("Adding Placeholder Boards")
        categories = ["Saylua Talk", "Help", "Real Life", "Your Pets"]
        for category in categories:
            category = BoardCategory(title=category)
            db.session.add(category)

            for n in range(4):
                title = soulname(7)
                url_slug = title
                description = "A board for talking about " + title

                new_board = Board(
                    title=title,
                    url_slug=url_slug,
                    categories=[category],
                    description=description
                )

                db.session.add(new_board)

        db.session.commit()

    print("Database Setup Complete")

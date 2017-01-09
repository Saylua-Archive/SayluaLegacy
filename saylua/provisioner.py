from saylua.models.role import Role

# To run this import setup in the interactive console and run it as such
# After that, edit a user's role to be admin to create the first admin
# Then, flush the memcache to make sure the user's role is updated
#
# from saylua.provisioner import setup
# setup()


def setup():
    # Create the role 'admin' with all privileges
    admin_role = Role(id='admin')
    admin_dict = admin_role.to_dict()
    for entry in admin_dict:
        setattr(admin_role, entry, True)
    admin_role.put()
    print("Admin Role Created")

    # Add the 'user' role
    user_role = Role(id='admin')
    user_role.can_post_threads = True
    user_role.can_comment = True
    user_role.put()
    print("User Role Created")

    print("Database Setup Complete")

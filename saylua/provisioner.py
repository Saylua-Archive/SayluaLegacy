from saylua.models.role import Role

# To run this import setup in the interactive console and run it as such
# After that, edit a user's role to be admin to create the first admin
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

    print("Database Setup Complete")

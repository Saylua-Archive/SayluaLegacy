from saylua.models.role import Role
from saylua.utils import is_devserver
from saylua.modules.forums.models.db import Board, BoardCategory, ForumThread, ForumPost
from saylua.models.user import User
from saylua.modules.pets.soulnames import soulname

# To run this import setup in the interactive console and run it as such
# After that, edit a user's role to be admin to create the first admin
# Then, flush the memcache to make sure the user's role is updated
#
# from saylua.provisioner import setup
# setup()

def generate_admin_user():
    display_name = 'admin'
    username = 'admin'
    phash = '$2a$01$c1I8kCq3L1YgMDu4Hb.4COFJBWMqnjnZhyBvfaBPOOuVfPimvLAQq'
    email = 'admin@saylua.wizards'

    admin_user = User(display_name=display_name, usernames=[username], phash=phash,
        email=email)

    admin_user.put()

def setup():
    # Create the role 'admin' with all privileges
    admin_role = Role(id='admin')
    admin_dict = admin_role.to_dict()
    for entry in admin_dict:
        setattr(admin_role, entry, True)
    admin_role.put()
    print('Admin Role Created')

    # Add the 'user' role
    user_role = Role(id='user')
    user_role.can_post_threads = True
    user_role.can_comment = True
    user_role.put()
    print('User Role Created')

    # Add the 'moderator' role
    moderator_role = Role(id='moderator')
    moderator_role.can_post_threads = True
    moderator_role.can_move_threads = True
    moderator_role.can_comment = True
    moderator_role.put()
    print('Moderator Role Created')

    # Add placeholders if on the dev server
    if is_devserver():
        print('Adding Initial Admin User')
        generate_admin_user()

        print('Adding Placeholder Users')
        users = []

        for i in range(4):
            display_name = soulname(7)
            username = display_name
            #The following hash corresponds to the password 'password' so you can use that to test
            phash = '$2a$01$c1I8kCq3L1YgMDu4Hb.4COFJBWMqnjnZhyBvfaBPOOuVfPimvLAQq'
            email = username + '@' + username + '.biz'
            new_user = User(display_name=display_name, usernames=[username], phash=phash,
                email=email)
            users.append(new_user.put().id()) #Add users to database, and their IDs to a list


        print('Adding Placeholder Board Categories')
        categories = ['Saylua Talk', 'Help', 'Real Life', 'Your Pets']
        for category in categories:
            BoardCategory(title=category).put()

        print('Adding Placeholder Boards')





    print('Database Setup Complete')

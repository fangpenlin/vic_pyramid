from __future__ import unicode_literals
import os
import sys
import transaction
import getpass

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from ..models import tables
from ..models import setup_database
from ..models.user import UserModel
from ..models.group import GroupModel
from ..models.permission import PermissionModel


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd)) 
    sys.exit(1)


def main(argv=sys.argv, input_func=raw_input, getpass_func=getpass.getpass):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    
    # create all tables
    settings = setup_database({}, **settings)
    engine = settings['engine']
    tables.DeclarativeBase.metadata.create_all(engine)
    
    session = settings['session']
    user_model = UserModel(session)
    group_model = GroupModel(session)
    permission_model = PermissionModel(session)
    
    with transaction.manager:
        admin = user_model.get_by_name('admin')
        if admin is None:
            print 'Create admin account'
            
            email = input_func(b'Email:')
            
            password = getpass_func(b'Password:')
            confirm = getpass_func(b'Confirm:')
            if password != confirm:
                print 'Password not match'
                return
        
            admin = user_model.create(
                user_name='admin',
                display_name='Administrator',
                email=email,
                password=password, 
                verified=True, 
            )
            print 'Created admin, user_id=%s' % admin.user_id
            
        permission = permission_model.get_by_name('admin')
        if permission is None:
            print 'Create admin permission ...'
            permission = permission_model.create(
                permission_name='admin',
                display_name='Administrate',
            )
            
        group = group_model.get_by_name('admin')
        if group is None:
            print 'Create admin group ...'
            group = group_model.create(
                group_name='admin',
                display_name='Administrators',
            )
            
        print 'Add admin permission to admin group'
        group_model.update(group, permissions=[permission])
        session.flush()
            
        print 'Add admin to admin group'
        user_model.update_groups(admin.user_id, group_ids=[group.group_id])
        session.flush()

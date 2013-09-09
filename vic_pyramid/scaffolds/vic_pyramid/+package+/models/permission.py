from __future__ import unicode_literals

from . import tables
from .base import BaseTableModel


class PermissionModel(BaseTableModel):
    """Permission data model
    
    """
    TABLE = tables.Permission
    
    def get_by_name(self, permission_name):
        """Get a permission by name
        
        """
        permission = (
            self.session
            .query(self.TABLE)
            .filter_by(permission_name=permission_name)
            .first()
        )
        return permission
        
    def get_permissions(self):
        """Get permissions
        
        """
        query = self.session.query(self.TABLE)
        return query
    
    def create(
        self, 
        permission_name, 
        description=None,
    ):
        """Create a new permission and return its id
        
        """
        permission = self.TABLE(
            permission_name=unicode(permission_name), 
            description=unicode(description) if description is not None else None, 
        )
        self.session.add(permission)
        # flush the change, so we can get real id
        self.session.flush()
        assert permission.permission_id is not None, \
            'Permission id should not be none here'
        permission_id = permission.permission_id
        
        self.logger.info('Create permission %s', permission_name)
        return permission_id
    
    def update_permission(self, permission_id, **kwargs):
        """Update attributes of a permission
        
        """
        permission = self.get(permission_id)
        if permission is None:
            raise KeyError
        if 'description' in kwargs:
            permission.description = kwargs['description']
        if 'permission_name' in kwargs:
            permission.permission_name = kwargs['permission_name']
        self.session.add(permission)

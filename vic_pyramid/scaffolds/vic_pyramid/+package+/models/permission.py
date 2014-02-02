from __future__ import unicode_literals

from . import tables
from .base import BaseTableModel
from .base import NOT_SET


class PermissionModel(BaseTableModel):
    """Permission data model
    
    """
    TABLE = tables.Permission
    
    def get_by_name(self, permission_name):
        """Get a permission by name
        
        """
        permission = (
            self.session
            .query(tables.Permission)
            .filter_by(permission_name=permission_name)
        ).first()
        return permission
    
    def create(
        self, 
        permission_name, 
        description=None,
    ):
        """Create a new permission and return its id
        
        """
        permission = tables.Permission(
            permission_name=unicode(permission_name), 
            description=unicode(description) if description is not None else None, 
        )
        self.session.add(permission)
        self.session.flush()
        return permission
    
    def update(
        self, 
        permission, 
        description=NOT_SET, 
        permission_name=NOT_SET,
    ):
        """Update attributes of a permission
        
        """
        if description is not NOT_SET:
            permission.description = description
        if permission_name is not NOT_SET:
            permission.permission_name = permission_name
        self.session.flush()

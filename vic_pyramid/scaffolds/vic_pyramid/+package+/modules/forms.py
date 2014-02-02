from __future__ import unicode_literals

from wtforms import ValidationError


def are_similar(left, right):
    """Return are two strings too similar
    
    """
    left = left.lower()
    right = right.lower()
    if left == right:
        return True
    if left and left in right:
        return True
    if right and right in left:
        return True
    return False


def similar(target, message):
    """This validator make sure that two fileds are not too similar. Mainly
    for comparing password and user name
    
    """
    def callee(form, field):
        try:
            other = form[target]
        except KeyError:
            raise ValidationError(
                field.gettext("Invalid field name '%s'.") % target)
        
        other_data = other.data.lower()
        my_data = field.data.lower()
        if are_similar(other_data, my_data):
            raise ValidationError(message)
    return callee

from app.models import AuthRole, AuthPermission, db

def create_or_update_role(role_dict):
    role = AuthRole.get_or_create(key=role_dict['key'])
    role.permissions = []
    for permission_key in role_dict['permissions']:
        permission = AuthPermission.get_or_create(key=permission_key)
        role.permissions.append(permission)
        permission.save()
    role.save()

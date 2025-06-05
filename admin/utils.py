from core.base_utils import get_admins_ids


def user_is_admin(user_id):
    admins = get_admins_ids()
    if user_id in admins:
        return True

    return False
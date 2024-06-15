def can_admin(user):
    try:
        return user.is_authenticated and user.username == 'jsaadatm'
    except Exception:
        return False
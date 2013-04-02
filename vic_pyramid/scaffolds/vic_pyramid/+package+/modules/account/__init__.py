def includeme(config):
    config.add_route('account.login', '/login')
    config.add_route('account.logout', '/logout')
    config.add_route('account.forgot_password', '/forgot_password')
    config.add_route('account.recovery_password', '/recovery_password')

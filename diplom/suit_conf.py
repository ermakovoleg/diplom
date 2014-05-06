#coding: utf-8
SUIT_CONFIG = {
    'ADMIN_NAME': 'Диплом "Соберем все!"',
    'HEADER_DATE_FORMAT': 'l, j F Y',
    'SEARCH_URL': '',

    'MENU': (

        # Keep original label and models
        'sites',

        # Rename app and set icon
        #{'app': 'auth', 'label': 'Пользователи', 'icon': 'icon-user'},


        # Custom app, with models
        {'label': 'Пользователи', 'icon': 'icon-user',
         'models': ('user.myuser', 'user.mygroup', 'user.district', 'user.Locality', 'user.groupmeta')},

        {'label': 'Запросы', 'icon': 'icon-list-alt',
         'models': ('forms_custom.template', 'forms_custom.templatefield')},

        {'label': 'Отчеты', 'icon': 'icon-file',
         'models': ('reports.reportmaps',)},
'''
        # Cross-linked models with custom name; Hide default icon
        {'label': 'Custom', 'icon': None, 'models': (
            'user.mygroup',
            {'model': 'user.myuser', 'label': 'Staff'}
        )},

        # Custom app, no models (child links)
        {'label': 'Users', 'url': 'user.myuser', 'icon':'icon-user'},

        # Separator
        '-',

        # Custom app and model with permissions
        {'label': 'Secure', 'permissions': 'auth.add_user', 'models': [
            {'label': 'custom-child', 'permissions': ('auth.add_user', 'auth.add_group')}
        ]},
'''
    )

}

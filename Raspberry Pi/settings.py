RESOURCE_METHODS = ['GET', 'POST']

ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

schema = {
    # Schema definition, based on Cerberus grammar. Check the Cerberus project
    # (https://github.com/nicolaiarocci/cerberus) for details.
    'usuario': {
        'type': 'string',
    },
    'identificador': {
        'type': 'string',
    },
    'sesion': {
        'type': 'string',
        'allowed': ["A", "B", "C"],
    },
    't': {
        'type': 'string',
    },
    'T': {
        'type': 'string',
    },
    'SP': {
        'type': 'string',
    }
}

medida = {

    'item_title': 'medida',

    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'identificador'
    },

    'cache_control': 'max-age=10,must-revalidate',

    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,

    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH', 'PUT', 'DELETE'],

    'schema': schema
}

DOMAIN = {
    'medida': medida,
}

def error_response(error_type, error_description):
    return {
        'error': error_type,
        'error_description': error_description
    }
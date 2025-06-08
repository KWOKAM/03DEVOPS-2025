
"""
Ce que nous traitons dans cette partie :
- un middleware pour activer l'authentification par cookie `Token` (en l'injectant dans les en-tetes),
- un middleware pour desactiver le cache HTTP afin de garantir que les donnees sont toujours a jour.
"""

def middleware_token_cookie(get_response):
  
    def middleware(request):
        jeton = request.COOKIES.get('Token')
        if jeton is not None:
            request.META['HTTP_AUTHORIZATION'] = f'Token {jeton}'

        return get_response(request)

    return middleware

def middleware_désactiver_cache(get_response):

    def middleware(request):
        reponse = get_response(request)
        reponse['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return reponse

    return middleware

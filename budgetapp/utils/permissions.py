def est_proprietaire_ou_admin(utilisateur, objet):
    est_proprio_direct = getattr(objet, 'owner', None) == utilisateur
    est_identique = objet == utilisateur
    est_admin = utilisateur.is_staff

    return est_proprio_direct or est_identique or est_admin

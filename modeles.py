class Etablissement:
    def __init__(self, id_etab: str, nom: str, type_etab: str, localite: str, capacite: int):
        self.id_etab = id_etab
        self.nom = nom
        self.type_etab = type_etab  # "Public" ou "Prive"
        self.localite = localite
        self.capacite = int(capacite)
        self.places_restantes = int(capacite)

    def est_disponible(self) -> bool:
        """Vérifie s'il reste des places libres dans l'établissement."""
        return self.places_restantes > 0

    def reserver_place(self) -> bool:
        """Réserve une place si l'établissement est disponible."""
        if self.est_disponible():
            self.places_restantes -= 1
            return True
        return False


class Eleve:
    def __init__(self, matricule: str, nom: str, prenom: str, date_naissance: str, sexe: str, moyenne: float, etab_origine: str, choix: list):
        self.matricule = matricule
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.sexe = sexe
        self.moyenne = float(moyenne)
        self.etab_origine = etab_origine
        self.choix = choix  # Liste de 3 IDs d'établissements
        self.statut = "NON_AFFECTE"
        self.affectation = None
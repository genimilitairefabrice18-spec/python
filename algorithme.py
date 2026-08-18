from database import (
    obtenir_tous_eleves,
    obtenir_tous_etablissements,
    mettre_a_jour_affectation,
    get_connection,
    reinitialiser_affectations
)

def lancer_affectation_automatique():
    """
    Exécute l'algorithme d'affectation basé sur le mérite (moyenne)
    et les vœux des élèves.
    """
    # 1. On réinitialise les affectations précédentes
    reinitialiser_affectations()

    # 2. Récupérer les établissements sous forme de dictionnaire pour accès rapide
    #    Exemple: {'ETAB01': {'nom': 'Lycée A', 'places_restantes': 30}, ...}
    etablissements_raw = obtenir_tous_etablissements()
    etablissements = {
        e['id_etab']: {
            'nom': e['nom'],
            'places_restantes': e['places_restantes']
        }
        for e in etablissements_raw
    }

    # 3. Récupérer tous les élèves (déjà triés par moyenne DESC dans database.py)
    eleves = obtenir_tous_eleves()

    stats = {
        "total_eleves": len(eleves),
        "affectes": 0,
        "non_affectes": 0,
        "choix_1": 0,
        "choix_2": 0,
        "choix_3": 0
    }

    # 4. Parcourir chaque élève du meilleur au moins bon
    for eleve in eleves:
        affecte = False
        
        # Parcourir les choix de l'élève (rang 1, 2, 3)
        for rang, id_etab in enumerate(eleve['choix'], start=1):
            if id_etab in etablissements and etablissements[id_etab]['places_restantes'] > 0:
                # Place trouvée !
                etablissements[id_etab]['places_restantes'] -= 1
                
                # Mise à jour en base de données
                mettre_a_jour_affectation(eleve['matricule'], "AFFECTE", id_etab)
                
                # Mise à jour des statistiques
                stats["affectes"] += 1
                stats[f"choix_{rang}"] += 1
                affecte = True
                break
        
        if not affecte:
            stats["non_affectes"] += 1

    # 5. Mettre à jour les places restantes des établissements dans la BDD
    conn = get_connection()
    cursor = conn.cursor()
    for id_etab, data in etablissements.items():
        cursor.execute(
            "UPDATE etablissements SET places_restantes = ? WHERE id_etab = ?",
            (data['places_restantes'], id_etab)
        )
    conn.commit()
    conn.close()

    return stats
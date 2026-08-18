import sqlite3
import json

DB_NAME = "school_management.db"

def get_connection():
    """Établit la connexion à la base de données SQLite."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par leur nom
    return conn

def init_db():
    """Initialise les tables de la base de données."""
    conn = get_connection()
    cursor = conn.cursor()

    # Table des établissements
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS etablissements (
            id_etab TEXT PRIMARY KEY,
            nom TEXT NOT NULL,
            type_etab TEXT NOT NULL,
            localite TEXT NOT NULL,
            capacite INTEGER NOT NULL,
            places_restantes INTEGER NOT NULL
        )
    ''')

    # Table des élèves
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS eleves (
            matricule TEXT PRIMARY KEY,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            date_naissance TEXT,
            sexe TEXT,
            moyenne REAL NOT NULL,
            etab_origine TEXT,
            choix TEXT NOT NULL, -- Stocké au format JSON (ex: ["ETAB01", "ETAB02", "ETAB03"])
            statut TEXT DEFAULT 'NON_AFFECTE',
            affectation TEXT
        )
    ''')

    conn.commit()
    conn.close()

# --- FONCTIONS POUR LES ÉTABLISSEMENTS ---

def ajouter_etablissement(id_etab, nom, type_etab, localite, capacite):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO etablissements (id_etab, nom, type_etab, localite, capacite, places_restantes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (id_etab, nom, type_etab, localite, capacite, capacite))
    conn.commit()
    conn.close()

def obtenir_tous_etablissements():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM etablissements ORDER BY nom")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# --- FONCTIONS POUR LES ÉLÈVES ---

def ajouter_eleve(matricule, nom, prenom, date_naissance, sexe, moyenne, etab_origine, choix_list):
    conn = get_connection()
    cursor = conn.cursor()
    choix_json = json.dumps(choix_list)  # Convertit la liste en chaîne JSON
    cursor.execute('''
        INSERT OR REPLACE INTO eleves (matricule, nom, prenom, date_naissance, sexe, moyenne, etab_origine, choix)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (matricule, nom, prenom, date_naissance, sexe, moyenne, etab_origine, choix_json))
    conn.commit()
    conn.close()

def obtenir_tous_eleves():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM eleves ORDER BY moyenne DESC")
    rows = cursor.fetchall()
    conn.close()
    
    eleves = []
    for row in rows:
        item = dict(row)
        item['choix'] = json.loads(item['choix'])  # Reconvertit le JSON en liste Python
        eleves.append(item)
    return eleves

def mettre_a_jour_affectation(matricule, statut, affectation_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE eleves
        SET statut = ?, affectation = ?
        WHERE matricule = ?
    ''', (statut, affectation_id, matricule))
    conn.commit()
    conn.close()

def reinitialiser_affectations():
    """Réinitialise le statut de tous les élèves et remet les places disponibles."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE eleves SET statut = 'NON_AFFECTE', affectation = NULL")
    cursor.execute("UPDATE etablissements SET places_restantes = capacite")
    conn.commit()
    conn.close()
    
def supprimer_eleve(matricule):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM eleves WHERE matricule = ?", (matricule,))
    conn.commit()
    conn.close()

def supprimer_etablissement(id_etab):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM etablissements WHERE id_etab = ?", (id_etab,))
    conn.commit()
    conn.close()
    
def modifier_eleve(matricule, nom, prenom, date_naissance, sexe, moyenne, etab_origine, choix_list):
    conn = get_connection()
    cursor = conn.cursor()
    choix_json = json.dumps(choix_list)
    cursor.execute('''
        UPDATE eleves
        SET nom = ?, prenom = ?, date_naissance = ?, sexe = ?, moyenne = ?, etab_origine = ?, choix = ?
        WHERE matricule = ?
    ''', (nom, prenom, date_naissance, sexe, moyenne, etab_origine, choix_json, matricule))
    conn.commit()
    conn.close()

def modifier_etablissement(id_etab, nom, type_etab, localite, capacite):
    conn = get_connection()
    cursor = conn.cursor()
    # On met à jour la capacité et ajuste les places restantes
    cursor.execute('''
        UPDATE etablissements
        SET code = ?,nom = ?, type_etab = ?, localite = ?, capacite = ?, places_restantes = ?
        WHERE id_etab = ?
    ''', (code, nom, type_etab, localite, capacite, capacite, id_etab))
    conn.commit()
    conn.close()

def obtenir_eleve_par_matricule(matricule):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM eleves WHERE matricule = ?", (matricule,))
    row = cursor.fetchone()
    conn.close()
    if row:
        item = dict(row)
        item['choix'] = json.loads(item['choix'])
        return item
    return None

def obtenir_etablissement_par_id(id_etab):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM etablissements WHERE id_etab = ?", (id_etab,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None
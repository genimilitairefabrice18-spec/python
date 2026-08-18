from flask import Flask, render_template, request, redirect, url_for, flash
import database
import algorithme

app = Flask(__name__)
app.secret_key = "cle_secrete_fabschool"

# Initialisation de la BDD au démarrage
database.init_db()

@app.route("/")
def dashboard():
    eleves = database.obtenir_tous_eleves()
    etablissements = database.obtenir_tous_etablissements()
    
    total_eleves = len(eleves)
    total_etab = len(etablissements)
    affectes = sum(1 for e in eleves if e['statut'] == 'AFFECTE')
    non_affectes = total_eleves - affectes

    return render_template(
        "dashboard.html",
        total_eleves=total_eleves,
        total_etab=total_etab,
        affectes=affectes,
        non_affectes=non_affectes
    )

# --- ROUTES ÉLÈVES ---

@app.route("/eleves", methods=["GET", "POST"])
def page_eleves():
    if request.method == "POST":
        matricule = request.form.get("matricule")
        nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        date_naissance = request.form.get("date_naissance")
        sexe = request.form.get("sexe")
        moyenne = float(request.form.get("moyenne", 0))
        etab_origine = request.form.get("etab_origine")
        
        choix_1 = request.form.get("choix_1")
        choix_2 = request.form.get("choix_2")
        choix_3 = request.form.get("choix_3")
        choix = [c for c in [choix_1, choix_2, choix_3] if c]

        database.ajouter_eleve(matricule, nom, prenom, date_naissance, sexe, moyenne, etab_origine, choix)
        flash("Élève ajouté avec succès !", "success")
        return redirect(url_for("page_eleves"))

    eleves = database.obtenir_tous_eleves()
    etablissements = database.obtenir_tous_etablissements()
    
    # Dictionnaire {id_etab: nom_etab} pour afficher le nom au lieu du code
    etab_dict = {etab['id_etab']: etab['nom'] for etab in etablissements}

    return render_template("eleves.html", eleves=eleves, etablissements=etablissements, etab_dict=etab_dict)

@app.route("/eleves/modifier/<matricule>", methods=["GET", "POST"])
def modifier_eleve_route(matricule):
    if request.method == "POST":
        nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        date_naissance = request.form.get("date_naissance")
        sexe = request.form.get("sexe")
        moyenne = float(request.form.get("moyenne", 0))
        etab_origine = request.form.get("etab_origine")
        
        choix_1 = request.form.get("choix_1")
        choix_2 = request.form.get("choix_2")
        choix_3 = request.form.get("choix_3")
        choix = [c for c in [choix_1, choix_2, choix_3] if c]

        database.modifier_eleve(matricule, nom, prenom, date_naissance, sexe, moyenne, etab_origine, choix)
        flash("Élève modifié avec succès !", "success")
        return redirect(url_for("page_eleves"))

    eleve = database.obtenir_eleve_par_matricule(matricule)
    etablissements = database.obtenir_tous_etablissements()
    return render_template("modifier_eleve.html", eleve=eleve, etablissements=etablissements)

@app.route("/eleves/supprimer/<matricule>", methods=["POST"])
def supprimer_eleve_route(matricule):
    database.supprimer_eleve(matricule)
    flash("Élève supprimé avec succès !", "info")
    return redirect(url_for("page_eleves"))

# --- ROUTES ÉTABLISSEMENTS ---

@app.route("/etablissements", methods=["GET", "POST"])
def page_etablissements():
    if request.method == "POST":
        id_etab = request.form.get("id_etab")
        nom = request.form.get("nom")
        type_etab = request.form.get("type_etab")
        localite = request.form.get("localite")
        capacite = int(request.form.get("capacite", 0))

        database.ajouter_etablissement(id_etab, nom, type_etab, localite, capacite)
        flash("Établissement ajouté avec succès !", "success")
        return redirect(url_for("page_etablissements"))

    etablissements = database.obtenir_tous_etablissements()
    return render_template("etablissements.html", etablissements=etablissements)

@app.route("/etablissements/modifier/<id_etab>", methods=["GET", "POST"])
def modifier_etablissement_route(id_etab):
    if request.method == "POST":
        nom = request.form.get("nom")
        type_etab = request.form.get("type_etab")
        localite = request.form.get("localite")
        capacite = int(request.form.get("capacite", 0))

        database.modifier_etablissement(id_etab, nom, type_etab, localite, capacite)
        flash("Établissement modifié avec succès !", "success")
        return redirect(url_for("page_etablissements"))

    etablissement = database.obtenir_etablissement_par_id(id_etab)
    return render_template("modifier_etablissement.html", etab=etablissement)

@app.route("/etablissements/supprimer/<id_etab>", methods=["POST"])
def supprimer_etablissement_route(id_etab):
    database.supprimer_etablissement(id_etab)
    flash("Établissement supprimé avec succès !", "info")
    return redirect(url_for("page_etablissements"))

# --- AFFECTATION AUTOMATIQUE ---

@app.route("/lancer-affectation", methods=["POST"])
def lancer_affectation():
    stats = algorithme.lancer_affectation_automatique()
    flash(f"Affectation terminée ! {stats['affectes']} élèves affectés sur {stats['total_eleves']}.", "info")
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True, port=8050)
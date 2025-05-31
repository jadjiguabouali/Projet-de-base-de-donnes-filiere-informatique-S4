import sqlite3
import streamlit as st

# Connexion à la base de données
conn = sqlite3.connect('hotel.db', check_same_thread=False)
cursor = conn.cursor()

# Fonction pour consulter la liste des réservations
def consulter_reservations():
    try:
        cursor.execute('''
        SELECT r.Id_Reservation, r.Date_arrivee, r.Date_depart, 
               c.Nom_complet, ch.Numero
        FROM Reservation r
        JOIN Client c ON r.Id_Client = c.Id_Client
        JOIN Chambre ch ON r.Id_Chambre = ch.Id_Chambre
        ''')
        reservations = cursor.fetchall()
        return reservations
    except Exception as e:
        st.error(f"Erreur lors de la récupération des réservations: {e}")
        return []

# Fonction pour consulter la liste des clients
def consulter_clients():
    try:
        cursor.execute('SELECT Id_Client, Nom_complet, Email, Telephone FROM Client')
        clients = cursor.fetchall()
        return clients
    except Exception as e:
        st.error(f"Erreur lors de la récupération des clients: {e}")
        return []

# Fonction pour consulter la liste des chambres disponibles pendant une période donnée
def consulter_chambres_disponibles(date_arrivee, date_depart):
    try:
        # Convertir les dates en format texte pour SQL
        date_arrivee_str = date_arrivee.strftime("%Y-%m-%d")
        date_depart_str = date_depart.strftime("%Y-%m-%d")
        
        cursor.execute('''
        SELECT c.Id_Chambre, c.Numero, c.Etage, 
               t.Type, t.Tarif
        FROM Chambre c
        JOIN Type_Chambre t ON c.Id_Type = t.Id_Type
        WHERE c.Id_Chambre NOT IN (
            SELECT r.Id_Chambre
            FROM Reservation r
            WHERE NOT (r.Date_depart <= ? OR r.Date_arrivee >= ?)
        )
        ''', (date_arrivee_str, date_depart_str))
        chambres = cursor.fetchall()
        return chambres
    except Exception as e:
        st.error(f"Erreur lors de la récupération des chambres disponibles: {e}")
        return []

# Fonction pour ajouter un client
def ajouter_client(adresse, ville, code_postal, email, telephone, nom_complet):
    try:
        cursor.execute('''
        INSERT INTO Client (Adresse, Ville, Code_postal, Email, Telephone, Nom_complet)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (adresse, ville, str(code_postal), email, telephone, nom_complet))
        conn.commit()
        st.success('Client ajouté avec succès')
    except Exception as e:
        st.error(f"Erreur lors de l'ajout du client: {e}")

# Fonction pour ajouter une réservation
def ajouter_reservation(date_arrivee, date_depart, id_client, id_chambre):
    try:
        # Convertir les dates en format texte pour SQL
        date_arrivee_str = date_arrivee.strftime("%Y-%m-%d")
        date_depart_str = date_depart.strftime("%Y-%m-%d")
        
        cursor.execute('''
        INSERT INTO Reservation (Date_arrivee, Date_depart, Id_Client, Id_Chambre)
        VALUES (?, ?, ?, ?)
        ''', (date_arrivee_str, date_depart_str, id_client, id_chambre))
        conn.commit()
        st.success('Réservation ajoutée avec succès')
    except Exception as e:
        st.error(f"Erreur lors de l'ajout de la réservation: {e}")

# Interface Streamlit
st.title('Gestion des Réservations d\'Hôtel')

# Section 1: Liste des réservations
st.header('Liste des Réservations')
reservations = consulter_reservations()
if reservations:
    st.table(reservations)
else:
    st.info("Aucune réservation trouvée")

# Section 2: Liste des clients
st.header('Liste des Clients')
clients = consulter_clients()
if clients:
    st.table(clients)
else:
    st.info("Aucun client trouvé")

# Section 3: Chambres disponibles
st.header('Recherche de Chambres Disponibles')
col1, col2 = st.columns(2)
with col1:
    date_arrivee = st.date_input('Date d\'arrivée')
with col2:
    date_depart = st.date_input('Date de départ')

if st.button('Rechercher les chambres disponibles'):
    if date_arrivee >= date_depart:
        st.error("La date de départ doit être après la date d'arrivée")
    else:
        chambres = consulter_chambres_disponibles(date_arrivee, date_depart)
        if chambres:
            st.table(chambres)
        else:
            st.info("Aucune chambre disponible pour cette période")

# Section 4: Ajout d'un nouveau client
st.header('Ajouter un Nouveau Client')
with st.form("client_form"):
    adresse = st.text_input('Adresse')
    ville = st.text_input('Ville')
    code_postal = st.text_input('Code postal', max_chars=5)
    email = st.text_input('Email')
    telephone = st.text_input('Téléphone', max_chars=10)
    nom_complet = st.text_input('Nom complet')
    
    submitted = st.form_submit_button('Ajouter Client')
    if submitted:
        if not all([adresse, ville, code_postal, email, telephone, nom_complet]):
            st.error("Tous les champs sont obligatoires")
        else:
            ajouter_client(adresse, ville, code_postal, email, telephone, nom_complet)

# Section 5: Ajout d'une nouvelle réservation
st.header('Ajouter une Nouvelle Réservation')
with st.form("reservation_form"):
    col1, col2 = st.columns(2)
    with col1:
        date_arrivee_res = st.date_input('Date d\'arrivée')
    with col2:
        date_depart_res = st.date_input('Date de départ')
    
    id_client_res = st.number_input('ID du Client', min_value=1, step=1)
    id_chambre_res = st.number_input('ID de la Chambre', min_value=1, step=1)
    
    submitted = st.form_submit_button('Ajouter Réservation')
    if submitted:
        if date_arrivee_res >= date_depart_res:
            st.error("La date de départ doit être après la date d'arrivée")
        else:
            ajouter_reservation(date_arrivee_res, date_depart_res, id_client_res, id_chambre_res)

# Fermeture de la connexion (ne sera jamais atteint dans Streamlit)
# conn.close()

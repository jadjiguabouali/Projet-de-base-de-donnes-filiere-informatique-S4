import sqlite3

# Connexion à la base de données (création si elle n'existe pas)
conn = sqlite3.connect('hotel.db')
cursor = conn.cursor()

# Suppression des tables existantes pour recréer une base propre
cursor.execute('DROP TABLE IF EXISTS Evaluation')
cursor.execute('DROP TABLE IF EXISTS Reservation')
cursor.execute('DROP TABLE IF EXISTS Chambre')
cursor.execute('DROP TABLE IF EXISTS Type_Chambre')
cursor.execute('DROP TABLE IF EXISTS Prestation')
cursor.execute('DROP TABLE IF EXISTS Client')
cursor.execute('DROP TABLE IF EXISTS Hotel')

# Création des tables avec les corrections
cursor.execute('''
CREATE TABLE Hotel (
    Id_Hotel INTEGER PRIMARY KEY,
    Ville TEXT,
    Pays TEXT,
    Code_postal TEXT  -- Changement de type pour conserver les zéros initiaux
)
''')

cursor.execute('''
CREATE TABLE Client (
    Id_Client INTEGER PRIMARY KEY,
    Adresse TEXT,
    Ville TEXT,
    Code_postal TEXT,  -- Changement de type
    Email TEXT,
    Telephone TEXT,
    Nom_complet TEXT
)
''')

cursor.execute('''
CREATE TABLE Prestation (
    Id_Prestation INTEGER PRIMARY KEY,
    Prix REAL,
    Description TEXT
)
''')

cursor.execute('''
CREATE TABLE Type_Chambre (
    Id_Type INTEGER PRIMARY KEY,
    Type TEXT,
    Tarif REAL
)
''')

cursor.execute('''
CREATE TABLE Chambre (
    Id_Chambre INTEGER PRIMARY KEY,
    Numero INTEGER,    -- Colonne ajoutée (numéro de chambre)
    Etage INTEGER,
    Fumeurs INTEGER,
    Id_Hotel INTEGER,
    Id_Type INTEGER,
    FOREIGN KEY (Id_Hotel) REFERENCES Hotel(Id_Hotel),
    FOREIGN KEY (Id_Type) REFERENCES Type_Chambre(Id_Type)
)
''')

cursor.execute('''
CREATE TABLE Reservation (
    Id_Reservation INTEGER PRIMARY KEY,
    Date_arrivee TEXT,
    Date_depart TEXT,
    Id_Client INTEGER,
    Id_Chambre INTEGER,
    FOREIGN KEY (Id_Client) REFERENCES Client(Id_Client),
    FOREIGN KEY (Id_Chambre) REFERENCES Chambre(Id_Chambre)
)
''')

cursor.execute('''
CREATE TABLE Evaluation (
    Id_Evaluation INTEGER PRIMARY KEY,
    Date_evaluation TEXT,  -- Nom corrigé (était Date_arrivee)
    Note INTEGER,
    Texte_descriptif TEXT,
    Id_Client INTEGER,
    FOREIGN KEY (Id_Client) REFERENCES Client(Id_Client)
)
''')

# Insertion des données avec corrections
hotels = [
    (1, 'Paris', 'France', '75001'),
    (2, 'Lyon', 'France', '69002')
]

clients = [
    (1, '12 Rue de Paris', 'Paris', '75001', 'jean.dupont@email.fr', '0612345678', 'Jean Dupont'),
    (2, '5 Avenue Victor Hugo', 'Lyon', '69002', 'marie.leroy@email.fr', '0623456789', 'Marie Leroy'),
    (3, '8 Boulevard Saint-Michel', 'Marseille', '13005', 'paul.moreau@email.fr', '0634567890', 'Paul Moreau'),
    (4, '27 Rue Nationale', 'Lille', '59800', 'lucie.martin@email.fr', '0645678901', 'Lucie Martin'),
    (5, '3 Rue des Fleurs', 'Nice', '06000', 'emma.giraud@email.fr', '0656789012', 'Emma Giraud')  # Code postal corrigé
]

prestations = [
    (1, 15.0, 'Petit-déjeuner'),
    (2, 30.0, 'Navette aéroport'),
    (3, 0.0, 'Wi-Fi gratuit'),
    (4, 50.0, 'Spa et bien-être'),
    (5, 20.0, 'Parking sécurisé')
]

type_chambres = [
    (1, 'Simple', 80.0),
    (2, 'Double', 120.0)
]

chambres = [
    (1, 201, 2, 0, 1, 1),
    (2, 502, 5, 1, 1, 2),
    (3, 305, 3, 0, 2, 1),
    (4, 410, 4, 0, 2, 2),
    (5, 104, 1, 1, 2, 2),
    (6, 202, 2, 0, 1, 1),
    (7, 307, 3, 1, 1, 2),
    (8, 101, 1, 0, 1, 1)
]

reservations = [
    (1, '2025-06-15', '2025-06-18', 1, 1),
    (2, '2025-07-01', '2025-07-05', 2, 2),
    (3, '2025-11-12', '2025-11-14', 2, 7),
    (4, '2026-02-01', '2026-02-05', 2, 5),  # Chambre corrigée (10 → 5)
    (5, '2025-08-10', '2025-08-14', 3, 3),
    (6, '2025-09-05', '2025-09-07', 4, 4),
    (7, '2026-01-15', '2026-01-18', 4, 6),  # Chambre corrigée (9 → 6)
    (8, '2025-09-20', '2025-09-25', 5, 5)
]

evaluations = [
    (1, '2025-06-15', 5, 'Excellent séjour, personnel très accueillant.', 1),
    (2, '2025-07-01', 4, 'Chambre propre, bon rapport qualité/prix.', 2),
    (3, '2025-08-10', 3, 'Séjour correct mais bruyant la nuit.', 3),
    (4, '2025-09-05', 5, 'Service impeccable, je recommande.', 4),
    (5, '2025-09-20', 4, 'Très bon petit-déjeuner, hôtel bien situé.', 5)
]

cursor.executemany('INSERT INTO Hotel VALUES (?, ?, ?, ?)', hotels)
cursor.executemany('INSERT INTO Client VALUES (?, ?, ?, ?, ?, ?, ?)', clients)
cursor.executemany('INSERT INTO Prestation VALUES (?, ?, ?)', prestations)
cursor.executemany('INSERT INTO Type_Chambre VALUES (?, ?, ?)', type_chambres)
cursor.executemany('INSERT INTO Chambre VALUES (?, ?, ?, ?, ?, ?)', chambres)
cursor.executemany('INSERT INTO Reservation VALUES (?, ?, ?, ?, ?)', reservations)
cursor.executemany('INSERT INTO Evaluation VALUES (?, ?, ?, ?, ?)', evaluations)

# Validation des changements
conn.commit()

# Vérification des données
print("Vérification des données insérées:")
for table in ['Hotel', 'Client', 'Prestation', 'Type_Chambre', 'Chambre', 'Reservation', 'Evaluation']:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"- {table}: {count} lignes")

# Fermeture de la connexion
conn.close()

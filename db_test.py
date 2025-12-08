import mysql.connector
from mysql.connector import Error
from getpass import getpass
import hashlib
import bcrypt

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db"
        )
        return connection
    except Error as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return None

def list_users(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, username, created_at, is_active FROM users")
        users = cursor.fetchall()
        
        if not users:
            print("Aucun utilisateur trouvé.")
            return
            
        print("\nListe des utilisateurs:")
        print("-" * 60)
        print(f"{'ID':<5} | {'Nom d\'utilisateur':<20} | {'Date de création':<20} | {'Statut'}")
        print("-" * 60)
        for user in users:
            status = "Actif" if user[3] else "Inactif"
            print(f"{user[0]:<5} | {user[1]:<20} | {str(user[2]):<20} | {status}")
        print("-" * 60)
        
    except Error as e:
        print(f"Erreur lors de la récupération des utilisateurs: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()

def add_user(connection):
    try:
        username = input("Nouveau nom d'utilisateur: ")
        password = getpass("Nouveau mot de passe: ")
        
        # Hachage du mot de passe avec bcrypt
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, hashed.decode('utf-8'))
        )
        connection.commit()
        print("Utilisateur ajouté avec succès!")
        
    except Error as e:
        print(f"Erreur lors de l'ajout de l'utilisateur: {e}")
        connection.rollback()
    finally:
        if 'cursor' in locals():
            cursor.close()

def main():
    print("=== Gestion simple d'utilisateurs ===\n")
    
    # Connexion à la base de données
    connection = connect_to_db()
    if not connection:
        return
    
    try:
        while True:
            print("\nOptions:")
            print("1. Lister les utilisateurs")
            print("2. Ajouter un utilisateur")
            print("3. Quitter")
            
            choice = input("\nVotre choix (1-3): ")
            
            if choice == '1':
                list_users(connection)
            elif choice == '2':
                add_user(connection)
            elif choice == '3':
                print("Au revoir!")
                break
            else:
                print("Option non valide. Veuillez réessayer.")
                
    finally:
        if connection.is_connected():
            connection.close()
            print("Connexion à la base de données fermée.")

if __name__ == "__main__":
    main()

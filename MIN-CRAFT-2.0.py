from mcrcon import MCRcon
import speech_recognition as sr

# Configuration RCON
RCON_HOST = "127.0.0.1"  # Adresse du serveur (localhost)
RCON_PORT = 25575        # Le port RCON (doit correspondre à celui dans server.properties)
RCON_PASSWORD = "root"   # Le mot de passe défini dans server.properties

# Configuration du micro
recognizer = sr.Recognizer()

def get_words_with_e(phrase):
    """Retourne les mots contenant la lettre 'E'."""
    return [word for word in phrase.split() if "e" in word.lower()]  # Insensible à la casse

def send_to_server(command):
    """Envoie une commande à la console du serveur Minecraft via RCON."""
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            print(f"Commande envoyée : {command}")  # Afficher la commande avant l'exécution
            response = mcr.command(command)
            print(f"Réponse du serveur : {response}")
    except Exception as e:
        print(f"Erreur RCON : {e}")

def select_language():
    """Permet à l'utilisateur de choisir la langue de reconnaissance vocale."""
    languages = {
        "1": ("fr-FR", "Français"),
        "2": ("en-US", "Anglais"),
        "3": ("es-ES", "Espagnol"),
        "4": ("de-DE", "Allemand")
    }
    print("Choisissez une langue pour la reconnaissance vocale :")
    for key, (code, name) in languages.items():
        print(f"{key}. {name}")
    choice = input("Entrez le numéro de la langue : ")
    if choice in languages:
        print(f"Langue sélectionnée : {languages[choice][1]}")
        return languages[choice][0]
    else:
        print("Choix invalide, la langue par défaut sera le Français (fr-FR).")
        return "fr-FR"

def main():
    """Boucle principale d'écoute et d'interaction avec Minecraft."""
    language = select_language()  # Demander la langue au démarrage

    while True:
        try:
            with sr.Microphone() as source:
                print("Parlez maintenant...")
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio, language=language)
                print(f"Vous avez dit : {text}")  # Affiche la transcription complète

                # Extraire les mots contenant "E"
                words_with_e = get_words_with_e(text)
                if not words_with_e:
                    print("Aucun mot avec 'E' détecté.")
                for word in words_with_e:
                    # Vérification du format de la commande
                    title_command = f'title @a title {{ "text": "{word}", "color": "red" }}'
                    sond_command = "playsound minecraft:entity.dragon_fireball.explode ambient @a"
                    effect_cmd = "effect give @p minecraft:blindness 1 255 true"
                    spam_one = "execute at @p run summon tnt ~ ~ ~ {Fuse:5} "
                    print(f"Commande title : {title_command}")  # Afficher la commande avant de l'envoyer

                    send_to_server(title_command)
                    send_to_server(sond_command)
                    send_to_server(effect_cmd)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    send_to_server(spam_one)
                    
                    
                    print(f"Commandes exécutées pour le mot : {word}")
        except sr.UnknownValueError:
            print("Audio incompréhensible.")
        except sr.RequestError as e:
            print(f"Erreur du service de reconnaissance vocale : {e}")
        except KeyboardInterrupt:
            print("Arrêt du script.")
            break

if __name__ == "__main__":
    main()

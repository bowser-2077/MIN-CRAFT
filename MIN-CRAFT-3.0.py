import subprocess
import sys
from mcrcon import MCRcon
import speech_recognition as sr
import random
from colorama import init, Fore
import time
from tqdm import tqdm

# Initialisation de colorama
init(autoreset=True)

# Liste des dépendances à installer
dependencies = ['mcrcon', 'speechrecognition', 'colorama', 'tqdm']

# Configuration RCON
RCON_HOST = "127.0.0.1"
RCON_PORT = 25575
RCON_PASSWORD = "root"

recognizer = sr.Recognizer()

# Liste des sons Minecraft à jouer aléatoirement
sounds = [
    "minecraft:music.game",
    "minecraft:entity.player.levelup",
    "minecraft:entity.wither.death",
    "minecraft:entity.lightning_bolt.impact",
    "minecraft:entity.ender_dragon.death",
    "minecraft:entity.zombie.death",
    "minecraft:entity.skeleton.death",
    "minecraft:entity.creeper.primed",
    "minecraft:entity.bat.death",
]

def get_words_with_e(phrase):
    return [word for word in phrase.split() if "e" in word.lower()]

def send_to_server(command):
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            print(Fore.GREEN + f"Commande envoyée : {command}")
            response = mcr.command(command)
            print(Fore.YELLOW + f"Réponse du serveur : {response}")
    except Exception as e:
        print(Fore.RED + f"Erreur RCON : {e}")

def select_language():
    languages = {
        "1": ("fr-FR", "Français"),
        "2": ("en-US", "Anglais"),
        "3": ("es-ES", "Espagnol"),
        "4": ("de-DE", "Allemand")
    }
    print(Fore.CYAN + "Choisissez une langue pour la reconnaissance vocale :")
    for key, (code, name) in languages.items():
        print(f"{key}. {name}")
    choice = input("Entrez le numéro de la langue : ")
    return languages.get(choice, ("fr-FR", "Français"))[0]

def play_death_sound():
    sound = random.choice(sounds)
    command = f"playsound {sound} @a"
    send_to_server(command)
    print(Fore.MAGENTA + f"Jouer le son: {sound}")

def install_dependencies():
    """Installe les dépendances via pip en arrière-plan avec une barre de progression."""
    for dep in tqdm(dependencies, desc="Téléchargement des dépendances", ncols=100):
        try:
            # Exécution de la commande pip install pour chaque dépendance, sans afficher la sortie
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(0.5)  # Temps de pause pour mieux visualiser la barre de progression
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'installation de {dep}: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Une erreur est survenue : {e}")
            sys.exit(1)

def main():
    # Installer les dépendances avant de commencer le programme principal
    print("Lancement du téléchargement des dépendances...\n")
    install_dependencies()
    print("\nToutes les dépendances ont été installées avec succès !")

    # Commencer le programme principal après l'installation des dépendances
    language = select_language()
    
    with sr.Microphone() as source:
        print(Fore.CYAN + "Calibrating microphone... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=5)
        print(Fore.CYAN + "Microphone calibrated. You can speak now.")

        while True:
            try:
                print(Fore.YELLOW + "Parlez maintenant...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                text = recognizer.recognize_google(audio, language=language)
                print(Fore.WHITE + f"Vous avez dit : {text}")
                
                words_with_e = get_words_with_e(text)
                if not words_with_e:
                    print(Fore.RED + "Aucun mot avec 'E' détecté.")
                    continue

                for word in words_with_e:
                    title_command = f'title @a title {{ "text": "{word}", "color": "red" }}'
                    spam_command = "execute at @p run summon tnt ~ ~ ~ {Fuse:5}"
                    
                    send_to_server(title_command)
                    for _ in range(5):  # Limité à 5 répétitions pour éviter un spam excessif
                        send_to_server(spam_command)
                    
                    print(Fore.GREEN + f"Commandes exécutées pour le mot : {word}")
                    
                    # Play random death sound
                    play_death_sound()

            except sr.UnknownValueError:
                print(Fore.RED + "Audio incompréhensible.")
            except sr.RequestError as e:
                print(Fore.RED + f"Erreur du service de reconnaissance vocale : {e}")
            except sr.WaitTimeoutError:
                print(Fore.RED + "Aucun son détecté. Réessayez.")
            except KeyboardInterrupt:
                print(Fore.RED + "Arrêt du script.")
                break

if __name__ == "__main__":
    main()

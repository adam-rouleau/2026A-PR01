# ======================== game.py ========================

import pygame
import random
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, JUMP_VELOCITY, SPRING_JUMP_VELOCITY,
    DOODLE_SPEED, DOODLE_WIDTH, DOODLE_HEIGHT, PLATFORM_WIDTH, PLATFORM_HEIGHT,
    MIN_PLATFORM_GAP, MAX_PLATFORM_GAP, CAMERA_SCROLL_THRESHOLD,
    PLATFORMS, doodle_dict, DOODLE_START_X, DOODLE_START_Y, LIVES
)
from platforms import create_platform, choose_platform_type
from doodle import doodle_left_img, doodle_right_img
from window import generate_initial_platforms


# ======================== PARTIE 3.1 ========================
def apply_gravity():
    """
    Applique la gravité au Doodle en augmentant progressivement sa vitesse verticale (vel_y).
    Met à jour la position verticale (y) du Doodle.
    """
    # TODO : Mettez à jour la vitesse verticale puis la position verticale
    # du Doodle à partir de GRAVITY.
    doodle_dict["vel_y"] += GRAVITY
    doodle_dict["y"] += doodle_dict["vel_y"]

    return

# ===========================================================


# ======================== PARTIE 1.2 ========================
def move_doodle():
    """
    Gère le déplacement horizontal du Doodle selon les touches pressées (Flèches ou A/D).
    Implémente le passage fluide d'un côté de l'écran à l'autre (Screen Wrap).
    """
    keys = pygame.key.get_pressed()

    # TODO : Gérez les déplacements gauche/droite et mettez à jour
    # simultanément la direction et l'image du Doodle.
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        doodle_dict["direction"] = "left"
        doodle_dict["image"] = doodle_left_img
        doodle_dict["x"] -= DOODLE_SPEED
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        doodle_dict["direction"] = "right"
        doodle_dict["image"] = doodle_right_img
        doodle_dict["x"] += DOODLE_SPEED

    # TODO : Implémentez le Screen Wrap pour qu'une partie du Doodle puisse
    # sortir d'un côté avant de réapparaître de l'autre.
    # N'utilisez pas de dimensions numériques écrites directement.

    position_doodle_x = doodle_dict["x"]
    position_bord_droit = SCREEN_WIDTH
    position_maximale_gauche = - (DOODLE_WIDTH/2)
    position_maximale_droite = position_bord_droit - (DOODLE_WIDTH/2)
    if position_doodle_x <= position_maximale_gauche:
        doodle_dict["x"] = position_maximale_droite
    elif position_doodle_x >= position_maximale_droite:
        doodle_dict["x"] = position_maximale_gauche

    return

# ===========================================================


# ======================== PARTIE 2.3 ========================
def move_platforms():
    """
    Déplace horizontalement les plateformes mobiles ("blue").
    Fait rebondir les plateformes lorsqu'elles atteignent les bords de la fenêtre.
    """
    # TODO : Parcourez les plateformes et gérez le déplacement des plateformes
    # bleues encore actives. Elles doivent rester dans la fenêtre en inversant
    # leur vitesse lorsqu'elles atteignent un bord.
    
    for platform in PLATFORMS: 
        position_plateform_x = platform["x"]
        position_bord_droit = SCREEN_WIDTH
        position_maximale_droite = position_bord_droit - platform["width"]
        if platform["type"] == "blue":
            platform["x"] += platform["vx"]
            if platform["x"] <= 0:
                platform["vx"] -= 2*platform["vx"]
            if platform["x"] >= position_maximale_droite:
                platform["vx"] -= 2*platform["vx"]
             


    return

# ===========================================================


# ======================== PARTIE 3.2 ========================
def check_platform_collisions():
    """
    Détecte si le Doodle atterrit sur une plateforme.
    Le rebond ne se produit QUE lorsque le Doodle descend (vel_y > 0)
    et qu'il arrive sur le dessus d'une plateforme.
    """
    # TODO : Implémentez la détection d'un atterrissage.
    #
    # Contraintes :
    # - aucun rebond pendant la montée ;
    # - ignorer les plateformes inactives ;
    # - utiliser rects_collide(...) pour le chevauchement des rectangles ;
    # - un simple chevauchement ne suffit pas : le Doodle doit arriver par
    #   le dessus de la plateforme. Pour le vérifier, comparez la position
    #   actuelle de ses pieds à leur position approximative à l'image
    #   précédente à l'aide de vel_y. Une tolérance de 14 pixels est permise ;
    # - spring : SPRING_JUMP_VELOCITY ;
    # - brown : JUMP_VELOCITY puis désactivation de la plateforme ;
    # - green/blue : JUMP_VELOCITY.
    vel_y = doodle_dict["vel_y"]
    doodle_x = doodle_dict["x"]
    doodle_y = doodle_dict["y"]

    rect_doodle = (doodle_x, doodle_y, DOODLE_WIDTH, DOODLE_HEIGHT)
    rect_doodle_before = rect_doodle # S'assurer que le premier coup ai une valeur
    #Si descente
    if vel_y > 0:
        for platform in range(len(PLATFORMS)):
            # platform_hitbox = {
            #     "gauche_x" : PLATFORMS[plateform]["x"], 
            #     "droite_x" : (PLATFORMS[plateform]["x"] + PLATFORM_WIDTH), 
            #     "haut_y" : PLATFORMS[plateform]["y"], 
            #     "bas_y" : (PLATFORMS["y"] + PLATFORM_HEIGHT),
            # }
            platform_x = PLATFORMS[platform]["x"]
            platform_y = PLATFORMS[platform]["y"]
            rect_platform = (platform_x, platform_y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
            if rects_collide(rect_doodle, rect_platform):
                if rects_collide(rect_doodle_before, rect_platform):
                    if PLATFORMS[platform]["type"] == "green" or PLATFORMS[platform]["type"] == "blue":
                        doodle_dict["vel_y"] = JUMP_VELOCITY
                    elif PLATFORMS[platform]["type"] == "spring":
                        doodle_dict["vel_y"] = SPRING_JUMP_VELOCITY
                    elif PLATFORMS[platform]["type"] == "brown":
                        doodle_dict["vel_y"] = JUMP_VELOCITY
                        PLATFORMS[platform]["active"] == False
                rect_doodle_before = (doodle_x, (doodle_y + vel_y), PLATFORM_WIDTH, PLATFORM_HEIGHT)


    return

# ===========================================================


# ======================== PARTIE 3.3 ========================
def scroll_camera():
    """
    Fait défiler le monde lorsque le Doodle dépasse CAMERA_SCROLL_THRESHOLD.
    Met à jour le score et maintient les plateformes visibles.
    """
    # TODO : Lorsque le Doodle dépasse le seuil de caméra, il doit rester
    # visuellement au seuil pendant que les plateformes sont déplacées vers
    # le bas de la même distance.
    #
    # Le score doit représenter la distance verticale ainsi parcourue et le
    # meilleur score doit être mis à jour. Les plateformes sorties sous
    # l'écran doivent être retirées, puis de nouvelles plateformes générées.
    doodle_y = doodle_dict["y"]
    if doodle_y <= CAMERA_SCROLL_THRESHOLD:
        print("Over", doodle_y)
        doodle_dict["y"] = CAMERA_SCROLL_THRESHOLD
        vitesse_deplacement_y = doodle_dict["vel_y"]
        print(vitesse_deplacement_y)
        for platform in range(len(PLATFORMS)):
            PLATFORMS[platform]["y"] -= vitesse_deplacement_y
        doodle_dict["score"] += vitesse_deplacement_y
        if doodle_dict["score"] > doodle_dict["high_score"]:
            doodle_dict["high_score"] = doodle_dict["score"]
        for platform in range(len(PLATFORMS)):
            if PLATFORMS[platform]["y"] >= SCREEN_HEIGHT:
                PLATFORMS[platform]["active"]
                generate_new_platforms()

    return

# ===========================================================


# ======================== PARTIE 3.4 ========================
def generate_new_platforms():
    """
    Génère de nouvelles plateformes au-dessus du haut de l'écran pour maintenir
    un flux continu lorsque la caméra défile.
    """
    # TODO : Complétez cette fonction en vous inspirant de la logique de
    # génération initiale, sans la recopier inutilement.
    #
    # Vous devrez partir de la plateforme actuellement la plus haute et
    # continuer à ajouter des plateformes tant que nécessaire. Utilisez
    # choose_platform_type(...) avec les probabilités indiquées dans le README.
    plateforme_plus_haute = PLATFORMS[-1]
    while (plateforme_plus_haute["y"] - MAX_PLATFORM_GAP) > 0:
        position_x = random.randint(0, (SCREEN_WIDTH-PLATFORM_WIDTH))
        position_y = plateforme_plus_haute["y"] - (random.randint(MIN_PLATFORM_GAP, MAX_PLATFORM_GAP))
        platform_type = choose_platform_type(0.55, 0.20, 13.0)
        create_platform(position_x, position_y, platform_type)


    return

# ===========================================================


def check_game_over():
    """
    Vérifie si le Doodle tombe sous le bas de l'écran.
    Si oui, réduit les vies.
    Retourne True si la partie est terminée.
    """
    if doodle_dict["y"] > SCREEN_HEIGHT:
        doodle_dict["lives"] -= 1
        return True
    return False


def restart_game():
    """
    Réinitialise la partie : position du Doodle, vitesse, score et plateformes.
    """
    doodle_dict["x"] = DOODLE_START_X
    doodle_dict["y"] = DOODLE_START_Y
    doodle_dict["vel_y"] = 0.0
    doodle_dict["direction"] = "right"
    doodle_dict["image"] = doodle_right_img
    doodle_dict["score"] = 0
    doodle_dict["lives"] = LIVES

    generate_initial_platforms()


def rects_collide(r1, r2):
    """
    Vérifie si deux rectangles (x, y, largeur, hauteur) se chevauchent.
    Cette fonction est fournie et ne doit pas être modifiée.
    """
    return not (
        r1[0] + r1[2] <= r2[0] or r1[0] >= r2[0] + r2[2] or
        r1[1] + r1[3] <= r2[1] or r1[1] >= r2[1] + r2[3]
    )

generate_initial_platforms
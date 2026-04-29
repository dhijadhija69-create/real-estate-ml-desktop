"""
ui/main_window.py - Main Prediction Interface with Profile + Chatbot (FAQ-based, Enhanced)
"""

import os, sys, unicodedata
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QComboBox, QCheckBox, QPushButton,
    QScrollArea, QMessageBox, QFrame, QTextEdit, QSizePolicy,
    QStackedWidget, QApplication
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QSize
from PyQt6.QtGui  import QFont, QColor


VILLES = [
    "Casablanca", "Rabat", "Marrakech", "Fès", "Tanger",
    "Agadir", "Meknès", "Oujda", "Kenitra", "Tétouan",
    "Salé", "Mohammedia", "El Jadida", "Nador", "Béni Mellal"
]

KITCHEN_MAP = {"Basic": 0, "Modern": 1, "Luxury": 2}


# ══════════════════════════════════════════════════════════════════════════════
#  INTELLIGENT CHATBOT ENGINE  (100% offline)
# ══════════════════════════════════════════════════════════════════════════════

def _normalize(text: str) -> str:
    """Lowercase + strip accents so 'Étage' matches 'etage'."""
    nfkd = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in nfkd if not unicodedata.combining(c))


# ── Synonym map ───────────────────────────────────────────────────────────────
# Each key is a canonical topic; values are words/phrases that map to it.
SYNONYMS: dict[str, list[str]] = {
    "bonjour":       ["bonjour", "salam", "salut", "hello", "bonsoir", "hi", "hey", "coucou"],
    "merci":         ["merci", "thanks", "thank you", "shukran", "parfait", "super", "nickel", "top"],
    "au_revoir":     ["au revoir", "bye", "a bientot", "ciao", "bonne journee", "bonne soiree"],
    "prediction":    ["prediction", "predire", "estimer", "estimation", "calculer", "prix predit",
                      "comment ca marche", "comment fonctionne", "comment utiliser",
                      "comment predire", "comment obtenir prix"],
    "fiabilite":     ["fiable", "fiabilite", "precis", "precision", "exact", "juste",
                      "marge erreur", "confiance", "taux erreur", "c est fiable"],
    "prix_change":   ["pourquoi prix change", "prix different", "prix varie", "variation prix",
                      "pas le meme prix", "prix incorrect", "prix bizarre"],
    "surface":       ["surface", "superficie", "m2", "metres carres", "taille", "grand", "petit",
                      "surface habitable", "combien de m2"],
    "chambres":      ["chambre", "chambres", "pieces", "studio", "f1", "f2", "f3", "f4", "f5",
                      "nombre de chambre", "chambre a coucher"],
    "salle_de_bain": ["salle de bain", "sdb", "douche", "wc", "toilette", "sanitaire",
                      "salle d eau", "bain", "lavabo"],
    "cuisine":       ["cuisine", "cuisinier", "basic", "moderne", "modern", "luxe", "luxury",
                      "type cuisine", "cuisine equipee", "open space"],
    "etage":         ["etage", "niveau", "rez de chaussee", "rdc", "dernier etage",
                      "combien etage", "hauteur"],
    "annee":         ["annee", "construction", "age", "vieux", "recent", "neuf", "nouveau",
                      "date construction", "quand construit", "ancien"],
    "localisation":  ["localisation", "emplacement", "adresse", "situation", "position",
                      "lieu", "endroit", "zone"],
    "quartier":      ["quartier", "neighbourhood", "secteur", "coin", "arrondissement",
                      "maarif", "gueliz", "hay riad", "agdal", "anfa", "ain diab"],
    "ville":         ["ville", "city", "casablanca", "rabat", "marrakech", "fes", "tanger",
                      "agadir", "meknes", "oujda", "kenitra", "tetouan", "maroc"],
    "piscine":       ["piscine", "pool", "swimming", "bain exterieur"],
    "garage":        ["garage", "box voiture", "abri voiture"],
    "balcon":        ["balcon", "loggia", "terrasse couverte"],
    "terrasse":      ["terrasse", "rooftop", "toit terrasse", "toiture"],
    "ascenseur":     ["ascenseur", "elevator", "lift", "monte charge"],
    "jardin":        ["jardin", "espace vert", "pelouse", "verdure", "exterieur"],
    "parking":       ["parking", "stationnement", "place voiture", "garer"],
    "vue":           ["vue", "panorama", "belle vue", "mer", "ocean", "montagne", "paysage"],
    "marche":        ["marche", "marche immobilier", "tendance", "evolution", "hausse", "baisse",
                      "conjoncture", "secteur immobilier"],
    "investir":      ["investir", "investissement", "rentabilite", "rendement", "achat locatif",
                      "placement immobilier", "bon investissement", "vaut la peine"],
    "acheter":       ["acheter", "achat", "acquisition", "comment acheter", "conseils achat",
                      "premier achat", "primo accedant"],
    "louer":         ["louer", "location", "bail", "loyer", "locataire", "proprietaire",
                      "location longue duree", "location courte duree"],
    "notaire":       ["notaire", "frais notaire", "acte de vente", "compromis", "signature",
                      "contrat", "titre foncier", "juridique", "legal"],
    "credit":        ["credit", "pret immobilier", "hypotheque", "financement", "banque",
                      "mensualite", "taux interet", "emprunt", "pret"],
    "darpredict":    ["darpredict", "application", "appli", "outil", "logiciel", "plateforme"],
    "aide":          ["aide", "help", "aidez moi", "besoin aide", "comment faire",
                      "je comprends pas", "je sais pas", "expliquer", "expliquez"],
}

# ── Rich response bank ────────────────────────────────────────────────────────
RESPONSES: dict[str, str] = {

    "bonjour": (
        "Bonjour et bienvenue sur DarPredict ! 👋\n\n"
        "Je suis PreHi, votre assistant immobilier expert. Je suis ici pour vous aider à :\n"
        "• Comprendre comment fonctionne l'estimation de prix\n"
        "• Vous expliquer les critères qui influencent la valeur d'un bien\n"
        "• Vous conseiller sur le marché immobilier marocain\n"
        "• Répondre à toutes vos questions sur l'immobilier\n\n"
        "N'hésitez pas à me poser n'importe quelle question, je suis là pour vous ! 😊"
    ),

    "merci": (
        "Avec plaisir ! 😊 C'est mon rôle de vous aider.\n\n"
        "Si vous avez d'autres questions sur l'immobilier ou sur DarPredict, "
        "n'hésitez surtout pas. Je reste disponible pour vous accompagner "
        "dans votre projet immobilier. 🏠"
    ),

    "au_revoir": (
        "Au revoir et bonne continuation ! 👋\n\n"
        "J'espère avoir pu vous aider dans votre recherche immobilière. "
        "N'oubliez pas de revenir sur DarPredict pour vos futures estimations. "
        "Bonne chance dans votre projet ! 🏡✨"
    ),

    "prediction": (
        "🏠 Comment fonctionne la prédiction de prix ?\n\n"
        "DarPredict utilise un modèle d'intelligence artificielle entraîné sur des milliers "
        "de transactions immobilières réelles au Maroc. Voici les étapes :\n\n"
        "1️⃣ Vous renseignez les caractéristiques du bien (surface, chambres, localisation...)\n"
        "2️⃣ Notre algorithme analyse ces données en les comparant à des biens similaires\n"
        "3️⃣ Il calcule une estimation basée sur les tendances du marché local\n"
        "4️⃣ Vous obtenez un prix estimé en dirhams (DH)\n\n"
        "💡 Conseil : Plus vous renseignez d'informations précises, plus l'estimation "
        "sera fiable. N'oubliez pas de cocher les équipements disponibles (piscine, "
        "garage, ascenseur...) car ils ont un impact significatif sur le prix final."
    ),

    "fiabilite": (
        "📊 Fiabilité des estimations DarPredict\n\n"
        "Notre modèle offre une bonne approximation du prix du marché, "
        "mais quelques points importants :\n\n"
        "✅ Ce que le modèle fait bien :\n"
        "• Capture les tendances générales par ville et quartier\n"
        "• Prend en compte l'impact des équipements (piscine, garage, etc.)\n"
        "• Intègre l'étage, l'année de construction et la surface\n\n"
        "⚠️ Les limites à connaître :\n"
        "• L'état général du bien (rénové ou non) n'est pas toujours mesurable\n"
        "• Des facteurs uniques (vue exceptionnelle, rue précise) peuvent varier\n\n"
        "💡 Recommandation : Utilisez l'estimation comme référence, et consultez "
        "également un agent immobilier local pour affiner votre évaluation."
    ),

    "prix_change": (
        "🔄 Pourquoi le prix change-t-il selon les paramètres ?\n\n"
        "C'est tout à fait normal ! Le prix d'un bien dépend de nombreux facteurs "
        "interdépendants :\n\n"
        "📍 La localisation (facteur n°1) :\n"
        "Un appartement à Casablanca Anfa peut coûter 3 à 4 fois plus qu'un bien "
        "identique dans un quartier périphérique.\n\n"
        "📐 La surface :\n"
        "Chaque m² supplémentaire augmente le prix, mais le prix/m² peut diminuer "
        "pour les très grandes surfaces (effet d'échelle).\n\n"
        "🏗️ L'année de construction :\n"
        "Un bien neuf coûte généralement 20 à 40% plus cher qu'un bien ancien équivalent.\n\n"
        "🛋️ Les équipements :\n"
        "Une piscine peut augmenter la valeur de 5 à 15%, un garage de 3 à 8%."
    ),

    "surface": (
        "📐 L'impact de la surface sur le prix\n\n"
        "La surface habitable est l'un des critères les plus déterminants :\n\n"
        "📊 Relation surface / usage :\n"
        "• Studio (30-50 m²) : idéal pour investissement locatif ou premier achat\n"
        "• Appartement moyen (80-120 m²) : le plus recherché par les familles\n"
        "• Grand appartement (150+ m²) : segment premium, souvent haut de gamme\n\n"
        "💡 À savoir :\n"
        "Le prix au m² diminue pour les grandes surfaces. Un 200 m² n'est pas "
        "forcément 2x plus cher qu'un 100 m² — le prix au m² peut être 10 à 20% "
        "inférieur.\n\n"
        "🔑 Conseil : Renseignez la surface habitable (hors balcons et terrasses) "
        "pour une estimation plus précise."
    ),

    "chambres": (
        "🛏️ L'influence du nombre de chambres\n\n"
        "Le nombre de chambres reflète la capacité d'accueil et cible différents profils :\n\n"
        "🏠 Profils typiques au Maroc :\n"
        "• Studio / F1 : célibataires, jeunes couples, investissement locatif\n"
        "• F2 (1-2 chambres) : jeunes couples, petites familles — très demandé\n"
        "• F3 (2-3 chambres) : familles avec enfants — le plus courant\n"
        "• F4-F5 (4+ chambres) : grandes familles, haut standing\n\n"
        "📈 Impact sur le prix :\n"
        "Chaque chambre supplémentaire peut augmenter la valeur de 5 à 15% "
        "selon la ville. À Casablanca, cela peut représenter 50 000 à 100 000 DH de plus."
    ),

    "salle_de_bain": (
        "🛁 L'impact des salles de bain sur la valeur\n\n"
        "Souvent sous-estimée, la salle de bain est pourtant un critère important :\n\n"
        "✅ Pourquoi c'est important :\n"
        "• Une SDB par chambre est le standard dans le haut standing\n"
        "• Une 2ème salle de bain augmente le confort et l'attractivité à la revente\n"
        "• Les acheteurs avec enfants accordent une grande importance à ce critère\n\n"
        "📊 Impact estimé sur le prix :\n"
        "• 1 SDB : standard pour les F2/F3\n"
        "• 2 SDB : peut augmenter la valeur de 3 à 8%\n"
        "• 3 SDB+ : signe de prestations luxe, impact pouvant dépasser 10%\n\n"
        "💡 Conseil : Une salle de bain bien rénovée peut significativement "
        "valoriser votre bien."
    ),

    "cuisine": (
        "🍳 L'importance du type de cuisine\n\n"
        "La cuisine joue un rôle croissant dans l'estimation des biens :\n\n"
        "🔹 Cuisine Basic :\n"
        "Équipement minimal, fonctionnel. Courante dans les logements économiques.\n\n"
        "🔸 Cuisine Modern :\n"
        "Plan de travail qualitatif, placards intégrés, équipements récents. "
        "Standard actuel du marché. Peut augmenter la valeur de 3 à 7%.\n\n"
        "💎 Cuisine Luxury :\n"
        "Matériaux haut de gamme (marbre, quartz), électroménager encastré de marque. "
        "Impact : +8 à +15% sur la valeur.\n\n"
        "💡 Tendance actuelle : Les cuisines ouvertes (open space) sont très prisées "
        "dans les nouveaux projets et augmentent l'attractivité du bien."
    ),

    "etage": (
        "🏢 L'influence de l'étage sur le prix\n\n"
        "L'étage peut faire varier le prix de manière significative :\n\n"
        "📊 Règle générale au Maroc :\n"
        "• RDC : souvent le moins cher (-5 à -15%), sauf si jardin privatif\n"
        "• 1er au 3ème étage : prix intermédiaire, appréciés des familles\n"
        "• 4ème étage et plus : prime si ascenseur présent (+3 à +10%)\n"
        "• Dernier étage : peut être le plus cher si belle vue et terrasse (+5 à +20%)\n\n"
        "⚠️ Facteur clé — l'ascenseur :\n"
        "Sans ascenseur, un appartement au 5ème étage peut perdre 10 à 15% de sa valeur. "
        "Avec ascenseur, les étages élevés deviennent très attractifs.\n\n"
        "💡 Combinez 'étage' + 'ascenseur' + 'belle vue' pour maximiser l'estimation."
    ),

    "annee": (
        "📅 L'impact de l'année de construction\n\n"
        "L'ancienneté d'un bien est un facteur déterminant dans son évaluation :\n\n"
        "🆕 Bien neuf (moins de 5 ans) :\n"
        "• Prix plus élevé (prime de nouveauté : +15 à +30%)\n"
        "• Garanties constructeur incluses\n"
        "• Normes récentes (isolation, sécurité, électricité)\n"
        "• Souvent exonéré de taxes pendant 5 ans (selon conditions)\n\n"
        "🏚️ Bien ancien (plus de 20 ans) :\n"
        "• Prix inférieur, mais négociable\n"
        "• Peut nécessiter des travaux de rénovation\n"
        "• Souvent situé dans des quartiers bien établis\n\n"
        "📊 Dépréciation moyenne : un bien perd environ 1 à 2% de valeur par an "
        "s'il n'est pas entretenu ou rénové."
    ),

    "localisation": (
        "📍 La localisation : le facteur n°1 en immobilier\n\n"
        "'Location, location, location' — c'est la règle d'or, "
        "et le Maroc ne fait pas exception.\n\n"
        "🗺️ Ce que la localisation englobe :\n"
        "• La ville (Casablanca vs ville secondaire peut tripler les prix)\n"
        "• Le quartier (Anfa vs Hay Mohammadi : rapport de 1 à 5)\n"
        "• La proximité des commodités (écoles, commerces, hôpitaux, transports)\n\n"
        "📊 Exemples de fourchettes de prix au m² au Maroc :\n"
        "• Casablanca premium (Anfa, CIL) : 15 000 à 30 000+ DH/m²\n"
        "• Casablanca standard : 8 000 à 15 000 DH/m²\n"
        "• Marrakech Guéliz/Hivernage : 12 000 à 25 000 DH/m²\n"
        "• Rabat Agdal/Hay Riad : 10 000 à 20 000 DH/m²\n"
        "• Villes secondaires : 4 000 à 10 000 DH/m²"
    ),

    "quartier": (
        "🏘️ L'importance du quartier dans l'estimation\n\n"
        "Au sein d'une même ville, les écarts de prix entre quartiers peuvent être énormes.\n\n"
        "🌟 Critères qui font un bon quartier :\n"
        "• Sécurité et tranquillité\n"
        "• Qualité des infrastructures (routes, éclairage, espaces verts)\n"
        "• Proximité des écoles, universités, centres médicaux\n"
        "• Accès aux transports en commun\n"
        "• Dynamisme commercial (commerces, restaurants)\n\n"
        "📈 Quartiers en hausse au Maroc :\n"
        "• Casablanca : Bouskoura, Californie, Sidi Maarouf\n"
        "• Marrakech : Route de l'Ourika, Targa\n"
        "• Rabat : Yacoub El Mansour, Technopolis\n\n"
        "💡 Renseignez le quartier précis dans le champ correspondant "
        "pour affiner l'estimation."
    ),

    "ville": (
        "🏙️ Les villes immobilières au Maroc\n\n"
        "Chaque ville marocaine a ses spécificités de marché :\n\n"
        "🥇 Casablanca — La capitale économique\n"
        "Le marché le plus cher et le plus dynamique.\n\n"
        "🥈 Rabat — La capitale administrative\n"
        "Marché stable et premium, très prisé des fonctionnaires et diplomates.\n\n"
        "🥉 Marrakech — La ville touristique\n"
        "Fort attrait des investisseurs étrangers.\n\n"
        "🏖️ Agadir — La station balnéaire\n"
        "Dominé par les résidences secondaires et le tourisme.\n\n"
        "🌊 Tanger — La ville du détroit\n"
        "En pleine croissance grâce aux investissements industriels.\n\n"
        "💡 Sélectionnez votre ville dans la liste pour une estimation adaptée "
        "aux prix réels de ce marché local."
    ),

    "piscine": (
        "🏊 La piscine : un équipement premium\n\n"
        "La piscine est l'un des équipements qui valorise le plus un bien :\n\n"
        "📊 Impact sur la valeur :\n"
        "• Villa individuelle avec piscine : +10 à +25%\n"
        "• Appartement en résidence avec piscine commune : +5 à +12%\n"
        "• Penthouse avec piscine privée : +15 à +30%\n\n"
        "🌍 Contexte marocain :\n"
        "Très appréciée à Marrakech, Agadir et dans les résidences haut standing "
        "de Casablanca. Elle attire particulièrement les acheteurs étrangers.\n\n"
        "⚠️ À noter : L'entretien d'une piscine représente un coût annuel "
        "de 5 000 à 20 000 DH selon la taille — à intégrer dans votre budget."
    ),

    "garage": (
        "🚗 Le garage : très recherché en ville\n\n"
        "Dans les grandes villes où le stationnement est difficile, "
        "le garage est devenu un équipement très prisé :\n\n"
        "📊 Impact sur la valeur :\n"
        "• Garage individuel : +3 à +10%\n"
        "• Double garage : +8 à +15%\n"
        "• Box fermé vs parking ouvert : le box fermé est nettement plus valorisé\n\n"
        "🏙️ À Casablanca, un emplacement de parking peut se vendre entre "
        "80 000 et 250 000 DH selon le quartier.\n\n"
        "💡 Si vous hésitez entre deux biens similaires, privilégiez celui avec "
        "garage — c'est un atout majeur à la revente."
    ),

    "balcon": (
        "🌿 Le balcon : un espace extérieur apprécié\n\n"
        "Dans un contexte urbain dense, tout espace extérieur privatif est valorisé :\n\n"
        "📊 Impact sur la valeur :\n"
        "• Petit balcon (< 5 m²) : +1 à +3%\n"
        "• Grand balcon (5-15 m²) : +3 à +6%\n"
        "• Balcon avec belle vue : peut atteindre +8 à +10%\n\n"
        "✅ Avantages du balcon :\n"
        "• Espace de vie supplémentaire (plantes, salon d'extérieur)\n"
        "• Luminosité et ventilation naturelle améliorées\n"
        "• Très recherché post-pandémie\n"
        "• Augmente l'attractivité à la location"
    ),

    "terrasse": (
        "☀️ La terrasse : un atout majeur de valorisation\n\n"
        "La terrasse est l'un des équipements les plus valorisants au Maroc "
        "grâce au climat ensoleillé :\n\n"
        "📊 Impact sur la valeur :\n"
        "• Terrasse standard (15-30 m²) : +5 à +12%\n"
        "• Grande terrasse (30+ m²) : +10 à +20%\n"
        "• Toit-terrasse privatif (penthouse) : +15 à +30%\n\n"
        "🌟 Pourquoi c'est si recherché au Maroc :\n"
        "• Climat ensoleillé (300+ jours de soleil/an)\n"
        "• Culture du plein air et des repas en extérieur\n"
        "• Possibilité d'aménagement (salon de jardin, pergola, barbecue)"
    ),

    "ascenseur": (
        "🛗 L'ascenseur : essentiel pour les étages élevés\n\n"
        "L'impact de l'ascenseur varie fortement selon l'étage :\n\n"
        "📊 Impact sur la valeur selon l'étage :\n"
        "• RDC et 1er étage : ascenseur peu impactant\n"
        "• 2ème-3ème étage : +2 à +5% avec ascenseur\n"
        "• 4ème étage et plus : +5 à +15% avec ascenseur\n"
        "• Sans ascenseur au 5ème étage : décote de -10 à -20%\n\n"
        "👴 Facteur démographique :\n"
        "Avec le vieillissement de la population, l'ascenseur devient de plus en plus "
        "indispensable. C'est un critère de confort qui pèse lourd dans la décision "
        "d'achat des familles.\n\n"
        "⚠️ Vérifiez toujours l'état et l'entretien de l'ascenseur — "
        "un ascenseur défaillant est un point de négociation."
    ),

    "jardin": (
        "🌳 Le jardin : la nature en ville\n\n"
        "Le jardin est un équipement rare et très recherché en milieu urbain :\n\n"
        "📊 Impact sur la valeur :\n"
        "• Jardin commun de résidence : +3 à +7%\n"
        "• Jardin privatif (villa) : +10 à +25% selon surface\n"
        "• Jardin intérieur (riad) : peut doubler la valeur du bien\n\n"
        "🌿 Tendance post-Covid :\n"
        "La demande pour les biens avec espace vert a explosé depuis 2020. "
        "Les Marocains accordent une importance croissante à la qualité de vie.\n\n"
        "💡 Spécificité marocaine : Les riads de Marrakech et Fès avec jardin "
        "intérieur sont parmi les biens les plus valorisés du marché."
    ),

    "parking": (
        "🅿️ Le parking : nécessité urbaine\n\n"
        "Le parking reste un atout considérable dans les zones urbaines :\n\n"
        "📊 Impact sur la valeur :\n"
        "• Place de parking extérieure : +2 à +5%\n"
        "• Parking souterrain sécurisé : +4 à +8%\n"
        "• Double place de parking : +6 à +12%\n\n"
        "🏙️ Contexte marocain :\n"
        "Dans des villes comme Casablanca, Rabat ou Marrakech, "
        "trouver à se garer est devenu un défi quotidien. "
        "Un bien avec parking se loue et se vend plus facilement.\n\n"
        "💡 Dans les nouvelles résidences, le parking est souvent inclus "
        "dans le prix — vérifiez toujours ce point."
    ),

    "vue": (
        "🌅 La belle vue : un luxe qui se monnaye\n\n"
        "Une vue exceptionnelle peut transformer radicalement la valeur d'un bien :\n\n"
        "📊 Impact sur la valeur selon le type de vue :\n"
        "• Vue sur cour ou rue standard : prix de base\n"
        "• Vue dégagée sur ville : +5 à +10%\n"
        "• Vue sur mer ou océan : +10 à +30%\n"
        "• Vue sur montagne (Atlas) : +8 à +20%\n"
        "• Vue sur monument historique : +10 à +25%\n\n"
        "🌊 Cas particulier — Agadir et Tanger :\n"
        "Les appartements avec vue directe sur l'océan peuvent se négocier "
        "50 à 100% plus cher que leurs équivalents sans vue.\n\n"
        "📸 Conseil : La vue est souvent l'argument de vente le plus puissant."
    ),

    "marche": (
        "📈 Le marché immobilier marocain — État des lieux\n\n"
        "Le marché est structuré par plusieurs forces :\n\n"
        "🏗️ Offre et demande :\n"
        "La demande est soutenue par une urbanisation rapide (60%+ de population urbaine), "
        "la croissance démographique et un déficit de logements estimé à 400 000 unités.\n\n"
        "💰 Tendances des prix :\n"
        "• Les prix ont connu une hausse significative depuis 2020\n"
        "• Les grandes villes (Casa, Rabat, Marrakech) restent les plus dynamiques\n"
        "• Le segment du logement social reste en tension permanente\n\n"
        "🏦 Financement :\n"
        "Les taux des crédits immobiliers oscillent entre 4% et 6%, "
        "avec des durées pouvant aller jusqu'à 25 ans.\n\n"
        "🌍 Investisseurs étrangers :\n"
        "Le Maroc attire de nombreux investisseurs (Européens, MRE) "
        "qui contribuent à la hausse des prix dans certains segments."
    ),

    "investir": (
        "💼 Investir dans l'immobilier au Maroc\n\n"
        "L'immobilier reste l'un des placements préférés des Marocains :\n\n"
        "✅ Avantages de l'investissement immobilier :\n"
        "• Valeur refuge contre l'inflation\n"
        "• Revenus locatifs réguliers (rendement brut de 5 à 8%)\n"
        "• Plus-value à la revente sur le long terme\n"
        "• Patrimoine transmissible\n\n"
        "🏆 Meilleures stratégies d'investissement au Maroc :\n"
        "1. Achat-location longue durée : revenus stables, idéal dans les villes universitaires\n"
        "2. Achat-location courte durée (Airbnb) : rendements élevés à Marrakech, Agadir\n"
        "3. Achat sur plan (VEFA) : prix d'achat inférieur, plus-value à la livraison\n"
        "4. Rénovation-revente : acheter ancien à rénover et revendre avec bénéfice\n\n"
        "⚠️ Points de vigilance :\n"
        "• Vérifiez le titre foncier avant tout achat\n"
        "• Calculez les frais annexes (notaire, agence, taxe)\n"
        "• Évaluez la liquidité du marché dans le quartier ciblé"
    ),

    "acheter": (
        "🏡 Guide d'achat immobilier au Maroc\n\n"
        "Acheter est souvent le plus grand investissement d'une vie. "
        "Voici les étapes clés :\n\n"
        "📋 Les étapes de l'achat :\n"
        "1️⃣ Définir votre budget (prix + frais = environ 7 à 10% du prix)\n"
        "2️⃣ Choisir la ville et le quartier selon vos critères\n"
        "3️⃣ Visiter plusieurs biens et comparer\n"
        "4️⃣ Utiliser DarPredict pour valider le prix demandé\n"
        "5️⃣ Négocier le prix (5 à 15% de marge est fréquent)\n"
        "6️⃣ Signer le compromis de vente\n"
        "7️⃣ Finaliser le financement (si crédit)\n"
        "8️⃣ Passer devant le notaire pour l'acte définitif\n\n"
        "💰 Frais à prévoir en plus du prix :\n"
        "• Droits d'enregistrement : 4%\n"
        "• Frais de notaire : 1 à 1,5%\n"
        "• Frais d'agence : 2 à 3% (si agence)\n"
        "• Conservation foncière : 1%"
    ),

    "louer": (
        "🔑 Location immobilière au Maroc\n\n"
        "La location est une alternative à l'achat ou une stratégie d'investissement :\n\n"
        "📊 Rendements locatifs par ville :\n"
        "• Casablanca : 4 à 6% brut annuel\n"
        "• Marrakech (location courte durée) : 6 à 10%\n"
        "• Rabat : 4 à 5%\n"
        "• Agadir : 5 à 8%\n\n"
        "📝 Points légaux importants :\n"
        "• Établissez toujours un contrat de bail écrit\n"
        "• Le dépôt de garantie est plafonné à 2 mois de loyer\n"
        "• La loi 67-12 encadre les relations bailleur-locataire\n\n"
        "💡 Conseils pour propriétaires :\n"
        "• Meublez le bien pour maximiser le loyer\n"
        "• Optez pour la location courte durée dans les villes touristiques\n"
        "• Sélectionnez soigneusement vos locataires"
    ),

    "notaire": (
        "⚖️ Le rôle du notaire dans l'immobilier marocain\n\n"
        "Au Maroc, le notaire joue un rôle central et obligatoire :\n\n"
        "📋 Ses missions principales :\n"
        "• Vérification de la situation juridique du bien\n"
        "• Rédaction et authentification de l'acte de vente\n"
        "• Calcul et collecte des droits de mutation\n"
        "• Inscription à la Conservation Foncière\n\n"
        "💰 Coût des frais de notaire :\n"
        "• Honoraires notariaux : 1 à 1,5% du prix de vente\n"
        "• Droits d'enregistrement : 4%\n"
        "• Conservation foncière : 1%\n"
        "• Total estimé : 6 à 7% du prix de vente\n\n"
        "⚠️ Important : Ne signez jamais un acte de vente sans passer par un notaire. "
        "Les ventes informelles vous exposent à de graves risques juridiques."
    ),

    "credit": (
        "🏦 Le crédit immobilier au Maroc\n\n"
        "Financer votre achat par crédit est très courant. Voici ce qu'il faut savoir :\n\n"
        "📊 Conditions actuelles du marché :\n"
        "• Taux d'intérêt : 4% à 6% selon les banques et votre profil\n"
        "• Durée maximale : 25 ans (certaines banques jusqu'à 30 ans)\n"
        "• Apport personnel recommandé : 20 à 30% du prix\n"
        "• Taux d'endettement maximum : 40% des revenus nets\n\n"
        "🏛️ Principales banques pour le crédit immo :\n"
        "CIH Bank, Attijariwafa Bank, BMCE, BCP, Société Générale\n\n"
        "💡 Conseils pour obtenir le meilleur taux :\n"
        "• Comparez les offres de plusieurs banques\n"
        "• Négociez : les taux sont souvent négociables\n"
        "• Simulez en ligne avant de vous engager\n"
        "• Vérifiez les frais de dossier et d'assurance"
    ),

    "darpredict": (
        "🤖 À propos de DarPredict\n\n"
        "DarPredict est une application d'IA dédiée à l'estimation "
        "des prix immobiliers au Maroc :\n\n"
        "🎯 Notre mission :\n"
        "Rendre l'estimation immobilière accessible, rapide et objective.\n\n"
        "⚙️ Comment utiliser l'application :\n"
        "1. Remplissez le formulaire avec les caractéristiques du bien\n"
        "2. Cliquez sur 'Predict Price'\n"
        "3. Obtenez une estimation en quelques secondes\n"
        "4. Sauvegardez vos estimations pour les comparer\n\n"
        "🔍 Les données analysées :\n"
        "Surface, chambres, salles de bain, cuisine, étage, année de construction, "
        "ville, et 9 équipements (piscine, garage, balcon, terrasse...).\n\n"
        "💡 Faites plusieurs simulations en variant les paramètres pour comprendre "
        "l'impact de chaque critère sur le prix final."
    ),

    "aide": (
        "🆘 Comment puis-je vous aider ?\n\n"
        "Je suis PreHi, votre assistant immobilier. Voici les sujets "
        "sur lesquels je peux vous renseigner :\n\n"
        "🏠 Utilisation de DarPredict :\n"
        "→ 'Comment fonctionne la prédiction ?'\n\n"
        "📊 Critères d'estimation :\n"
        "→ surface, chambres, étage, année, cuisine, ascenseur...\n\n"
        "📍 Localisation :\n"
        "→ ville, quartier, localisation\n\n"
        "🏡 Équipements :\n"
        "→ piscine, garage, terrasse, parking, jardin...\n\n"
        "💼 Marché et conseils :\n"
        "→ acheter, louer, investir, crédit, notaire\n\n"
        "Posez votre question librement, je ferai de mon mieux ! 😊"
    ),

    "_fallback": (
        "🤔 Je n'ai pas bien compris votre question.\n\n"
        "Voici quelques exemples de questions que vous pouvez me poser :\n"
        "• 'Comment fonctionne la prédiction de prix ?'\n"
        "• 'Quel est l'impact de la surface sur le prix ?'\n"
        "• 'Est-ce que la piscine augmente la valeur ?'\n"
        "• 'Comment acheter un bien immobilier au Maroc ?'\n"
        "• 'Quelles villes sont les plus chères ?'\n\n"
        "Reformulez votre question et j'essaierai de vous aider au mieux. 😊"
    ),
}


def get_response(user_input: str) -> str:
    """
    Intelligent FAQ matching (offline):
    1. Normalize input (lowercase + strip accents)
    2. Score each topic by synonym matches (longer = higher score)
    3. Return the richest matching response
    """
    norm = _normalize(user_input)

    scores: dict[str, int] = {}
    for topic, synonyms in SYNONYMS.items():
        score = 0
        for syn in synonyms:
            if _normalize(syn) in norm:
                score += len(syn.split())   # longer match = higher weight
        if score > 0:
            scores[topic] = score

    if scores:
        best_topic = max(scores, key=lambda t: scores[t])
        return RESPONSES.get(best_topic, RESPONSES["_fallback"])

    return RESPONSES["_fallback"]


# ══════════════════════════════════════════════════════════════════════════════
#  STYLESHEET
# ══════════════════════════════════════════════════════════════════════════════

STYLE = """
QWidget#mainBg { background: #F5F3EE; }
QScrollArea#mainScroll { border: none; background: #F5F3EE; }
QLabel#mainTitle {
    font-size: 26px; font-weight: 800; color: #1a2e2d; font-family: 'Segoe UI';
}
QLabel#mainSubtitle { font-size: 13px; color: #6b7f7e; font-family: 'Segoe UI'; }
QWidget#formCard {
    background: white; border-radius: 16px; border: 1px solid #d8e4e3;
}
QLabel#cardTitle { font-size: 15px; font-weight: 700; color: #1a2e2d; }
QLabel#fieldLabel { font-size: 12px; font-weight: 600; color: #6b7f7e; }
QLineEdit#fieldInput {
    border: 1.5px solid #d8e4e3; border-radius: 10px; padding: 0 12px;
    font-size: 14px; color: #1a2e2d; background: #F5F3EE; font-family: 'Segoe UI';
}
QLineEdit#fieldInput:focus { border-color: #6CB8A9; background: white; }
QComboBox#fieldCombo {
    border: 1.5px solid #d8e4e3; border-radius: 10px; padding: 0 12px;
    font-size: 14px; color: #1a2e2d; background: #F5F3EE;
}
QComboBox#fieldCombo:focus { border-color: #6CB8A9; }
QComboBox#fieldCombo::drop-down { border: none; width: 30px; }
QWidget#featureTile {
    background: #F5F3EE; border-radius: 14px; border: 1.5px solid #d8e4e3;
    min-width: 100px; min-height: 100px;
}
QWidget#featureTile:hover { border-color: #6CB8A9; background: #eaf4f2; }
QLabel#tileLabel { font-size: 11px; color: #6b7f7e; font-weight: 600; }
QPushButton#btnPredict {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #6CB8A9,stop:1 #1F5F5B);
    color: white; border: none; border-radius: 14px;
    font-size: 16px; font-weight: 700; font-family: 'Segoe UI';
}
QPushButton#btnPredict:hover {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #7ecabb,stop:1 #2a7570);
}
QPushButton#avatarChip {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #6CB8A9,stop:1 #1F5F5B);
    color: white; border: none; border-radius: 22px;
    font-size: 13px; font-weight: 600; padding: 0 16px;
}
QPushButton#avatarChip:hover { background: #1F5F5B; }
QPushButton#btnChat {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #6CB8A9,stop:1 #1F5F5B);
    color: white; border: none; border-radius: 22px;
    font-size: 13px; font-weight: 600; padding: 0 16px;
}
QPushButton#btnChat:hover { background: #2a7570; }
QPushButton#btnLogout {
    background: rgba(220,60,60,0.10); color: #c0392b;
    border: 1.5px solid rgba(220,60,60,0.30); border-radius: 22px;
    font-size: 13px; font-weight: 600; padding: 0 16px;
}
QPushButton#btnLogout:hover { background: rgba(220,60,60,0.20); }
QPushButton#btnSave {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #f0a500,stop:1 #c47d00);
    color: white; border: none; border-radius: 22px;
    font-size: 13px; font-weight: 600; padding: 0 16px;
}
QPushButton#btnSave:hover { background: #c47d00; }
QWidget#resultPanel {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #6CB8A9,stop:1 #1F5F5B);
    border-radius: 20px;
}
QLabel#resultSub   { color: rgba(255,255,255,0.75); font-size: 13px; }
QLabel#resultPrice { color: white; font-size: 36px; font-weight: 800; }
QLabel#resultMeta  { color: rgba(255,255,255,0.65); font-size: 12px; }
QWidget#chatPanel  { background: white; border-left: 1.5px solid #d8e4e3; }
QTextEdit#chatHistory {
    background: #F5F3EE; border: none; border-radius: 12px;
    font-size: 13px; color: #1a2e2d; padding: 8px;
}
QLineEdit#chatInput {
    border: 1.5px solid #d8e4e3; border-radius: 20px; padding: 0 16px;
    font-size: 13px; color: #1a2e2d; background: #F5F3EE;
}
QLineEdit#chatInput:focus { border-color: #6CB8A9; background: white; }
QPushButton#btnSend {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #6CB8A9,stop:1 #1F5F5B);
    color: white; border: none; border-radius: 20px;
    font-size: 14px; font-weight: 700;
}
QPushButton#btnSend:hover { background: #1F5F5B; }
"""


# ══════════════════════════════════════════════════════════════════════════════
#  PREDICTION WORKER
# ══════════════════════════════════════════════════════════════════════════════

class PredictionWorker(QThread):
    done  = pyqtSignal(float)
    error = pyqtSignal(str)

    def __init__(self, features: dict):
        super().__init__()
        self.features = features

    def run(self):
        try:
            from prediction import predict_price
            price = predict_price(self.features)
            self.done.emit(float(price))
        except Exception as e:
            self.error.emit(str(e))


# ══════════════════════════════════════════════════════════════════════════════
#  FEATURE TILE
# ══════════════════════════════════════════════════════════════════════════════

class FeatureTile(QWidget):
    def __init__(self, emoji: str, label: str, key: str):
        super().__init__()
        self.key = key
        self.setObjectName("featureTile")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(4)

        icon = QLabel(emoji)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setFont(QFont("Segoe UI Emoji", 24))

        lbl = QLabel(label)
        lbl.setObjectName("tileLabel")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.checkbox = QCheckBox()
        self.checkbox.setObjectName("tileCheck")

        layout.addWidget(icon)
        layout.addWidget(lbl)
        layout.addWidget(self.checkbox, alignment=Qt.AlignmentFlag.AlignCenter)

    def value(self) -> int:
        return 1 if self.checkbox.isChecked() else 0


# ══════════════════════════════════════════════════════════════════════════════
#  CHAT PANEL
# ══════════════════════════════════════════════════════════════════════════════

class ChatPanel(QWidget):
    PANEL_WIDTH = 360

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("chatPanel")
        self.setFixedWidth(self.PANEL_WIDTH)
        self._history: list[dict] = []
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        # Title row
        title_row = QHBoxLayout()
        title = QLabel("🏠 PreHi — Assistant Immobilier")
        title.setStyleSheet("font-size:14px; font-weight:700; color:#1a2e2d;")
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(28, 28)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton { background:#f0eded; border:none; border-radius:14px;
                          color:#6b7f7e; font-size:14px; }
            QPushButton:hover { background:#d8e4e3; }
        """)
        close_btn.clicked.connect(self.hide)
        title_row.addWidget(title)
        title_row.addStretch()
        title_row.addWidget(close_btn)
        layout.addLayout(title_row)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #d8e4e3;")
        layout.addWidget(sep)

        # Chat history
        self.history_display = QTextEdit()
        self.history_display.setObjectName("chatHistory")
        self.history_display.setReadOnly(True)
        self.history_display.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        layout.addWidget(self.history_display)

        self._append_bot(
            "Bonjour ! Je suis PreHi, votre assistant immobilier expert. 🏠\n\n"
            "Je peux vous aider sur :\n"
            "• L'estimation des prix immobiliers\n"
            "• Les critères qui valorisent un bien\n"
            "• Le marché immobilier marocain\n"
            "• Les conseils d'achat, vente et location\n\n"
            "Posez-moi votre question ! 😊"
        )

        # Quick suggestion chips
        chips_row = QHBoxLayout()
        chips_row.setSpacing(6)
        for label in ["Comment ça marche ?", "Investir ?", "Aide"]:
            chip = QPushButton(label)
            chip.setFixedHeight(28)
            chip.setCursor(Qt.CursorShape.PointingHandCursor)
            chip.setStyleSheet("""
                QPushButton {
                    background: #eaf4f2; color: #1F5F5B;
                    border: 1px solid #6CB8A9; border-radius: 14px;
                    font-size: 11px; font-weight: 600; padding: 0 10px;
                }
                QPushButton:hover { background: #6CB8A9; color: white; }
            """)
            chip.clicked.connect(lambda _, t=label: self._send_text(t))
            chips_row.addWidget(chip)
        chips_row.addStretch()
        layout.addLayout(chips_row)

        # Input row
        input_row = QHBoxLayout()
        self.chat_input = QLineEdit()
        self.chat_input.setObjectName("chatInput")
        self.chat_input.setPlaceholderText("Votre question sur l'immobilier…")
        self.chat_input.setFixedHeight(40)
        self.chat_input.returnPressed.connect(self._send)

        send_btn = QPushButton("➤")
        send_btn.setObjectName("btnSend")
        send_btn.setFixedSize(40, 40)
        send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        send_btn.clicked.connect(self._send)

        input_row.addWidget(self.chat_input)
        input_row.addWidget(send_btn)
        layout.addLayout(input_row)

    def _append_user(self, text: str):
        safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self.history_display.append(
            f'<div style="text-align:right;margin:6px 0;">'
            f'<span style="background:#6CB8A9;color:white;border-radius:12px;'
            f'padding:8px 14px;font-size:13px;">{safe}</span></div>'
        )

    def _append_bot(self, text: str):
        safe = (text
                .replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                .replace("\n", "<br>"))
        self.history_display.append(
            f'<div style="text-align:left;margin:6px 0;">'
            f'<span style="background:#eaf4f2;color:#1a2e2d;border-radius:12px;'
            f'padding:8px 14px;font-size:13px;display:inline-block;line-height:1.5;">'
            f'{safe}</span></div>'
        )
        sb = self.history_display.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _send_text(self, text: str):
        """Used by suggestion chips."""
        self.chat_input.setText(text)
        self._send()

    def _send(self):
        msg = self.chat_input.text().strip()
        if not msg:
            return
        self.chat_input.clear()
        self._append_user(msg)

        reply = get_response(msg)
        self._history.append({"role": "user",      "content": msg})
        self._history.append({"role": "assistant",  "content": reply})
        self._append_bot(reply)


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN WINDOW
# ══════════════════════════════════════════════════════════════════════════════

class MainWindow(QMainWindow):
    FEATURES = [
        ("🏊", "Piscine",   "piscine"),
        ("🚗", "Garage",    "garage"),
        ("🌱", "Balcon",    "balcon"),
        ("☀️",  "Terrasse",  "terrasse"),
        ("🅿️",  "Parking",  "parking"),
        ("🧑‍🌾", "Gardien",  "gardien"),
        ("🛗",  "Ascenseur","ascenseur"),
        ("🌳", "Jardin",    "jardin"),
        ("🌅", "Belle Vue", "belle_vue"),
    ]

    def __init__(self, user: dict):
        super().__init__()
        self.user = user
        self.setWindowTitle("DarPredict")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet(STYLE)
        self._build_ui()

    def _build_ui(self):
        outer_widget = QWidget()
        outer_layout = QHBoxLayout(outer_widget)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        self.setCentralWidget(outer_widget)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("mainScroll")
        outer_layout.addWidget(scroll, stretch=1)

        root = QWidget()
        root.setObjectName("mainBg")
        scroll.setWidget(root)
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(40, 30, 40, 40)
        root_layout.setSpacing(24)

        root_layout.addLayout(self._build_header())

        form_row = QHBoxLayout()
        form_row.setSpacing(20)
        form_row.addWidget(self._build_basic_info_card())
        form_row.addWidget(self._build_property_details_card())
        root_layout.addLayout(form_row)

        root_layout.addWidget(self._build_features_card())

        predict_btn = QPushButton("$  Predict Price")
        predict_btn.setObjectName("btnPredict")
        predict_btn.setFixedHeight(56)
        predict_btn.clicked.connect(self._handle_predict)
        root_layout.addWidget(predict_btn)

        self.result_panel = self._build_result_panel()
        self.result_panel.hide()
        root_layout.addWidget(self.result_panel)

        self.chat_panel = ChatPanel()
        self.chat_panel.hide()
        outer_layout.addWidget(self.chat_panel)

    def _build_header(self):
        row = QHBoxLayout()

        left = QVBoxLayout()
        title = QLabel("DarPredict")
        title.setObjectName("mainTitle")
        subtitle = QLabel(
            f"Hello, {self.user.get('username', 'User')}! "
            "Fill in the details to predict property value"
        )
        subtitle.setObjectName("mainSubtitle")
        left.addWidget(title)
        left.addWidget(subtitle)

        username = self.user.get('username', 'User')
        avatar = QPushButton(f"  {username[:1].upper()}  {username}")
        avatar.setObjectName("avatarChip")
        avatar.setFixedHeight(44)
        avatar.setCursor(Qt.CursorShape.PointingHandCursor)
        avatar.clicked.connect(self._open_profile)

        chat_btn = QPushButton("💬 PreHi")
        chat_btn.setObjectName("btnChat")
        chat_btn.setFixedHeight(44)
        chat_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        chat_btn.clicked.connect(self._toggle_chat)

        save_btn = QPushButton("💾  Save")
        save_btn.setObjectName("btnSave")
        save_btn.setFixedHeight(44)
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self._handle_save)

        logout_btn = QPushButton("  Log out")
        logout_btn.setObjectName("btnLogout")
        logout_btn.setFixedHeight(44)
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_btn.clicked.connect(self._handle_logout)

        row.addLayout(left)
        row.addStretch()
        row.addWidget(save_btn)
        row.addWidget(chat_btn)
        row.addWidget(avatar)
        row.addWidget(logout_btn)
        return row

    def _handle_save(self):
        import json
        from datetime import datetime

        data = {
            "surface":        self.surface_input.text().strip(),
            "chambres":       self.chambres_input.text().strip(),
            "salles_de_bain": self.sdb_input.text().strip(),
            "kitchen":        self.kitchen_combo.currentText(),
            "etage":          self.etage_input.text().strip(),
            "annee":          self.annee_input.text().strip(),
            "localisation":   self.city_combo.currentText(),
            "quartier":       self.neighborhood_input.text().strip(),
            **{key: tile.value() for key, tile in self.feature_tiles.items()},
            "saved_by":       self.user.get("email", "unknown"),
            "saved_at":       datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        save_dir  = os.path.join(os.path.dirname(__file__), "..", "data")
        save_path = os.path.join(save_dir, "saved_form.json")
        os.makedirs(save_dir, exist_ok=True)

        existing = []
        if os.path.isfile(save_path):
            try:
                with open(save_path, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            except Exception:
                existing = []

        existing.append(data)
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)

        QMessageBox.information(self, "Sauvegardé", "✅ Formulaire sauvegardé avec succès !")

    def _open_profile(self):
        try:
            from ui.profile_widget import ProfileModal
            modal = ProfileModal(self.user, parent=self)
            modal.exec()
        except ImportError:
            QMessageBox.information(
                self, "Profil",
                f"Utilisateur : {self.user.get('username', 'N/A')}\n"
                f"Email       : {self.user.get('email', 'N/A')}"
            )

    def _toggle_chat(self):
        if self.chat_panel.isVisible():
            self.chat_panel.hide()
        else:
            self.chat_panel.show()

    def _handle_logout(self):
        reply = QMessageBox.question(
            self, "Déconnexion",
            "Voulez-vous vraiment vous déconnecter ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Cancel,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.close()

    def _build_basic_info_card(self):
        card = QWidget()
        card.setObjectName("formCard")
        layout = QVBoxLayout(card)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        title_row = QHBoxLayout()
        icon = QLabel("🏠")
        icon.setFont(QFont("Segoe UI Emoji", 18))
        card_title = QLabel("Basic Information")
        card_title.setObjectName("cardTitle")
        title_row.addWidget(icon)
        title_row.addWidget(card_title)
        title_row.addStretch()
        layout.addLayout(title_row)

        layout.addWidget(self._lbl("Surface (m²)"))
        self.surface_input = QLineEdit()
        self.surface_input.setPlaceholderText("150")
        self.surface_input.setObjectName("fieldInput")
        self.surface_input.setFixedHeight(42)
        layout.addWidget(self.surface_input)

        br_row = QHBoxLayout()
        bl = QVBoxLayout()
        br = QVBoxLayout()

        bl.addWidget(self._lbl("🛏  Chambres"))
        self.chambres_input = QLineEdit()
        self.chambres_input.setPlaceholderText("3")
        self.chambres_input.setObjectName("fieldInput")
        self.chambres_input.setFixedHeight(42)
        bl.addWidget(self.chambres_input)

        br.addWidget(self._lbl("🛁  Salles de bain"))
        self.sdb_input = QLineEdit()
        self.sdb_input.setPlaceholderText("2")
        self.sdb_input.setObjectName("fieldInput")
        self.sdb_input.setFixedHeight(42)
        br.addWidget(self.sdb_input)

        br_row.addLayout(bl)
        br_row.addLayout(br)
        layout.addLayout(br_row)

        layout.addWidget(self._lbl("Kitchen"))
        self.kitchen_combo = QComboBox()
        self.kitchen_combo.setObjectName("fieldCombo")
        self.kitchen_combo.addItem("Select type")
        self.kitchen_combo.addItems(list(KITCHEN_MAP.keys()))
        self.kitchen_combo.setFixedHeight(42)
        layout.addWidget(self.kitchen_combo)

        layout.addStretch()
        return card

    def _build_property_details_card(self):
        card = QWidget()
        card.setObjectName("formCard")
        layout = QVBoxLayout(card)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        title_row = QHBoxLayout()
        icon = QLabel("🏢")
        icon.setFont(QFont("Segoe UI Emoji", 18))
        card_title = QLabel("Property Details")
        card_title.setObjectName("cardTitle")
        title_row.addWidget(icon)
        title_row.addWidget(card_title)
        title_row.addStretch()
        layout.addLayout(title_row)

        layout.addWidget(self._lbl("⬡  Étage"))
        self.etage_input = QLineEdit()
        self.etage_input.setPlaceholderText("2")
        self.etage_input.setObjectName("fieldInput")
        self.etage_input.setFixedHeight(42)
        layout.addWidget(self.etage_input)

        layout.addWidget(self._lbl("📅  Année de construction"))
        self.annee_input = QLineEdit()
        self.annee_input.setPlaceholderText("2020")
        self.annee_input.setObjectName("fieldInput")
        self.annee_input.setFixedHeight(42)
        layout.addWidget(self.annee_input)

        layout.addWidget(self._lbl("📍  Ville"))
        self.city_combo = QComboBox()
        self.city_combo.setObjectName("fieldCombo")
        self.city_combo.addItem("Sélectionner une ville")
        self.city_combo.addItems(VILLES)
        self.city_combo.setFixedHeight(42)
        layout.addWidget(self.city_combo)

        layout.addWidget(self._lbl("Area / Neighborhood"))
        self.neighborhood_input = QLineEdit()
        self.neighborhood_input.setPlaceholderText("Maarif")
        self.neighborhood_input.setObjectName("fieldInput")
        self.neighborhood_input.setFixedHeight(42)
        layout.addWidget(self.neighborhood_input)

        layout.addStretch()
        return card

    def _build_features_card(self):
        card = QWidget()
        card.setObjectName("formCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Property Features")
        title.setObjectName("cardTitle")
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(12)
        self.feature_tiles = {}

        for idx, (emoji, label, key) in enumerate(self.FEATURES):
            tile = FeatureTile(emoji, label, key)
            self.feature_tiles[key] = tile
            grid.addWidget(tile, idx // 5, idx % 5)

        layout.addLayout(grid)
        return card

    def _build_result_panel(self):
        panel = QWidget()
        panel.setObjectName("resultPanel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(8)

        self.result_sub = QLabel("Estimated Property Value")
        self.result_sub.setObjectName("resultSub")
        self.result_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.result_price = QLabel("—")
        self.result_price.setObjectName("resultPrice")
        self.result_price.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.result_meta = QLabel("")
        self.result_meta.setObjectName("resultMeta")
        self.result_meta.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.result_sub)
        layout.addWidget(self.result_price)
        layout.addWidget(self.result_meta)
        return panel

    def _handle_predict(self):
        features, err = self._collect_and_validate()
        if err:
            QMessageBox.warning(self, "Erreur de validation", err)
            return

        self.result_price.setText("Calcul en cours…")
        self.result_panel.show()

        self._worker = PredictionWorker(features)
        self._worker.done.connect(lambda p: self._on_done(p, features))
        self._worker.error.connect(self._on_error)
        self._worker.start()

    def _on_done(self, price: float, features: dict):
        formatted = f"{int(price):,}".replace(",", ".") + " DH"
        self.result_price.setText(formatted)
        city    = features.get("localisation", "")
        surface = features.get("surface", "")
        hood    = self.neighborhood_input.text().strip()
        self.result_meta.setText(f"Based on {surface}m² in {city}, {hood}")
        self.result_panel.show()
        self._log_prediction(features, int(price))

    def _on_error(self, msg: str):
        QMessageBox.critical(self, "Erreur de prédiction", msg)
        self.result_price.setText("Erreur")

    def _collect_and_validate(self):
        try:
            surface = float(self.surface_input.text())
            assert surface > 0
        except Exception:
            return None, "Surface invalide."
        try:
            chambres = int(self.chambres_input.text())
        except Exception:
            return None, "Nombre de chambres invalide."
        try:
            sdb = int(self.sdb_input.text())
        except Exception:
            return None, "Nombre de salles de bain invalide."

        kitchen_text = self.kitchen_combo.currentText()
        if kitchen_text == "Select type":
            return None, "Veuillez sélectionner un type de cuisine."
        kitchen_val = KITCHEN_MAP[kitchen_text]

        try:
            etage = int(self.etage_input.text())
        except Exception:
            return None, "Étage invalide."
        try:
            annee = int(self.annee_input.text())
            assert 1900 <= annee <= 2026
        except Exception:
            return None, "Année invalide (1900-2026)."

        ville = self.city_combo.currentText()
        if ville == "Sélectionner une ville":
            return None, "Veuillez sélectionner une ville."

        features = {
            "surface":        surface,
            "chambres":       chambres,
            "salles_de_bain": sdb,
            "kitchen":        kitchen_val,
            "etage":          etage,
            "annee":          annee,
            "localisation":   ville,
            **{key: tile.value() for key, tile in self.feature_tiles.items()},
        }
        return features, None

    def _log_prediction(self, features: dict, price: int):
        import csv, uuid
        from datetime import datetime

        log_path = os.path.join(os.path.dirname(__file__), "..", "data", "predictions.csv")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        file_exists = os.path.isfile(log_path)
        row = {
            "id":             str(uuid.uuid4())[:8],
            "user_email":     self.user.get("email", "unknown"),
            "surface":        features["surface"],
            "chambres":       features["chambres"],
            "salles_de_bain": features["salles_de_bain"],
            "kitchen":        features["kitchen"],
            "etage":          features["etage"],
            "annee":          features["annee"],
            "localisation":   features["localisation"],
            "piscine":        features["piscine"],
            "garage":         features["garage"],
            "balcon":         features["balcon"],
            "terrasse":       features["terrasse"],
            "parking":        features["parking"],
            "gardien":        features["gardien"],
            "ascenseur":      features["ascenseur"],
            "jardin":         features["jardin"],
            "belle_vue":      features["belle_vue"],
            "prix_predit_DH": price,
            "date":           datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        with open(log_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(row.keys()))
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)

    @staticmethod
    def _lbl(text):
        lbl = QLabel(text)
        lbl.setObjectName("fieldLabel")
        return lbl
"""
Configuration constants for the War of the Ring pygame interface.
"""

from pathlib import Path
from enum import Enum, auto
from game_env.army import FreeUnit, ShadowUnit, ArmyUnit
from game_env.action_dice.dice import ActionResult
from game_env.game_env_enums import Player
from game_env.regions_enum import R


# =============================================================================
# Paths
# =============================================================================

BASE_DIR = Path(__file__).parent
IMAGES_DIR = BASE_DIR / "images"
GUIDANCE_DIR = BASE_DIR / "guidance"
CARDS_DIR = IMAGES_DIR / "cards"
SMALLCARDS_DIR = IMAGES_DIR / "smallcards"
UNITS_DIR = IMAGES_DIR / "units"
REGIONS_JSON = GUIDANCE_DIR / "regions_en.json"


# =============================================================================
# Display Settings
# =============================================================================

# Window settings
WINDOW_TITLE = "War of the Ring"
DEFAULT_WINDOW_WIDTH = 1600
DEFAULT_WINDOW_HEIGHT = 900
MIN_WINDOW_WIDTH = 1280
MIN_WINDOW_HEIGHT = 720
FPS = 60

# Board scaling (which board image to use as base)
# Available: 80, 90, 100, 110, 120, 130, 140, 150, 200
DEFAULT_BOARD_SCALE = 140

# Layout dimensions (percentages of window)
SIDEBAR_WIDTH_PERCENT = 0.20  # 20% of window width
CARD_PANEL_HEIGHT = 120  # Fixed pixel height
ACTION_PANEL_HEIGHT = 80  # Fixed pixel height
BOARD_MARGIN = 10


# =============================================================================
# Colors
# =============================================================================

class Colors:
    # Basic colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)
    LIGHT_GRAY = (192, 192, 192)

    # UI colors
    BACKGROUND = (30, 30, 35)
    PANEL_BG = (45, 45, 50)
    PANEL_BORDER = (80, 80, 90)
    TEXT_PRIMARY = (240, 240, 240)
    TEXT_SECONDARY = (180, 180, 180)
    TEXT_MUTED = (120, 120, 120)

    # Player colors
    FREE_PEOPLES = (70, 130, 180)  # Steel blue
    SHADOW = (139, 69, 69)  # Dark red

    # Nation colors (from regions_en.json)
    ELVES = (4, 143, 26)  # #048f1a
    DWARVES = (80, 27, 19)  # #501b13
    GONDOR = (67, 66, 108)  # #43426c
    NORTH = (12, 138, 179)  # #0c8ab3
    ROHAN = (4, 107, 38)  # #046b26
    ISENGARD = (222, 216, 0)  # #ded800
    SAURON = (224, 80, 23)  # #e05017
    SOUTHRONS = (250, 172, 37)  # #faac25
    EASTERLINGS = (250, 172, 37)  # #faac25
    NEUTRAL = (192, 192, 192)  # #c0c0c0

    # Highlight colors
    HIGHLIGHT_SELECTED = (255, 215, 0, 150)  # Gold with alpha
    HIGHLIGHT_VALID_MOVE = (0, 255, 0, 100)  # Green with alpha
    HIGHLIGHT_HOVER = (255, 255, 255, 80)  # White with alpha
    HIGHLIGHT_ATTACK = (255, 0, 0, 100)  # Red with alpha

    # Card panel
    CARD_BORDER = (100, 100, 110)
    CARD_SELECTED = (255, 215, 0)

    # Dice
    DICE_BG = (60, 60, 65)
    DICE_BORDER = (100, 100, 110)


# =============================================================================
# Unit Image Mapping
# =============================================================================

UNIT_IMAGES = {
    # Free Peoples - North
    FreeUnit.nort_reg: "NorthRegular.png",
    FreeUnit.nort_elt: "NorthElite.png",
    FreeUnit.nort_ldr: "NorthLeader.png",
    # Free Peoples - Elves
    FreeUnit.elvn_reg: "ElvenRegular.png",
    FreeUnit.elvn_elt: "ElvenElite.png",
    FreeUnit.elvn_ldr: "ElvenLeader.png",
    # Free Peoples - Dwarves
    FreeUnit.dwar_reg: "DwarvenRegular.png",
    FreeUnit.dwar_elt: "DwarvenElite.png",
    FreeUnit.dwar_ldr: "DwarvenLeader.png",
    # Free Peoples - Rohan
    FreeUnit.rohn_reg: "RohanRegular.png",
    FreeUnit.rohn_elt: "RohanElite.png",
    FreeUnit.rohn_ldr: "RohanLeader.png",
    # Free Peoples - Gondor
    FreeUnit.gond_reg: "GondorRegular.png",
    FreeUnit.gond_elt: "GondorElite.png",
    FreeUnit.gond_ldr: "GondorLeader.png",
    # Shadow - Isengard
    ShadowUnit.isen_reg: "IsengardRegular.png",
    ShadowUnit.isen_elt: "IsengardElite.png",
    # Shadow - Mordor/Sauron
    ShadowUnit.mord_reg: "SauronRegular.png",
    ShadowUnit.mord_elt: "SauronElite.png",
    # Shadow - Easterlings/Southrons
    ShadowUnit.east_reg: "SouthronRegular.png",
    ShadowUnit.east_elt: "SouthronElite.png",
    # Nazgul
    ShadowUnit.nazgul: "Nazgul.png",
}

# Character images
CHARACTER_IMAGES = {
    "gandalf_grey": "Gandalfthegrey.png",
    "gandalf_white": "Gandalfthewhite.png",
    "strider": "Strider.png",
    "aragorn": "Aragorn.png",
    "boromir": "Boromir.png",
    "legolas": "Legolas.png",
    "gimli": "Gimli.png",
    "merry": "Merry.png",
    "pippin": "Pippin.png",
    "gollum": "Gollum.png",
    "saruman": "Saruman.png",
    "witch_king": "WitchKing.png",
    "mouth": "Mouth.png",
}

# Fellowship marker
FELLOWSHIP_IMAGE = "Fellowship.png"
FELLOWSHIP_REVEALED_IMAGE = "Fellowship_revealed.png"


# =============================================================================
# Action Dice Image Mapping
# =============================================================================

ACTION_DICE_IMAGES = {
    Player.FREE: {
        ActionResult.CHARACTER: "ADFPcharacter.png",
        ActionResult.MUSTER: "ADFPmuster.png",
        ActionResult.PALANTIR: "ADFPevent.png",
        ActionResult.HYBRID: "ADFParmymuster.png",
        ActionResult.WILL: "ADFPwill.png",
        # Free peoples don't have ARMY or EYE
    },
    Player.SHADOW: {
        ActionResult.CHARACTER: "ADSAcharacter.png",
        ActionResult.MUSTER: "ADSAmuster.png",
        ActionResult.PALANTIR: "ADSAevent.png",
        ActionResult.HYBRID: "ADSAarmymuster.png",
        ActionResult.ARMY: "ADSAarmy.png",
        ActionResult.EYE: "ADSAeye.png",
    },
}


# =============================================================================
# Region ID Mapping (JSON ID -> R enum)
# =============================================================================

# This maps the JSON region IDs to the game_env R enum values
# Based on name matching between regions_en.json and regions_enum.py
REGION_JSON_TO_ENUM = {
    # Elves (1xx)
    101: R.GREY_HAVENS,
    102: R.RIVENDELL,
    103: R.LORIEN,
    104: R.WOODLAND_REALM,
    # Dwarves (2xx)
    201: R.NORTH_ERED_LUIN,
    202: R.ERED_LUIN,
    203: R.EREBOR,
    204: R.IRON_HILLS,
    # Gondor (3xx)
    301: R.ANFALAS,
    302: R.ERECH,
    303: R.DOL_AMROTH,
    304: R.LAMEDON,
    305: R.PELARGIR,
    306: R.LOSSARNACH,
    307: R.MINAS_TIRITH,
    308: R.DRUADAN_FOREST,
    # North (4xx)
    401: R.THE_SHIRE,
    402: R.BUCKLAND,
    403: R.BREE,
    404: R.NORTH_DOWNS,
    405: R.CARROCK,
    406: R.RHOSGOBEL,
    407: R.OLD_FOREST_ROAD,
    408: R.DALE,
    # Rohan (5xx)
    501: R.FORDS_OF_ISEN,
    502: R.HELMS_DEEP,
    503: R.WESTEMNET,
    504: R.EDORAS,
    505: R.EASTEMNET,
    506: R.FOLDE,
    # Isengard (6xx)
    601: R.NORTH_DUNLAND,
    602: R.SOUTH_DUNLAND,
    603: R.GAP_OF_ROHAN,
    604: R.ORTHANC,
    # Sauron/Mordor (7xx)
    701: R.ANGMAR,
    702: R.MOUNT_GRAM,
    703: R.MOUNT_GUNDABAD,
    704: R.MORIA,
    705: R.DOL_GULDUR,
    706: R.SOUTHERN_MIRKWOOD,
    707: R.MORANNON,
    708: R.MINAS_MORGUL,
    709: R.NURN,
    710: R.GORGOROTH,
    711: R.BARAD_DUR,
    # Southrons (8xx)
    801: R.UMBAR,
    802: R.NEAR_HARAD,
    803: R.FAR_HARAD,
    804: R.KHAND,
    # Easterlings (9xx)
    901: R.NORTH_RHUN,
    902: R.SOUTH_RHUN,
    903: R.EAST_RHUN,
    # Neutral/Free regions (10xx)
    1001: R.FORLINDON,
    1002: R.EVENDIM,
    1003: R.ARNOR,
    1004: R.ETTENMOORS,
    1005: R.WEATHER_HILLS,
    1006: R.TROLLSHAWS,
    1007: R.SOUTH_DOWNS,
    1008: R.TOWER_HILLS,
    1009: R.HARLINDON,
    1010: R.SOUTH_ERED_LUIN,
    1011: R.OLD_FOREST,
    1012: R.CARDOLAN,
    1013: R.MINHIRIATH,
    1014: R.THARBAD,
    1015: R.ENEDWAITH,
    1016: R.DRUWAITH_IAUR,
    1017: R.ANDRAST,
    1018: R.HOLLIN,
    1019: R.FORDS_OF_BRUINEN,
    1020: R.EAGLES_EYRIE,
    1021: R.OLD_FORD,
    1022: R.GOBLINS_GATE,
    1023: R.HIGH_PASS,
    1024: R.GLADDEN_FIELDS,
    1025: R.DIMRILL_DALE,
    1026: R.FANGORN,
    1027: R.PARTH_CELEBRANT,
    1028: R.NORTHERN_MIRKWOOD,
    1029: R.WITHERED_HEATH,
    1030: R.WESTERN_MIRKWOOD,
    1031: R.NARROWS_OF_THE_FOREST,
    1032: R.EASTERN_MIRKWOOD,
    1033: R.NORTH_ANDUIN_VALE,
    1034: R.SOUTH_ANDUIN_VALE,
    1035: R.WESTERN_BROWN_LANDS,
    1036: R.EASTERN_BROWN_LANDS,
    1037: R.WESTERN_EMYN_MUIL,
    1038: R.EASTERN_EMYN_MUIL,
    1039: R.DEAD_MARSHES,
    1040: R.OSGILIATH,
    1041: R.WEST_HARONDOR,
    1042: R.EAST_HARONDOR,
    1043: R.NORTH_ITHILIEN,
    1044: R.SOUTH_ITHILIEN,
    1045: R.NORTHERN_RHOVANION,
    1046: R.VALE_OF_THE_CARNEN,
    1047: R.VALE_OF_THE_CELDUIN,
    1048: R.SOUTHERN_RHOVANION,
    1049: R.NORTHERN_DORWINION,
    1050: R.SOUTHERN_DORWINION,
    1051: R.NOMAN_LANDS,
    1052: R.DAGORLAD,
    1053: R.ASH_MOUNTAINS,
}

# Reverse mapping (R enum -> JSON ID)
REGION_ENUM_TO_JSON = {v: k for k, v in REGION_JSON_TO_ENUM.items()}


# =============================================================================
# UI Element Sizes
# =============================================================================

# Card sizes
CARD_THUMBNAIL_WIDTH = 60
CARD_THUMBNAIL_HEIGHT = 84
CARD_FULL_WIDTH = 250
CARD_FULL_HEIGHT = 350

# Dice sizes
ACTION_DIE_SIZE = 48
COMBAT_DIE_SIZE = 40

# Unit tokens
UNIT_TOKEN_SIZE = 24
UNIT_TOKEN_SMALL = 18

# Buttons
BUTTON_HEIGHT = 32
BUTTON_MIN_WIDTH = 80
BUTTON_PADDING = 8

# Fonts
FONT_SIZE_LARGE = 24
FONT_SIZE_MEDIUM = 18
FONT_SIZE_SMALL = 14
FONT_SIZE_TINY = 11


# =============================================================================
# Interaction States
# =============================================================================

class InteractionState(Enum):
    IDLE = auto()
    SELECTING_SOURCE = auto()
    SELECTING_DESTINATION = auto()
    SELECTING_CARD = auto()
    SELECTING_UNITS = auto()
    VIEWING_CARD = auto()
    DIALOG_OPEN = auto()
    ROLLING_DICE = auto()


# =============================================================================
# Board image files
# =============================================================================

def get_board_image_path(scale: int = DEFAULT_BOARD_SCALE, variant: str = "") -> Path:
    """
    Get the path to a board image at the specified scale.

    Args:
        scale: Board scale percentage (80, 90, 100, 110, 120, 130, 140, 150, 200)
        variant: Optional variant suffix (e.g., "W" for alternate style)

    Returns:
        Path to the board image file
    """
    filename = "map_en.jpg"
    # if scale == 100:
    #     filename = f"board{variant}.jpg" if variant else "board.jpg"
    # else:
    #     filename = f"board{scale}{variant}.jpg"
    return IMAGES_DIR / filename


# =============================================================================
# Siege overlay mapping
# =============================================================================

SIEGE_OVERLAYS = {
    R.BARAD_DUR: "OverlayBaradDurSiege.png",
    R.DOL_AMROTH: "OverlayDolAmrothSiege.png",
    R.DOL_GULDUR: "OverlayDolGuldurSiege.png",
    R.EREBOR: "OverlayEreborSiege.png",
    R.GREY_HAVENS: "OverlayGreyHavensSiege.png",
    R.HELMS_DEEP: "OverlayHelmsDeepSiege.png",
    R.LORIEN: "OverlayLorienSiege.png",
    R.MINAS_MORGUL: "OverlayMinasMorgulSiege.png",
    R.MINAS_TIRITH: "OverlayMinasTirithSiege.png",
    R.MORANNON: "OverlayMorannonSiege.png",
    R.MORIA: "OverlayMoriaSiege.png",
    R.MOUNT_GUNDABAD: "OverlayMtGundabadSiege.png",
    R.ORTHANC: "OverlayOrthancSiege.png",
    R.RIVENDELL: "OverlayRivendellSiege.png",
    R.UMBAR: "OverlayUmbarSiege.png",
    R.WOODLAND_REALM: "OverlayWoodlandRealmSiege.png",
}


# =============================================================================
# Control markers
# =============================================================================

CONTROL_MARKERS = {
    Player.FREE: "FreeControl.png",
    Player.SHADOW: "ShadowControl.png",
}


# =============================================================================
# Starting unit counts for reinforcement pools
# =============================================================================

# Maximum units available for each nation
MAX_UNITS = {
    # Free Peoples
    "north": {"regular": 6, "elite": 4, "leader": 3},
    "elves": {"regular": 4, "elite": 4, "leader": 3},
    "dwarves": {"regular": 3, "elite": 3, "leader": 3},
    "rohan": {"regular": 6, "elite": 4, "leader": 3},
    "gondor": {"regular": 8, "elite": 4, "leader": 3},
    # Shadow
    "isengard": {"regular": 6, "elite": 4},
    "mordor": {"regular": 12, "elite": 6},
    "easterlings": {"regular": 6, "elite": 4},
}

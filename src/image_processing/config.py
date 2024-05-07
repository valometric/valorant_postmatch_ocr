# config.py

# Maps
MAPS = [
    "ASCENT",
    "BIND",
    "BREEZE",
    "ICEBOX",
    "HAVEN",
    "PEARL",
    "LOTUS",
    "SUNSET",
    "SPLIT",
    "FRACTURE",
]

# Column Indices
COL_HEIGHT_START, COL_HEIGHT_END = 340, 860
ACS_COL_START, ACS_COL_END = 635, 825
IGN_COL_START, IGN_COL_END = 378, 555
KDA_COL_START, KDA_COL_END = 815, 1000
ECON_COL_START, ECON_COL_END = 980, 1120
FIRST_BLOODS_COL_START, FIRST_BLOODS_COL_END = 1160, 1240
PLANTS_COL_START, PLANTS_COL_END = 1300, 1400
DEFUSES_COL_START, DEFUSES_COL_END = 1460, 1550
SCORE_COL_START, SCORE_COL_END = 825, 1060
PROFILE_SCORE_COL_START, PROFILE_SCORE_COL_END = 730, 800
OPPONENT_SCORE_COL_START, OPPONENT_SCORE_COL_END = 1060, 1150
DATE_COL_START, DATE_COL_END = 60, 180
GAME_TYPE_COL_START, GAME_TYPE_COL_END = 70, 180
MAP_COL_START, MAP_COL_END = 50, 200
DURATION_COL_START, DURATION_COL_END = 50, 150
AGENT_COL_START, AGENT_COL_END = 281, 330
SCORE_ROW_START, SCORE_ROW_END = 80, 175
DETAILS_DATE_ROW_START, DETAILS_DATE_ROW_END = 90, 110
DETAILS_GAME_TYPE_ROW_START, DETAILS_GAME_TYPE_ROW_END = 110, 128
DETAILS_MAP_ROW_START, DETAILS_MAP_ROW_END = 128, 140
DETAILS_DURATION_ROW_START, DETAILS_DURATION_ROW_END = 140, 160
UNRANKED_ACS_COL_END = 635 + 177  # Adjusted for ranked games
UNRANKED_IGN_COL_START, UNRANKED_IGN_COL_END = (
    330,
    330 + 177,
)  # Adjusted for ranked games


# Define your class indices mapping based on the output from train_generator.class_indices.items()
class_indices = {
    "Astra_Ally": 0,
    "Astra_Enemy": 1,
    "Astra_Self": 2,
    "Breach_Ally": 3,
    "Breach_Enemy": 4,
    "Breach_Self": 5,
    "Brimstone_Ally": 6,
    "Brimstone_Enemy": 7,
    "Brimstone_Self": 8,
    "Chamber_Ally": 9,
    "Chamber_Enemy": 10,
    "Chamber_Self": 11,
    "Clove_Ally": 12,
    "Clove_Enemy": 13,
    "Clove_Self": 14,
    "Cypher_Ally": 15,
    "Cypher_Enemy": 16,
    "Cypher_Self": 17,
    "Deadlock_Ally": 18,
    "Deadlock_Enemy": 19,
    "Deadlock_Self": 20,
    "Fade_Ally": 21,
    "Fade_Enemy": 22,
    "Fade_Self": 23,
    "Gekko_Ally": 24,
    "Gekko_Enemy": 25,
    "Gekko_Self": 26,
    "Harbor_Ally": 27,
    "Harbor_Enemy": 28,
    "Harbor_Self": 29,
    "Iso_Ally": 30,
    "Iso_Enemy": 31,
    "Iso_Self": 32,
    "Jett_Ally": 33,
    "Jett_Enemy": 34,
    "Jett_Self": 35,
    "KAYO_Ally": 36,
    "KAYO_Enemy": 37,
    "KAYO_Self": 38,
    "Killjoy_Ally": 39,
    "Killjoy_Enemy": 40,
    "Killjoy_Self": 41,
    "Neon_Ally": 42,
    "Neon_Enemy": 43,
    "Neon_Self": 44,
    "Omen_Ally": 45,
    "Omen_Enemy": 46,
    "Omen_Self": 47,
    "Phoenix_Ally": 48,
    "Phoenix_Enemy": 49,
    "Phoenix_Self": 50,
    "Raze_Ally": 51,
    "Raze_Enemy": 52,
    "Raze_Self": 53,
    "Reyna_Ally": 54,
    "Reyna_Enemy": 55,
    "Reyna_Self": 56,
    "Sage_Ally": 57,
    "Sage_Enemy": 58,
    "Sage_Self": 59,
    "Skye_Ally": 60,
    "Skye_Enemy": 61,
    "Skye_Self": 62,
    "Sova_Ally": 63,
    "Sova_Enemy": 64,
    "Sova_Self": 65,
    "Viper_Ally": 66,
    "Viper_Enemy": 67,
    "Viper_Self": 68,
    "Yoru_Ally": 69,
    "Yoru_Enemy": 70,
    "Yoru_Self": 71,
}

# Reversed mapping from index to class label
index_to_class_label = {v: k for k, v in class_indices.items()}

# Tesseract Configuration
CUSTOM_CONFIG = r"--oem 3 --psm 6"

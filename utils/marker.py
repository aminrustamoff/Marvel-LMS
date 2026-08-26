LISTENING_SCORE_MAP = {
    "section_1": {
        0: 2.0,
        1: 2.5,
        2: 3.0,
        3: 3.5,
        4: 4.0,
        5: 4.5,
        6: 5.0,
        7: 6.0,
        8: 7.0,
        9: 8.0,
        10: 9.0,
    },

    "section_2": {
        0: 2.0,
        1: 2.5,
        2: 3.0,
        3: 3.5,
        4: 4.0,
        5: 4.5,
        6: 5.5,
        7: 6.5,
        8: 7.5,
        9: 8.5,
        10: 9.0,
    },

    "section_3": {
        0: 2.0,
        1: 2.5,
        2: 3.0,
        3: 3.5,
        4: 4.5,
        5: 5.0,
        6: 6.0,
        7: 7.0,
        8: 8.0,
        9: 8.5,
        10: 9.0,
    },

    "section_4": {
        0: 2.0,
        1: 2.5,
        2: 3.0,
        3: 4.0,
        4: 4.5,
        5: 5.5,
        6: 6.5,
        7: 7.5,
        8: 8.0,
        9: 8.5,
        10: 9.0,
    },
}

READING_SCORE_MAP = {
    "passage_1": {
        0: 2.0,
        1: 2.5,
        2: 3.0,
        3: 3.5,
        4: 4.0,
        5: 4.5,
        6: 5.0,
        7: 5.5,
        8: 6.0,
        9: 6.5,
        10: 7.0,
        11: 7.5,
        12: 8.0,
        13: 9.0,
        14: 9.0,
    },

    "passage_2": {
        0: 2.0,
        1: 2.5,
        2: 3.0,
        3: 3.5,
        4: 4.0,
        5: 4.5,
        6: 5.0,
        7: 6.0,
        8: 6.5,
        9: 7.0,
        10: 7.5,
        11: 8.0,
        12: 8.5,
        13: 9.0,
        14: 9.0,
    },

    "passage_3": {
        0: 2.0,
        1: 2.5,
        2: 3.0,
        3: 3.5,
        4: 4.0,
        5: 5.0,
        6: 5.5,
        7: 6.5,
        8: 7.0,
        9: 7.5,
        10: 8.0,
        11: 8.5,
        12: 8.75,
        13: 9.0,
        14: 9.0,
    },
}

def get_listening_band(section: int , correct_count: int) -> float|None:
    """Har bir listening sectionlar uchun alohida hisoblangan maxsus hisoblagich"""
    try:
        return LISTENING_SCORE_MAP[f"section_{section}"][correct_count]
    except Exception as e:
        return None

def get_reading_band(passage: int , correct_count: int) -> float|None:
    """Har bir listening sectionlar uchun alohida hisoblangan maxsus hisoblagich"""
    try:
        return READING_SCORE_MAP[f"section_{passage}"][correct_count]
    except Exception as e:
        return None
    
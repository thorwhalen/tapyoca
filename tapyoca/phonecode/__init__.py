"""Phonecode: Making pronounceable codes"""

from tapyoca.phonecode.phonecode import (
    # Data management
    download_required_data,
    get_cmudict,
    get_word_frequencies,
    # Phoneme utilities
    strip_stress,
    get_phonemes,
    word_contains_phonemes,
    is_vowel_phoneme,
    is_consonant_phoneme,
    separate_vowels_consonants,
    # Word finding
    find_words_with_phonemes,
    find_words_for_phoneme_pairs,
    find_multi_pair_words,
    # Mapping classes
    PhonemeMapping,
    GridMapping,
    IntegerMapping,
    CoordsWordCodec,
    # High-level functions
    create_5x5_codenames_mapping,
    create_integer_encoding_mapping,
    print_5x5_results,
    print_integer_results,
    suggest_phonemes_for_grid,
    # Display utilities
    print_coord_words_grid,
    print_two_coord_words_table,
    print_two_coord_summary,
)

__all__ = [
    # Data management
    'download_required_data',
    'get_cmudict',
    'get_word_frequencies',
    # Phoneme utilities
    'strip_stress',
    'get_phonemes',
    'word_contains_phonemes',
    'is_vowel_phoneme',
    'is_consonant_phoneme',
    'separate_vowels_consonants',
    # Word finding
    'find_words_with_phonemes',
    'find_words_for_phoneme_pairs',
    'find_multi_pair_words',
    # Mapping classes
    'PhonemeMapping',
    'GridMapping',
    'IntegerMapping',
    'CoordsWordCodec',
    # High-level functions
    'create_5x5_codenames_mapping',
    'create_integer_encoding_mapping',
    'print_5x5_results',
    'print_integer_results',
    'suggest_phonemes_for_grid',
    # Display utilities
    'print_coord_words_grid',
    'print_two_coord_words_table',
    'print_two_coord_summary',
]

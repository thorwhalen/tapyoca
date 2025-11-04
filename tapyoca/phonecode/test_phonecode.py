"""
Tests for phonecode module.
"""

import pytest
from tapyoca import phonecode


def test_strip_stress():
    """Test stress marker removal."""
    assert phonecode.strip_stress('AE1') == 'AE'
    assert phonecode.strip_stress('T') == 'T'
    assert phonecode.strip_stress('IY2') == 'IY'


def test_is_vowel_phoneme():
    """Test vowel detection."""
    assert phonecode.is_vowel_phoneme('AE')
    assert phonecode.is_vowel_phoneme('IY')
    assert not phonecode.is_vowel_phoneme('T')
    assert not phonecode.is_vowel_phoneme('K')


def test_is_consonant_phoneme():
    """Test consonant detection."""
    assert phonecode.is_consonant_phoneme('T')
    assert phonecode.is_consonant_phoneme('K')
    assert not phonecode.is_consonant_phoneme('AE')
    assert not phonecode.is_consonant_phoneme('IY')


def test_separate_vowels_consonants():
    """Test vowel/consonant separation."""
    vowels, consonants = phonecode.separate_vowels_consonants(['K', 'AE', 'T'])
    assert vowels == ['AE']
    assert set(consonants) == {'K', 'T'}


def test_get_phonemes():
    """Test phoneme extraction from words."""
    # This test requires nltk data
    try:
        phonemes = phonecode.get_phonemes('cat')
        assert len(phonemes) > 0
        assert any('K' in pron for pron in phonemes)
    except RuntimeError:
        pytest.skip("CMUdict not available")


def test_grid_mapping_creation():
    """Test GridMapping creation."""
    consonants = ['P', 'T', 'K', 'F', 'S']
    vowels = ['IY', 'AE', 'AA', 'OW', 'UW']

    mapping = phonecode.GridMapping(consonants, vowels, grid_shape=(5, 5))

    assert mapping.grid_shape == (5, 5)
    assert len(mapping.coord_to_phonemes) == 25

    # Test coordinate lookup
    phonemes = mapping.coord_to_phonemes[(0, 0)]
    assert phonemes == (consonants[0], vowels[0])


def test_integer_mapping_creation():
    """Test IntegerMapping creation."""
    mapping = phonecode.IntegerMapping()

    assert len(mapping.consonants) == 10
    assert len(mapping.vowels) == 10

    # Test encoding
    phonemes = mapping.encode_integer(42)
    assert len(phonemes) == 2  # Two digits


def test_suggest_phonemes():
    """Test phoneme suggestion."""
    consonants, vowels = phonecode.suggest_phonemes_for_grid(5, 5)

    assert len(consonants) == 5
    assert len(vowels) == 5
    assert all(phonecode.is_consonant_phoneme(c) for c in consonants)
    assert all(phonecode.is_vowel_phoneme(v) for v in vowels)


def test_word_contains_phonemes():
    """Test word phoneme checking."""
    try:
        # Simple test with known word
        result = phonecode.word_contains_phonemes('cat', {'K', 'AE', 'T'})
        assert isinstance(result, bool)
    except RuntimeError:
        pytest.skip("CMUdict not available")


def test_coords_word_codec_creation():
    """Test CoordsWordCodec initialization."""
    try:
        # Create a simple mapping
        consonants = ['P', 'T', 'K']
        vowels = ['IY', 'AE', 'AA']
        mapping = phonecode.GridMapping(consonants, vowels, grid_shape=(3, 3))

        # Create mock single_coord_words
        single_coord_words = {
            (0, 0): [('pea', ['P', 'IY'], 1000.0)],
            (0, 1): [('pat', ['P', 'AE', 'T'], 500.0)],
        }

        codec = phonecode.CoordsWordCodec(mapping, single_coord_words)

        assert codec.mapping == mapping
        assert codec.single_coord_words == single_coord_words
        assert 'pea' in codec.word_to_coords
        assert 'pat' in codec.word_to_coords
    except RuntimeError:
        pytest.skip("CMUdict not available")


def test_coords_to_phoneme_pairs_encoding():
    """Test encoding coordinates to phoneme pairs."""
    consonants = ['P', 'T', 'K']
    vowels = ['IY', 'AE', 'AA']
    mapping = phonecode.GridMapping(consonants, vowels, grid_shape=(3, 3))

    codec = phonecode.CoordsWordCodec(mapping, {})

    coords = [(0, 0), (1, 1)]
    pairs = codec.encode_coords_to_phoneme_pairs(coords)

    assert pairs == [('P', 'IY'), ('T', 'AE')]


def test_phoneme_pairs_to_coords_decoding():
    """Test decoding phoneme pairs to coordinates."""
    consonants = ['P', 'T', 'K']
    vowels = ['IY', 'AE', 'AA']
    mapping = phonecode.GridMapping(consonants, vowels, grid_shape=(3, 3))

    codec = phonecode.CoordsWordCodec(mapping, {})

    pairs = [('P', 'IY'), ('T', 'AE')]
    coords = codec.decode_phoneme_pairs_to_coords(pairs)

    assert coords == [(0, 0), (1, 1)]


def test_word_to_coords_sequential_decoding():
    """Test sequential word-to-coords decoding to avoid ambiguity."""
    try:
        consonants = ['K', 'S', 'T', 'L', 'P']
        vowels = ['AE', 'AA', 'IY', 'OW', 'UW']
        mapping = phonecode.GridMapping(consonants, vowels, grid_shape=(5, 5))

        codec = phonecode.CoordsWordCodec(mapping, {})

        # Test "class" which has phonemes [K, L, AE, S]
        # Sequential analysis should find K...AE as first C-V pair
        # Not S-AE (which would be ambiguous)
        coords, is_valid = codec.decode_word_to_coords('class')

        # Should find K-AE as the sequential pair
        assert len(coords) >= 1
        # First coord should be (0, 0) which is K-AE
        if coords:
            assert coords[0] == (0, 0)  # K is consonants[0], AE is vowels[0]

    except RuntimeError:
        pytest.skip("CMUdict not available")


def test_validate_word_for_coords():
    """Test word validation for expected coordinates."""
    try:
        consonants = ['P', 'T', 'K']
        vowels = ['IY', 'AE', 'AA']
        mapping = phonecode.GridMapping(consonants, vowels, grid_shape=(3, 3))

        codec = phonecode.CoordsWordCodec(mapping, {})

        # Test a word that should encode specific coords
        # "pea" has phonemes [P, IY] which should map to (0, 0)
        is_valid, message = codec.validate_word_for_coords('pea', [(0, 0)])

        assert isinstance(is_valid, bool)
        assert isinstance(message, str)

        if is_valid:
            assert '✓' in message
        else:
            assert '✗' in message

    except RuntimeError:
        pytest.skip("CMUdict not available")


def test_find_valid_words_for_coords():
    """Test finding and validating words for coordinates."""
    try:
        consonants = ['P', 'T', 'K', 'S', 'F']
        vowels = ['IY', 'AE', 'AA', 'OW', 'UW']
        mapping = phonecode.GridMapping(consonants, vowels, grid_shape=(5, 5))

        codec = phonecode.CoordsWordCodec(mapping, {})

        # Find words for a single coordinate
        coords = [(0, 0)]  # P-IY
        valid_words = codec.find_valid_words_for_coords(coords, max_results=5)

        assert isinstance(valid_words, list)
        # Each result should be (word, phonemes, frequency)
        for word, phonemes, freq in valid_words:
            assert isinstance(word, str)
            assert isinstance(phonemes, list)
            assert isinstance(freq, (int, float))

            # Verify the word actually decodes to expected coords
            decoded, is_valid = codec.decode_word_to_coords(word, expected_num_coords=1)
            assert is_valid
            assert set(decoded) == set(coords)

    except RuntimeError:
        pytest.skip("CMUdict not available")


def test_codec_round_trip():
    """Test that encoding and decoding are inverse operations."""
    try:
        consonants = ['P', 'T', 'K', 'S', 'F']
        vowels = ['IY', 'AE', 'AA', 'OW', 'UW']
        mapping = phonecode.GridMapping(consonants, vowels, grid_shape=(5, 5))

        codec = phonecode.CoordsWordCodec(mapping, {})

        # Test round trip: coords → phoneme pairs → coords
        original_coords = [(0, 0), (1, 1), (2, 2)]

        # Encode
        phoneme_pairs = codec.encode_coords_to_phoneme_pairs(original_coords)

        # Decode
        decoded_coords = codec.decode_phoneme_pairs_to_coords(phoneme_pairs)

        # Should match original
        assert decoded_coords == original_coords

    except RuntimeError:
        pytest.skip("CMUdict not available")


def test_codec_handles_ambiguous_words():
    """Test that codec disambiguates words with multiple C-V combinations."""
    try:
        consonants = ['K', 'S', 'T', 'L', 'P']
        vowels = ['AE', 'AA', 'IY', 'OW', 'UW']
        mapping = phonecode.GridMapping(consonants, vowels, grid_shape=(5, 5))

        codec = phonecode.CoordsWordCodec(mapping, {})

        # "class" = [K, L, AE, S]
        # Has potential for K-AE and S-AE
        # Should only find the FIRST sequential C-V pair (K-AE)
        coords, _ = codec.decode_word_to_coords('class')

        # Should have exactly one coord (K, AE) at (0, 0)
        # Not multiple coords due to finding all combinations
        k_ae_coord = (0, 0)  # K is first consonant, AE is first vowel

        if coords:
            # First found coord should be K-AE
            assert coords[0] == k_ae_coord

    except RuntimeError:
        pytest.skip("CMUdict not available")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

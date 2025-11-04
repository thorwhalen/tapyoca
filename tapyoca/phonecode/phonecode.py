"""
Phoneme-based encoding and decoding tools.

This module provides tools for creating mappings between discrete multidimensional spaces,
with one space being the phoneme space. Supports applications like:
- Encoding grid positions (e.g., 5x5 Codenames grid) into words
- Encoding integers as pronounceable words
- Finding words that contain specific phoneme combinations

Installation Requirements:
    pip install nltk

First-time setup:
    import phonecode
    phonecode.download_required_data()  # Downloads CMUdict and frequency data
"""

from typing import Dict, List, Set, Tuple, Optional, Iterable, Callable
from collections import defaultdict, Counter
from itertools import combinations, product
from pathlib import Path
import re
import urllib.request
import json


# ============================================================================
# Data Management
# ============================================================================


def download_required_data(force: bool = False) -> None:
    """
    Download required data for phonecode module.

    Downloads:
    - CMU Pronouncing Dictionary (via nltk)
    - Word frequency list

    Args:
        force: If True, re-download even if data exists

    >>> # download_required_data()  # Uncomment to run
    """
    import nltk

    print("Downloading CMU Pronouncing Dictionary...")
    try:
        nltk.data.find('corpora/cmudict')
        if not force:
            print("  CMUdict already downloaded.")
        else:
            nltk.download('cmudict', quiet=False)
    except LookupError:
        nltk.download('cmudict', quiet=False)

    print("\nDownloading word frequency data...")
    freq_file = Path.home() / '.phonecode' / 'word_freq.json'
    freq_file.parent.mkdir(exist_ok=True)

    if freq_file.exists() and not force:
        print("  Word frequency data already downloaded.")
        return

    # Download from a reliable source (COCA word frequency list)
    url = "https://raw.githubusercontent.com/hackerb9/gwordlist/master/frequency-alpha-alldicts.txt"

    try:
        print(f"  Downloading from {url}...")
        response = urllib.request.urlopen(url)
        lines = response.read().decode('utf-8').split('\n')

        freq_dict = {}
        for line in lines[1:50001]:  # Skip header, get top 50k words
            if line.strip() and not line.startswith('#'):
                parts = line.split()
                if len(parts) >= 3:
                    # Format: RANK WORD COUNT ...
                    # Get word from second column
                    word = parts[1].lower()
                    try:
                        # Count is in third column, remove commas
                        count_str = parts[2].replace(',', '')
                        freq = float(count_str)
                        freq_dict[word] = freq
                    except (ValueError, IndexError):
                        continue

        with open(freq_file, 'w') as f:
            json.dump(freq_dict, f)

        print(f"  Downloaded frequency data for {len(freq_dict)} words.")

    except Exception as e:
        print(f"  Warning: Could not download frequency data: {e}")
        print("  Module will work but without frequency information.")


def _load_cmudict() -> Dict[str, List[List[str]]]:
    """
    Load CMU Pronouncing Dictionary.

    Returns:
        Dictionary mapping words to lists of phoneme sequences
    """
    try:
        from nltk.corpus import cmudict

        return cmudict.dict()
    except LookupError:
        raise RuntimeError(
            "CMUdict not found. Please run: phonecode.download_required_data()"
        )


def _load_word_frequencies() -> Dict[str, float]:
    """
    Load word frequency data.

    Returns:
        Dictionary mapping words to frequency scores
    """
    freq_file = Path.home() / '.phonecode' / 'word_freq.json'

    if not freq_file.exists():
        return {}

    try:
        with open(freq_file, 'r') as f:
            return json.load(f)
    except Exception:
        return {}


# Global caches
_CMUDICT_CACHE = None
_FREQ_CACHE = None


def get_cmudict() -> Dict[str, List[List[str]]]:
    """Get cached CMU dictionary."""
    global _CMUDICT_CACHE
    if _CMUDICT_CACHE is None:
        _CMUDICT_CACHE = _load_cmudict()
    return _CMUDICT_CACHE


def get_word_frequencies() -> Dict[str, float]:
    """Get cached word frequency data."""
    global _FREQ_CACHE
    if _FREQ_CACHE is None:
        _FREQ_CACHE = _load_word_frequencies()
    return _FREQ_CACHE


# ============================================================================
# Phoneme Processing
# ============================================================================


def strip_stress(phoneme: str) -> str:
    """
    Remove stress markers from phoneme.

    >>> strip_stress('AE1')
    'AE'
    >>> strip_stress('T')
    'T'
    """
    return re.sub(r'\d', '', phoneme)


def get_phonemes(word: str) -> List[List[str]]:
    """
    Get phoneme transcriptions for a word.

    Args:
        word: Word to transcribe

    Returns:
        List of possible phoneme sequences (handles multiple pronunciations)

    >>> phonemes = get_phonemes('cat')
    >>> len(phonemes) > 0
    True
    """
    cmudict = get_cmudict()
    word_lower = word.lower()

    if word_lower not in cmudict:
        return []

    # Strip stress markers
    return [[strip_stress(p) for p in pron] for pron in cmudict[word_lower]]


def word_contains_phonemes(
    word: str, required_phonemes: Set[str], any_order: bool = True
) -> bool:
    """
    Check if word contains all required phonemes.

    Args:
        word: Word to check
        required_phonemes: Set of phonemes that must be present
        any_order: If True, phonemes can appear in any order

    Returns:
        True if word contains all required phonemes

    >>> word_contains_phonemes('cat', {'K', 'AE', 'T'})
    True
    >>> word_contains_phonemes('cat', {'K', 'IY'})
    False
    """
    pronunciations = get_phonemes(word)

    for pron in pronunciations:
        pron_set = set(pron)
        if required_phonemes.issubset(pron_set):
            return True

    return False


def is_vowel_phoneme(phoneme: str) -> bool:
    """
    Check if phoneme is a vowel.

    >>> is_vowel_phoneme('AE')
    True
    >>> is_vowel_phoneme('T')
    False
    """
    # Vowels in CMUdict are represented with letters only (consonants may have digits)
    # Actually, both can have digits for stress, so we check the base
    vowels = {
        'AA',
        'AE',
        'AH',
        'AO',
        'AW',
        'AY',
        'EH',
        'ER',
        'EY',
        'IH',
        'IY',
        'OW',
        'OY',
        'UH',
        'UW',
    }
    return strip_stress(phoneme) in vowels


def is_consonant_phoneme(phoneme: str) -> bool:
    """
    Check if phoneme is a consonant.

    >>> is_consonant_phoneme('T')
    True
    >>> is_consonant_phoneme('AE')
    False
    """
    return not is_vowel_phoneme(phoneme)


def separate_vowels_consonants(phonemes: List[str]) -> Tuple[List[str], List[str]]:
    """
    Separate phoneme list into vowels and consonants.

    >>> separate_vowels_consonants(['K', 'AE', 'T'])
    (['AE'], ['K', 'T'])
    """
    vowels = [p for p in phonemes if is_vowel_phoneme(p)]
    consonants = [p for p in phonemes if is_consonant_phoneme(p)]
    return vowels, consonants


# ============================================================================
# Word Search
# ============================================================================


def find_words_with_phonemes(
    required_phonemes: Set[str],
    *,
    max_results: int = 100,
    min_word_length: int = 3,
    max_word_length: int = 15,
    sort_by_frequency: bool = True,
    common_only: bool = False,
) -> List[Tuple[str, List[str], float]]:
    """
    Find words containing all required phonemes.

    Args:
        required_phonemes: Set of phonemes that must be present
        max_results: Maximum number of results to return
        min_word_length: Minimum word length
        max_word_length: Maximum word length
        sort_by_frequency: Sort results by word frequency
        common_only: Only include words in top 50k frequency list

    Returns:
        List of (word, phonemes, frequency) tuples

    >>> results = find_words_with_phonemes({'K', 'AE', 'T'}, max_results=5, common_only=False)  # doctest: +SKIP
    >>> any('cat' in word for word, _, _ in results)  # doctest: +SKIP
    True
    """
    cmudict = get_cmudict()
    freq_dict = get_word_frequencies()

    results = []

    for word, pronunciations in cmudict.items():
        # Filter by length
        if not (min_word_length <= len(word) <= max_word_length):
            continue

        # Filter by common words if requested
        if common_only and word not in freq_dict:
            continue

        # Check each pronunciation
        for pron in pronunciations:
            pron_stripped = [strip_stress(p) for p in pron]
            pron_set = set(pron_stripped)

            if required_phonemes.issubset(pron_set):
                freq = freq_dict.get(word, 0.0)
                results.append((word, pron_stripped, freq))
                break  # Only add word once even if multiple pronunciations match

    # Sort by frequency if requested
    if sort_by_frequency:
        results.sort(key=lambda x: x[2], reverse=True)
    else:
        results.sort(key=lambda x: x[0])  # Alphabetical

    return results[:max_results]


def find_words_for_phoneme_pairs(
    phoneme_pairs: List[Tuple[str, str]], **kwargs
) -> Dict[Tuple[str, str], List[Tuple[str, List[str], float]]]:
    """
    Find words for each phoneme pair (typically consonant-vowel or vowel-consonant).

    Args:
        phoneme_pairs: List of (consonant, vowel) or (vowel, consonant) pairs
        **kwargs: Additional arguments passed to find_words_with_phonemes

    Returns:
        Dictionary mapping each pair to list of matching words

    >>> pairs = [('K', 'AE'), ('T', 'IY')]
    >>> results = find_words_for_phoneme_pairs(pairs, max_results=3)
    >>> len(results) == 2
    True
    """
    results = {}

    for pair in phoneme_pairs:
        required = set(pair)
        words = find_words_with_phonemes(required, **kwargs)
        results[pair] = words

    return results


def find_multi_pair_words(
    phoneme_pairs: List[Tuple[str, str]], num_pairs: int = 2, **kwargs
) -> Dict[Tuple[Tuple[str, str], ...], List[Tuple[str, List[str], float]]]:
    """
    Find words that satisfy multiple phoneme pairs simultaneously.

    This is useful for encoding multiple grid positions in a single word.

    Args:
        phoneme_pairs: List of available phoneme pairs
        num_pairs: Number of pairs to combine
        **kwargs: Additional arguments passed to find_words_with_phonemes

    Returns:
        Dictionary mapping pair combinations to matching words

    >>> pairs = [('K', 'AE'), ('T', 'IY'), ('S', 'UW')]
    >>> results = find_multi_pair_words(pairs, num_pairs=2, max_results=2)
    >>> isinstance(results, dict)
    True
    """
    results = {}

    for pair_combo in combinations(phoneme_pairs, num_pairs):
        # Flatten all phonemes from the pairs
        required = set()
        for pair in pair_combo:
            required.update(pair)

        words = find_words_with_phonemes(required, **kwargs)
        if words:  # Only include if at least one word found
            results[pair_combo] = words

    return results


# ============================================================================
# Mapping Creation
# ============================================================================


class PhonemeMapping:
    """
    Base class for phoneme-based encoding mappings.

    Provides methods to encode/decode between a target space and phoneme space.
    """

    def __init__(
        self, phoneme_to_target: Dict[str, any], target_to_phoneme: Dict[any, str]
    ):
        """
        Initialize mapping.

        Args:
            phoneme_to_target: Maps phonemes to target space elements
            target_to_phoneme: Maps target space elements to phonemes
        """
        self.phoneme_to_target = phoneme_to_target
        self.target_to_phoneme = target_to_phoneme

    def encode_word(self, word: str) -> List[any]:
        """
        Decode word into target space elements.

        >>> # Example usage with custom mapping
        """
        pronunciations = get_phonemes(word)

        if not pronunciations:
            return []

        # Use first pronunciation
        phonemes = pronunciations[0]

        targets = []
        for phoneme in phonemes:
            if phoneme in self.phoneme_to_target:
                targets.append(self.phoneme_to_target[phoneme])

        return targets

    def decode_target(self, target: any) -> Optional[str]:
        """Get phoneme for a target element."""
        return self.target_to_phoneme.get(target)


class GridMapping(PhonemeMapping):
    """
    Mapping for 2D grid positions.

    Maps (consonant, vowel) pairs to (row, col) coordinates.
    """

    def __init__(
        self,
        consonants: List[str],
        vowels: List[str],
        grid_shape: Tuple[int, int] = (5, 5),
    ):
        """
        Initialize grid mapping.

        Args:
            consonants: List of consonant phonemes for rows
            vowels: List of vowel phonemes for columns
            grid_shape: Shape of grid (rows, cols)
        """
        self.consonants = consonants
        self.vowels = vowels
        self.grid_shape = grid_shape

        # Create mappings
        phoneme_to_target = {}
        target_to_phoneme = {}

        # Map consonants to rows (cycling if needed)
        for i in range(grid_shape[0]):
            c = consonants[i % len(consonants)]
            phoneme_to_target[c] = ('row', i)
            if ('row', i) not in target_to_phoneme:
                target_to_phoneme[('row', i)] = c

        # Map vowels to columns (cycling if needed)
        for j in range(grid_shape[1]):
            v = vowels[j % len(vowels)]
            phoneme_to_target[v] = ('col', j)
            if ('col', j) not in target_to_phoneme:
                target_to_phoneme[('col', j)] = v

        super().__init__(phoneme_to_target, target_to_phoneme)

        # Create coordinate mappings
        self.coord_to_phonemes = {}
        self.phonemes_to_coord = {}

        for i in range(grid_shape[0]):
            for j in range(grid_shape[1]):
                c = consonants[i % len(consonants)]
                v = vowels[j % len(vowels)]
                self.coord_to_phonemes[(i, j)] = (c, v)
                # Allow lookup by either order
                self.phonemes_to_coord[(c, v)] = (i, j)
                self.phonemes_to_coord[(v, c)] = (i, j)

    def decode_word_to_coords(self, word: str) -> List[Tuple[int, int]]:
        """
        Decode word to grid coordinates.

        Finds all (consonant, vowel) pairs in word and maps to coordinates.

        >>> # Example with specific mapping
        """
        pronunciations = get_phonemes(word)

        if not pronunciations:
            return []

        phonemes = pronunciations[0]
        vowels, consonants = separate_vowels_consonants(phonemes)

        coords = []

        # Try to find consonant-vowel pairs
        c_set = set(consonants)
        v_set = set(vowels)

        # Check all possible C-V combinations present in word
        for c in c_set:
            for v in v_set:
                if (c, v) in self.phonemes_to_coord:
                    coords.append(self.phonemes_to_coord[(c, v)])

        return list(set(coords))  # Remove duplicates

    def encode_coords(self, coords: List[Tuple[int, int]]) -> Set[str]:
        """
        Get required phonemes for encoding coordinates.

        >>> # Example with specific mapping
        """
        phonemes = set()
        for coord in coords:
            if coord in self.coord_to_phonemes:
                phonemes.update(self.coord_to_phonemes[coord])
        return phonemes


class IntegerMapping(PhonemeMapping):
    """
    Mapping for integers to pronounceable words.

    Uses consonant-vowel alternation to create pronounceable digit sequences.
    """

    def __init__(self, consonants: List[str] = None, vowels: List[str] = None):
        """
        Initialize integer mapping.

        Args:
            consonants: List of 10 consonants for digits 0-9
            vowels: List of 10 vowels for digits 0-9 (in alternate positions)
        """
        if consonants is None:
            # Default: use common distinct consonants
            consonants = ['S', 'T', 'N', 'R', 'L', 'K', 'M', 'P', 'D', 'B']

        if vowels is None:
            # Default: use distinct vowels
            vowels = ['IY', 'AE', 'AA', 'AO', 'UW', 'EH', 'IH', 'AH', 'OW', 'ER']

        assert len(consonants) == 10, "Need exactly 10 consonants"
        assert len(vowels) == 10, "Need exactly 10 vowels"

        self.consonants = consonants
        self.vowels = vowels

        # Create digit mappings
        phoneme_to_target = {}
        target_to_phoneme = {}

        for i, c in enumerate(consonants):
            phoneme_to_target[c] = ('digit_c', i)
            target_to_phoneme[('digit_c', i)] = c

        for i, v in enumerate(vowels):
            phoneme_to_target[v] = ('digit_v', i)
            target_to_phoneme[('digit_v', i)] = v

        super().__init__(phoneme_to_target, target_to_phoneme)

    def encode_integer(self, n: int, use_consonants_first: bool = True) -> List[str]:
        """
        Encode integer as phoneme sequence.

        Args:
            n: Integer to encode
            use_consonants_first: If True, odd positions use consonants

        Returns:
            List of phonemes representing the integer

        >>> # Example with specific mapping
        """
        digits = [int(d) for d in str(n)]
        phonemes = []

        for i, digit in enumerate(digits):
            if (i % 2 == 0) == use_consonants_first:
                phonemes.append(self.consonants[digit])
            else:
                phonemes.append(self.vowels[digit])

        return phonemes

    def decode_word_to_integer(
        self, word: str, use_consonants_first: bool = True
    ) -> Optional[int]:
        """
        Decode word to integer.

        >>> # Example with specific mapping
        """
        pronunciations = get_phonemes(word)

        if not pronunciations:
            return None

        phonemes = pronunciations[0]
        digits = []

        for i, phoneme in enumerate(phonemes):
            if (i % 2 == 0) == use_consonants_first:
                # Expect consonant
                if phoneme in self.consonants:
                    digits.append(self.consonants.index(phoneme))
                else:
                    return None
            else:
                # Expect vowel
                if phoneme in self.vowels:
                    digits.append(self.vowels.index(phoneme))
                else:
                    return None

        return int(''.join(map(str, digits)))


# ============================================================================
# High-Level Interface Functions
# ============================================================================


def create_5x5_codenames_mapping(
    consonants: List[str] = None,
    vowels: List[str] = None,
    words_per_coord: int = 1,
    check_multi_coord: bool = True,
    max_multi_coord: int = 2,
) -> Dict:
    """
    Create a complete mapping for 5x5 Codenames grid.

    Args:
        consonants: List of 5-10 consonants (uses voicing pairs if None)
        vowels: List of 5 vowels (uses distinct vowels if None)
        words_per_coord: Number of example words to find per coordinate
        check_multi_coord: Whether to search for multi-coordinate words
        max_multi_coord: Maximum number of coordinates to combine

    Returns:
        Dictionary containing:
        - 'mapping': GridMapping object
        - 'single_coord_words': Words for each coordinate
        - 'multi_coord_words': Words encoding multiple coordinates (if checked)
        - 'statistics': Coverage statistics

    >>> result = create_5x5_codenames_mapping(words_per_coord=2, check_multi_coord=False)  # doctest: +ELLIPSIS
    Finding words for single coordinates...
    Coverage: .../25 coordinates have at least one word
    >>> 'mapping' in result
    True
    >>> 'single_coord_words' in result
    True
    """
    # Default phonemes
    if consonants is None:
        # Use 5 voicing pairs = 10 consonants, but only use 5 for 5x5 grid
        consonants = ['P', 'T', 'K', 'F', 'S']  # Voiceless
        # Could extend to ['P', 'B', 'T', 'D', 'K', 'G', 'F', 'V', 'S', 'Z']

    if vowels is None:
        # 5 maximally distinct vowels
        vowels = ['IY', 'AE', 'AA', 'OW', 'UW']

    # Create mapping
    mapping = GridMapping(consonants, vowels, grid_shape=(5, 5))

    # Find words for each coordinate
    print("Finding words for single coordinates...")
    single_coord_words = {}

    all_coords = [(i, j) for i in range(5) for j in range(5)]

    for coord in all_coords:
        required = mapping.encode_coords([coord])
        words = find_words_with_phonemes(
            required,
            max_results=words_per_coord,
            common_only=True,
            sort_by_frequency=True,
        )
        single_coord_words[coord] = words

    # Check coverage
    covered = sum(1 for words in single_coord_words.values() if words)
    print(f"Coverage: {covered}/25 coordinates have at least one word")

    result = {
        'mapping': mapping,
        'consonants': consonants,
        'vowels': vowels,
        'single_coord_words': single_coord_words,
        'statistics': {
            'total_coords': 25,
            'covered_coords': covered,
            'coverage_percent': covered / 25 * 100,
        },
    }

    # Find multi-coordinate words if requested
    if check_multi_coord:
        print(f"\nSearching for words encoding multiple coordinates...")

        # Get all phoneme pairs
        all_pairs = [mapping.coord_to_phonemes[coord] for coord in all_coords]

        multi_coord_words = {}

        for n in range(2, max_multi_coord + 1):
            print(f"  Checking {n}-coordinate combinations...")
            results = find_multi_pair_words(
                all_pairs, num_pairs=n, max_results=5, common_only=True
            )

            if results:
                print(f"    Found words for {len(results)} combinations")
                multi_coord_words[n] = results

        result['multi_coord_words'] = multi_coord_words

    return result


def create_integer_encoding_mapping(
    max_integer: int = 999,
    consonants: List[str] = None,
    vowels: List[str] = None,
    examples_per_length: int = 5,
) -> Dict:
    """
    Create mapping for encoding integers as pronounceable words.

    Args:
        max_integer: Maximum integer to support (determines digit length)
        consonants: List of 10 consonants for digits 0-9
        vowels: List of 10 vowels for digits 0-9
        examples_per_length: Number of example words to find per digit length

    Returns:
        Dictionary containing:
        - 'mapping': IntegerMapping object
        - 'example_words': Example words for different digit lengths
        - 'phoneme_patterns': Phoneme patterns for each digit length

    >>> result = create_integer_encoding_mapping(max_integer=99, examples_per_length=2)  # doctest: +ELLIPSIS
    Creating integer encoding for up to 2 digits...
    Consonants (0-9): ...
    Vowels (0-9): ...
    <BLANKLINE>
    Finding words for 1-digit numbers...
    <BLANKLINE>
    Finding words for 2-digit numbers...
    >>> 'mapping' in result
    True
    """
    # Create mapping
    mapping = IntegerMapping(consonants, vowels)

    # Determine max digits needed
    max_digits = len(str(max_integer))

    print(f"Creating integer encoding for up to {max_digits} digits...")
    print(f"Consonants (0-9): {mapping.consonants}")
    print(f"Vowels (0-9): {mapping.vowels}")

    # Generate example patterns and find words
    example_words = {}
    phoneme_patterns = {}

    for num_digits in range(1, max_digits + 1):
        print(f"\nFinding words for {num_digits}-digit numbers...")

        # Generate some example numbers
        example_numbers = []
        if num_digits == 1:
            example_numbers = list(range(10))
        elif num_digits == 2:
            example_numbers = [0, 11, 22, 50, 99]
        else:
            example_numbers = [0, 111, 500, 10**num_digits - 1]

        patterns = {}
        for num in example_numbers[:examples_per_length]:
            if num >= 10**num_digits:
                continue

            # Pad with zeros if needed
            num_str = str(num).zfill(num_digits)
            phonemes = mapping.encode_integer(int(num_str))

            # Find words with this pattern
            required = set(phonemes)
            words = find_words_with_phonemes(
                required,
                max_results=3,
                common_only=True,
                min_word_length=num_digits,
                max_word_length=num_digits + 3,
            )

            patterns[num] = {'phonemes': phonemes, 'words': words}

        example_words[num_digits] = patterns
        phoneme_patterns[num_digits] = [
            mapping.encode_integer(i) for i in range(min(10, 10**num_digits))
        ]

    return {
        'mapping': mapping,
        'consonants': mapping.consonants,
        'vowels': mapping.vowels,
        'max_integer': max_integer,
        'max_digits': max_digits,
        'example_words': example_words,
        'phoneme_patterns': phoneme_patterns,
    }


def print_5x5_results(results: Dict, show_multi: bool = True) -> None:
    """
    Pretty-print results from create_5x5_codenames_mapping.

    >>> results = create_5x5_codenames_mapping(words_per_coord=1, check_multi_coord=False)  # doctest: +SKIP
    >>> print_5x5_results(results, show_multi=False)  # doctest: +SKIP
    """
    print("\n" + "=" * 70)
    print("5×5 CODENAMES MAPPING")
    print("=" * 70)

    mapping = results['mapping']
    consonants = results['consonants']
    vowels = results['vowels']

    print(f"\nPhoneme Assignments:")
    print(f"  Rows (consonants): {consonants}")
    print(f"  Cols (vowels): {vowels}")

    print(f"\nCoverage: {results['statistics']['coverage_percent']:.1f}%")
    print(f"  {results['statistics']['covered_coords']}/25 coordinates have words")

    print("\n" + "-" * 70)
    print("GRID WITH EXAMPLE WORDS")
    print("-" * 70)

    # Print grid header
    print(f"\n{'':5}", end='')
    for j, v in enumerate(vowels[:5]):
        print(f"{v:12}", end='')
    print()
    print(f"{'':5}" + "-" * 60)

    # Print each row
    for i in range(5):
        c = consonants[i]
        print(f"{c:5}", end='')

        for j in range(5):
            coord = (i, j)
            words = results['single_coord_words'].get(coord, [])

            if words:
                word = words[0][0]  # First word
                print(f"{word:12}", end='')
            else:
                print(f"{'---':12}", end='')
        print()

    if show_multi and 'multi_coord_words' in results:
        print("\n" + "-" * 70)
        print("MULTI-COORDINATE WORDS")
        print("-" * 70)

        for n, combos in sorted(results['multi_coord_words'].items()):
            print(f"\n{n}-coordinate combinations: {len(combos)} found")

            # Show a few examples
            for combo, words in list(combos.items())[:3]:
                coords = [mapping.phonemes_to_coord[pair] for pair in combo]
                word_list = [w[0] for w in words[:2]]
                print(f"  {coords}: {', '.join(word_list)}")


def print_integer_results(results: Dict) -> None:
    """
    Pretty-print results from create_integer_encoding_mapping.

    >>> results = create_integer_encoding_mapping(max_integer=99, examples_per_length=1)  # doctest: +SKIP
    >>> print_integer_results(results)  # doctest: +SKIP
    """
    print("\n" + "=" * 70)
    print("INTEGER ENCODING MAPPING")
    print("=" * 70)

    print(f"\nDigit Assignments:")
    print(f"  Consonants: {results['consonants']}")
    print(f"  Vowels: {results['vowels']}")
    print(
        f"\nSupports integers up to {results['max_integer']} ({results['max_digits']} digits)"
    )

    print("\n" + "-" * 70)
    print("EXAMPLE ENCODINGS")
    print("-" * 70)

    for num_digits, patterns in sorted(results['example_words'].items()):
        print(f"\n{num_digits}-digit numbers:")

        for num, info in sorted(patterns.items()):
            phonemes_str = '-'.join(info['phonemes'])
            words = info['words']

            if words:
                word_list = ', '.join(w[0] for w in words[:3])
                print(f"  {num:3d} → {phonemes_str:20} | {word_list}")
            else:
                print(f"  {num:3d} → {phonemes_str:20} | (no common words found)")


# ============================================================================
# Utility Functions
# ============================================================================


def analyze_phoneme_coverage(words: Iterable[str]) -> Dict[str, int]:
    """
    Analyze which phonemes appear in a word list.

    >>> words = ['cat', 'dog', 'fish']
    >>> coverage = analyze_phoneme_coverage(words)
    >>> isinstance(coverage, dict)
    True
    """
    phoneme_counts = Counter()

    for word in words:
        pronunciations = get_phonemes(word)
        if pronunciations:
            for phoneme in pronunciations[0]:
                phoneme_counts[phoneme] += 1

    return dict(phoneme_counts)


def suggest_phonemes_for_grid(
    num_consonants: int = 5, num_vowels: int = 5
) -> Tuple[List[str], List[str]]:
    """
    Suggest optimal phonemes for grid encoding based on frequency and distinctiveness.

    >>> consonants, vowels = suggest_phonemes_for_grid(5, 5)
    >>> len(consonants) == 5
    True
    >>> len(vowels) == 5
    True
    """
    # High-frequency, distinct consonants
    best_consonants = ['T', 'S', 'R', 'N', 'D', 'L', 'K', 'M', 'P', 'B', 'F', 'V']

    # High-frequency, distinct vowels
    best_vowels = ['IY', 'AE', 'AA', 'OW', 'UW', 'EH', 'IH', 'AH', 'ER', 'AO']

    return best_consonants[:num_consonants], best_vowels[:num_vowels]


# ============================================================================
# Codec for Unambiguous Word-to-Coords Encoding/Decoding
# ============================================================================


class CoordsWordCodec:
    """
    Unambiguous codec for encoding/decoding between coordinates and words.

    Uses SEQUENTIAL consonant-vowel pairs to avoid ambiguity.
    Example: "class" has phonemes [K, L, AE, S]
             Sequential analysis: K...AE is the first C-V sequence → (K, AE)
             Avoids ambiguity of finding all C-V combinations
    """

    def __init__(self, mapping: GridMapping, single_coord_words: Dict):
        """
        Initialize codec with a mapping and word database.

        Args:
            mapping: GridMapping object
            single_coord_words: Dict mapping coords to lists of (word, phonemes, freq)
        """
        self.mapping = mapping
        self.single_coord_words = single_coord_words

        # Build word-to-coords lookup (inverse mapping)
        self.word_to_coords = {}
        for coord, word_list in single_coord_words.items():
            for word, phonemes, freq in word_list:
                if word not in self.word_to_coords:
                    self.word_to_coords[word] = []
                expected_pair = mapping.coord_to_phonemes[coord]
                self.word_to_coords[word].append((coord, expected_pair))

    def encode_coords_to_phoneme_pairs(
        self, coords: List[Tuple[int, int]]
    ) -> List[Tuple[str, str]]:
        """
        Encode coordinates to phoneme pairs.

        >>> # Example: [(0, 0), (1, 2)] → [('P', 'IY'), ('T', 'AA')]
        """
        return [self.mapping.coord_to_phonemes[coord] for coord in coords]

    def decode_phoneme_pairs_to_coords(
        self, phoneme_pairs: List[Tuple[str, str]]
    ) -> List[Tuple[int, int]]:
        """Decode phoneme pairs to coordinates."""
        coords = []
        for pair in phoneme_pairs:
            if pair in self.mapping.phonemes_to_coord:
                coords.append(self.mapping.phonemes_to_coord[pair])
        return coords

    def decode_word_to_coords(
        self, word: str, expected_num_coords: Optional[int] = None
    ) -> Tuple[List[Tuple[int, int]], bool]:
        """
        Decode word to coordinates using SEQUENTIAL phoneme analysis.

        Args:
            word: Word to decode
            expected_num_coords: Optional expected number of coordinates

        Returns:
            (coords, is_valid): Decoded coordinates and validity flag
        """
        pronunciations = get_phonemes(word)
        if not pronunciations:
            return ([], False)

        phonemes = pronunciations[0]

        # Find sequential consonant-vowel pairs
        coords = []
        i = 0
        while i < len(phonemes):
            if is_consonant_phoneme(phonemes[i]):
                # Look for next vowel
                for j in range(i + 1, len(phonemes)):
                    if is_vowel_phoneme(phonemes[j]):
                        c, v = phonemes[i], phonemes[j]
                        pair = (c, v)
                        if pair in self.mapping.phonemes_to_coord:
                            coords.append(self.mapping.phonemes_to_coord[pair])
                            i = j + 1
                            break
                else:
                    i += 1
            else:
                i += 1

        is_valid = True
        if expected_num_coords is not None:
            is_valid = len(coords) == expected_num_coords

        return (coords, is_valid)

    def validate_word_for_coords(
        self, word: str, expected_coords: List[Tuple[int, int]]
    ) -> Tuple[bool, str]:
        """
        Validate that a word properly encodes the expected coordinates.

        Returns:
            (is_valid, message): Validation result and explanation
        """
        decoded_coords, _ = self.decode_word_to_coords(word)

        expected_set = set(expected_coords)
        decoded_set = set(decoded_coords)

        if decoded_set == expected_set:
            return (True, f"✓ '{word}' correctly encodes {expected_coords}")
        else:
            missing = expected_set - decoded_set
            extra = decoded_set - expected_set
            msg = f"✗ '{word}' validation failed:\n"
            msg += f"  Expected: {expected_coords}\n"
            msg += f"  Decoded:  {decoded_coords}\n"
            if missing:
                msg += f"  Missing:  {missing}\n"
            if extra:
                msg += f"  Extra:    {extra}"
            return (False, msg)

    def find_valid_words_for_coords(
        self, coords: List[Tuple[int, int]], max_results: int = 10
    ) -> List[Tuple[str, List[str], float]]:
        """
        Find words that unambiguously encode the given coordinates.

        Searches for candidates and validates them with sequential decoder.
        """
        required_phonemes = self.mapping.encode_coords(coords)

        candidates = find_words_with_phonemes(
            required_phonemes,
            max_results=max_results * 3,
            common_only=True,
            sort_by_frequency=True,
        )

        valid_words = []
        for word, prons, freq in candidates:
            decoded_coords, is_valid = self.decode_word_to_coords(word, len(coords))
            if is_valid and set(decoded_coords) == set(coords):
                valid_words.append((word, prons, freq))
                if len(valid_words) >= max_results:
                    break

        return valid_words


def print_coord_words_grid(result, max_words_per_cell=3):
    """
    Print single_coord_words in a readable grid format with stacked words.

    Args:
        result: Output from create_5x5_codenames_mapping
        max_words_per_cell: Maximum number of words to show per coordinate
    """
    mapping = result['mapping']
    single_coord_words = result['single_coord_words']
    consonants = result['consonants']
    vowels = result['vowels']

    col_width = 18

    # Header
    print("\n" + "=" * 100)
    print("WORD GRID (Consonant-Vowel Combinations)")
    print("=" * 100)
    print(f"\nConsonants (rows): {consonants}")
    print(f"Vowels (columns): {vowels}\n")

    # Column headers
    print(" " * 8, end="")
    for vowel in vowels:
        print(f"{vowel:^{col_width}}", end="")
    print("\n" + " " * 8 + "-" * (col_width * len(vowels)))

    # Grid rows - each row can be multiple lines tall
    for i, consonant in enumerate(consonants):
        # Collect all words for this row
        row_words = []
        max_height = 0

        for j in range(len(vowels)):
            coord = (i, j)
            words = single_coord_words.get(coord, [])
            word_list = [w[0] for w in words[:max_words_per_cell]] if words else ["---"]
            row_words.append(word_list)
            max_height = max(max_height, len(word_list))

        # Print this row line by line
        for line_num in range(max_height):
            if line_num == 0:
                print(f"{consonant:>6} |", end="")
            else:
                print(" " * 8, end="")

            for word_list in row_words:
                if line_num < len(word_list):
                    word = word_list[line_num]
                    # Truncate individual words if too long
                    if len(word) > col_width - 2:
                        word = word[: col_width - 4] + ".."
                else:
                    word = ""
                print(f"{word:^{col_width}}", end="")
            print()

        # Separator between rows
        if i < len(consonants) - 1:
            print(" " * 8 + "·" * (col_width * len(vowels)))

    # Statistics
    stats = result['statistics']
    print("\n" + "-" * 100)
    print(
        f"Coverage: {stats['covered_coords']}/{stats['total_coords']} coordinates "
        f"({stats['coverage_percent']:.1f}%)"
    )
    print("=" * 100)


def print_two_coord_words_table(result, max_words_per_combo=3, max_combos=50):
    """
    Print a table of 2-coordinate combinations and their words.

    Args:
        result: Output from create_5x5_codenames_mapping
        max_words_per_combo: Maximum words to show per coordinate pair
        max_combos: Maximum number of combinations to display
    """
    if 'multi_coord_words' not in result or 2 not in result['multi_coord_words']:
        print("No 2-coordinate words found. Run with check_multi_coord=True")
        return

    two_coord_words = result['multi_coord_words'][2]
    mapping = result['mapping']

    # Organize by coordinate pairs
    coord_pairs = []
    for phoneme_pair_set, words in two_coord_words.items():
        coords = tuple(
            sorted([mapping.phonemes_to_coord[pair] for pair in phoneme_pair_set])
        )
        phoneme_pairs = tuple(sorted(phoneme_pair_set))

        if words:  # Only include if there are words
            # Sort words by frequency
            sorted_words = sorted(words, key=lambda x: x[2], reverse=True)
            coord_pairs.append((coords, phoneme_pairs, sorted_words))

    # Sort by number of words (descending), then by frequency of best word
    coord_pairs.sort(key=lambda x: (len(x[2]), x[2][0][2] if x[2] else 0), reverse=True)

    # Print header
    print("\n" + "=" * 100)
    print("2-COORDINATE WORD COMBINATIONS")
    print("=" * 100)
    print(f"\nTotal combinations with words: {len(coord_pairs)}")
    print(f"Showing top {min(max_combos, len(coord_pairs))} combinations\n")
    print("-" * 100)

    # Print table
    for i, (coords, phoneme_pairs, words) in enumerate(coord_pairs[:max_combos], 1):
        # Header for this combination
        coord_str = f"{coords[0]} & {coords[1]}"
        phoneme_str = f"{phoneme_pairs[0]} & {phoneme_pairs[1]}"
        print(
            f"\n{i:3d}. Coords: {coord_str:20s} Phonemes: {phoneme_str:20s} ({len(words)} words)"
        )

        # Print words (without frequency)
        for j, (word, phonemes, freq) in enumerate(words[:max_words_per_combo], 1):
            print(f"      {j}. {word:20s} phonemes: {phonemes}")

        if len(words) > max_words_per_combo:
            print(f"      ... and {len(words) - max_words_per_combo} more")

    if len(coord_pairs) > max_combos:
        print(f"\n... and {len(coord_pairs) - max_combos} more combinations")

    print("\n" + "=" * 100)


def print_two_coord_summary(result):
    """
    Print a compact summary of 2-coordinate word coverage.
    """
    if 'multi_coord_words' not in result or 2 not in result['multi_coord_words']:
        print("No 2-coordinate words found. Run with check_multi_coord=True")
        return

    two_coord_words = result['multi_coord_words'][2]
    mapping = result['mapping']

    # Calculate statistics
    total_possible = 25 * 24 // 2  # C(25, 2) = 300
    combos_with_words = sum(1 for words in two_coord_words.values() if words)
    total_words = sum(len(words) for words in two_coord_words.values())

    # Find best and worst coverage
    word_counts = []
    for phoneme_pair_set, words in two_coord_words.items():
        coords = tuple(
            sorted([mapping.phonemes_to_coord[pair] for pair in phoneme_pair_set])
        )
        word_counts.append((coords, len(words)))

    word_counts.sort(key=lambda x: x[1], reverse=True)

    print("\n" + "=" * 80)
    print("2-COORDINATE WORD COVERAGE SUMMARY")
    print("=" * 80)
    print(f"\nTotal possible 2-coord combinations: {total_possible}")
    print(
        f"Combinations with at least 1 word:   {combos_with_words} ({combos_with_words/total_possible*100:.1f}%)"
    )
    print(f"Total words found:                    {total_words}")
    print(f"Average words per combination:        {total_words/combos_with_words:.1f}")

    print(f"\n--- Top 10 Best Covered Combinations ---")
    for coords, count in word_counts[:10]:
        print(f"  {str(coords):20s} → {count:3d} words")

    print(f"\n--- Bottom 10 (Least Covered) ---")
    for coords, count in word_counts[-10:]:
        if count > 0:
            print(f"  {str(coords):20s} → {count:3d} words")

    # Show uncovered combinations
    uncovered = total_possible - combos_with_words
    if uncovered > 0:
        print(f"\n{uncovered} combinations have NO words found")

    print("=" * 80)


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    print("\nPhonecode module loaded successfully!")
    print("\nTo get started:")
    print("  1. Run: phonecode.download_required_data()")
    print("  2. Try: results = phonecode.create_5x5_codenames_mapping()")
    print("  3. View: phonecode.print_5x5_results(results)")

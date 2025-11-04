# Phonecode

A Python module for phoneme-based encoding and decoding between discrete multidimensional spaces.

## Overview

`phonecode` provides tools for creating mappings between target spaces (like grid positions or integers) and the phoneme space of English words. This enables encoding information into pronounceable words and decoding words back to their original meaning.

## Applications

- **Codenames Strategy**: Encode multiple grid positions in a single clue word
- **Mnemonic Systems**: Convert numbers to memorable pronounceable words
- **Steganography**: Hide information in natural-sounding speech
- **Memory Palaces**: Create phonetic pegs for memorization
- **Assistive Communication**: Design phoneme-based communication systems

## Installation

```bash
pip install nltk
```

## First-Time Setup

```python
import phonecode

# Download required data (CMU Pronouncing Dictionary + word frequencies)
phonecode.download_required_data()
```

This downloads:
- CMU Pronouncing Dictionary (phoneme transcriptions for ~130,000 words)
- Word frequency data (top 50,000 most common English words)

## Quick Start

### Example 1: 5×5 Codenames Grid

```python
import phonecode

# Create a mapping for a 5x5 grid
results = phonecode.create_5x5_codenames_mapping(
    words_per_coord=3,  # Find 3 example words per grid position
    check_multi_coord=True,  # Search for multi-position words
    max_multi_coord=2  # Up to 2 positions per word
)

# View the results
phonecode.print_5x5_results(results)

# Use the mapping
mapping = results['mapping']

# Decode a word to grid coordinates
coords = mapping.decode_word_to_coords("castle")
print(f"'castle' encodes: {coords}")

# Find words for specific coordinates
target = [(0, 1), (2, 3)]
phonemes = mapping.encode_coords(target)
words = phonecode.find_words_with_phonemes(phonemes, max_results=5)
print(f"Words for {target}: {[w[0] for w in words]}")
```

### Example 2: Integer Encoding

```python
import phonecode

# Create an integer encoding system
results = phonecode.create_integer_encoding_mapping(
    max_integer=999,
    examples_per_length=5
)

# View the results
phonecode.print_integer_results(results)

# Use the mapping
mapping = results['mapping']

# Encode an integer
phonemes = mapping.encode_integer(42)
print(f"42 → {'-'.join(phonemes)}")

# Find pronounceable words for this number
words = phonecode.find_words_with_phonemes(set(phonemes), max_results=5)
print(f"Possible words: {[w[0] for w in words]}")
```

### Example 3: Word Search

```python
import phonecode

# Search for words containing specific phonemes
required = {'K', 'AE', 'T'}  # Phonemes in "cat"
words = phonecode.find_words_with_phonemes(
    required,
    max_results=10,
    common_only=True,
    sort_by_frequency=True
)

for word, phonemes, freq in words:
    print(f"{word}: {'-'.join(phonemes)} (freq: {freq:.2f})")
```

## Core Concepts

### Phoneme Space

English has approximately:
- **24 consonants**: P, B, T, D, K, G, F, V, S, Z, etc.
- **16 vowels**: IY, IH, EY, EH, AE, AA, etc.

The module uses the CMU Pronouncing Dictionary's ARPABET notation.

### Mapping Strategy

1. **Card-ID System** (Recommended): 
   - Each target (e.g., grid position) gets a unique consonant+vowel pair
   - Words containing both phonemes encode that target
   - Phonemes can appear in any order or position
   - Enables natural word formation

2. **Coordinate System**:
   - Consonants map to one dimension (rows)
   - Vowels map to another dimension (columns)
   - More compact but constrains word choice

### Voicing Pairs

Extend coverage by using voicing pairs:
- **/p/ - /b/** (pit/bit)
- **/t/ - /d/** (tin/din)
- **/k/ - /g/** (cap/gap)
- **/f/ - /v/** (fan/van)
- **/s/ - /z/** (sip/zip)

This doubles your consonant space: 5 pairs = 10 consonants.

## API Reference

### Data Management

```python
download_required_data(force=False)
```
Download CMUdict and word frequency data.

### Phoneme Processing

```python
get_phonemes(word: str) -> List[List[str]]
```
Get phoneme transcriptions for a word.

```python
is_vowel_phoneme(phoneme: str) -> bool
is_consonant_phoneme(phoneme: str) -> bool
```
Check phoneme type.

```python
word_contains_phonemes(word: str, required: Set[str]) -> bool
```
Check if word contains all required phonemes.

### Word Search

```python
find_words_with_phonemes(
    required_phonemes: Set[str],
    max_results: int = 100,
    min_word_length: int = 3,
    max_word_length: int = 15,
    sort_by_frequency: bool = True,
    common_only: bool = False
) -> List[Tuple[str, List[str], float]]
```
Find words containing all required phonemes.

```python
find_multi_pair_words(
    phoneme_pairs: List[Tuple[str, str]],
    num_pairs: int = 2,
    **kwargs
) -> Dict
```
Find words encoding multiple coordinate pairs.

### Mapping Classes

#### GridMapping

Maps consonant-vowel pairs to 2D grid coordinates.

```python
mapping = GridMapping(
    consonants=['P', 'T', 'K', 'F', 'S'],
    vowels=['IY', 'AE', 'AA', 'OW', 'UW'],
    grid_shape=(5, 5)
)

# Get phonemes for coordinates
phonemes = mapping.coord_to_phonemes[(row, col)]

# Decode word to coordinates
coords = mapping.decode_word_to_coords("castle")

# Get required phonemes for coordinates
required = mapping.encode_coords([(0, 0), (2, 3)])
```

#### IntegerMapping

Maps digits to phonemes for pronounceable number encoding.

```python
mapping = IntegerMapping()  # Uses default consonants/vowels

# Encode integer to phonemes
phonemes = mapping.encode_integer(42)

# Decode word to integer
number = mapping.decode_word_to_integer("some_word")
```

### High-Level Functions

```python
create_5x5_codenames_mapping(
    consonants=None,
    vowels=None,
    words_per_coord=3,
    check_multi_coord=True,
    max_multi_coord=3
) -> Dict
```
Create complete 5×5 grid mapping with word examples.

```python
create_integer_encoding_mapping(
    max_integer=999,
    consonants=None,
    vowels=None,
    examples_per_length=5
) -> Dict
```
Create integer encoding with example words.

```python
print_5x5_results(results: Dict, show_multi=True)
print_integer_results(results: Dict)
```
Pretty-print mapping results.

## Design Considerations

### Phoneme Selection

Choose phonemes that are:
1. **Highly distinct** (minimize confusion)
2. **Frequent** (appear in many common words)
3. **Robustly pronounced** (hard to mishear)

**Recommended consonants**: P, T, K, F, S (or their voicing pairs)
**Recommended vowels**: IY, AE, AA, OW, UW

Avoid:
- /ɪ/ and /i/ (too similar)
- /n/ and /m/ (nasals sound similar)
- /d/ and /t/ (voicing confusion)

### Order Flexibility

Allowing both CV and VC order (e.g., "TI" or "IT" for /t/+/i/) dramatically increases word availability:
- Without: Only "TIme", "TIger", "parTIal"
- With: "IT", "bIT", "sIT", "kITe", "wriTE", plus all the above

### Multi-Coordinate Words

Encoding 3+ coordinates in one word is extremely difficult. Best strategy:
- Target 1-2 coordinates per word
- Use semantic clues when phonetic encoding fails
- Pre-compute common combinations

## Advanced Usage

### Custom Phoneme Sets

```python
# Use voicing pairs for 10 consonants
consonants = ['P', 'B', 'T', 'D', 'K', 'G', 'F', 'V', 'S', 'Z']
vowels = ['IY', 'AE', 'AA', 'OW', 'UW']

# Create 10×5 = 50 position grid (use subset for 5×5)
mapping = GridMapping(consonants, vowels, grid_shape=(5, 5))
```

### Analyzing Coverage

```python
# Check which coordinates have available words
results = create_5x5_codenames_mapping(words_per_coord=1)

for coord, words in results['single_coord_words'].items():
    if not words:
        print(f"No words found for {coord}")
```

### Building a Word-Finding Tool

```python
def find_codenames_clue(target_coords, mapping):
    """Find best word to encode target coordinates."""
    required = mapping.encode_coords(target_coords)
    
    words = find_words_with_phonemes(
        required,
        max_results=20,
        common_only=True,
        sort_by_frequency=True
    )
    
    # Filter by additional criteria
    best_words = []
    for word, phonemes, freq in words:
        if len(word) <= 8:  # Prefer shorter words
            best_words.append((word, freq))
    
    return best_words
```

## Testing

```bash
# Run tests (requires pytest)
pytest test_phonecode.py -v

# Run doctests
python phonecode.py
```

## Demo

```bash
python demo_phonecode.py
```

This runs demonstrations of all major features.

## Limitations

- Requires NLTK and CMUdict data
- Only supports English phonemes
- Word frequency data may be outdated
- Multi-coordinate words (3+) are rare
- Some dialects merge certain phonemes (e.g., /ɑ/ and /ɔ/)

## Future Enhancements

- Support for other languages
- Real-time word suggestions
- Interactive web interface
- Pre-computed word databases for common patterns
- Phoneme similarity metrics for fuzzy matching
- Integration with speech recognition

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please:
1. Add tests for new features
2. Update documentation
3. Follow existing code style
4. Include docstrings with examples

## Acknowledgments

- CMU Pronouncing Dictionary
- NLTK project
- Word frequency data from various corpora

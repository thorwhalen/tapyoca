"""
Demo script for phonecode module.

Shows how to use the main features.
"""

from tapyoca import phonecode

def demo_5x5_codenames():
    """Demonstrate 5x5 Codenames grid encoding."""
    print("\n" + "="*80)
    print("DEMO: 5×5 CODENAMES GRID ENCODING")
    print("="*80)
    
    # Create mapping with default phonemes
    results = phonecode.create_5x5_codenames_mapping(
        words_per_coord=3,
        check_multi_coord=True,
        max_multi_coord=2
    )
    
    # Print results
    phonecode.print_5x5_results(results, show_multi=True)
    
    # Show how to use the mapping
    print("\n" + "="*80)
    print("USING THE MAPPING")
    print("="*80)
    
    mapping = results['mapping']
    
    # Example: Encode word "CASTLE"
    test_word = "castle"
    coords = mapping.decode_word_to_coords(test_word)
    print(f"\nThe word '{test_word}' encodes these coordinates: {coords}")
    
    # Example: Find what phonemes we need for specific coordinates
    target_coords = [(0, 0), (2, 3)]
    required_phonemes = mapping.encode_coords(target_coords)
    print(f"\nTo encode {target_coords}, we need phonemes: {required_phonemes}")
    
    # Find words that work
    words = phonecode.find_words_with_phonemes(
        required_phonemes,
        max_results=5,
        common_only=True
    )
    print(f"Example words: {[w[0] for w in words]}")


def demo_integer_encoding():
    """Demonstrate integer encoding."""
    print("\n" + "="*80)
    print("DEMO: INTEGER ENCODING")
    print("="*80)
    
    # Create mapping
    results = phonecode.create_integer_encoding_mapping(
        max_integer=999,
        examples_per_length=3
    )
    
    # Print results
    phonecode.print_integer_results(results)
    
    # Show encoding/decoding
    print("\n" + "="*80)
    print("ENCODING/DECODING EXAMPLES")
    print("="*80)
    
    mapping = results['mapping']
    
    # Encode some numbers
    test_numbers = [7, 42, 123]
    for num in test_numbers:
        phonemes = mapping.encode_integer(num)
        print(f"\n{num} → {'-'.join(phonemes)}")
        
        # Try to find words
        words = phonecode.find_words_with_phonemes(
            set(phonemes),
            max_results=3,
            common_only=True
        )
        if words:
            print(f"  Possible words: {[w[0] for w in words[:3]]}")


def demo_word_search():
    """Demonstrate word search functionality."""
    print("\n" + "="*80)
    print("DEMO: WORD SEARCH")
    print("="*80)
    
    # Search for words with specific phonemes
    required = {'K', 'AE', 'T'}
    print(f"\nSearching for words with phonemes: {required}")
    
    words = phonecode.find_words_with_phonemes(
        required,
        max_results=10,
        common_only=True
    )
    
    print(f"\nFound {len(words)} words:")
    for word, phonemes, freq in words[:10]:
        print(f"  {word:15} {'-'.join(phonemes):30} (freq: {freq:.2f})")


def main():
    """Run all demos."""
    print("\n" + "="*80)
    print("PHONECODE MODULE DEMO")
    print("="*80)
    print("\nFirst, make sure data is downloaded...")
    
    try:
        phonecode.download_required_data()
    except Exception as e:
        print(f"Warning: {e}")
        print("Some features may not work without data.")
    
    # Run demos
    demo_word_search()
    demo_5x5_codenames()
    demo_integer_encoding()
    
    print("\n" + "="*80)
    print("DEMO COMPLETE")
    print("="*80)


if __name__ == '__main__':
    main()

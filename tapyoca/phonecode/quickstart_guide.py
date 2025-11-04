"""
PHONECODE QUICK START GUIDE
============================

This guide shows you how to use phonecode for your Codenames strategy.

SETUP (one-time only):
----------------------
1. Install: pip install nltk
2. Download data:
   >>> from tapyoca import phonecode
   >>> phonecode.download_required_data()  # doctest: +SKIP

BASIC WORKFLOW FOR CODENAMES:
------------------------------
"""

from tapyoca import phonecode


def codenames_workflow():
    """Complete workflow for Codenames strategy."""

    # Step 1: Create the mapping (do this before game starts)
    print("=" * 70)
    print("STEP 1: CREATE MAPPING")
    print("=" * 70)

    results = phonecode.create_5x5_codenames_mapping(
        words_per_coord=5,  # Get 5 example words per position
        check_multi_coord=True,
        max_multi_coord=2,
    )

    phonecode.print_5x5_results(results, show_multi=True)

    # Step 2: Memorize the phoneme grid
    print("\n" + "=" * 70)
    print("STEP 2: MEMORIZATION CHART")
    print("=" * 70)

    print("\nYou need to memorize:")
    print("  Rows (consonants): P, T, K, F, S")
    print("  Cols (vowels): IY, AE, AA, OW, UW")
    print("\nExample: Position (1,2) = T + AA")
    print("         Position (3,0) = F + IY (like 'FEE')")

    # Step 3: During the game - find words for your targets
    print("\n" + "=" * 70)
    print("STEP 3: FIND CLUE WORDS (During Game)")
    print("=" * 70)

    mapping = results['mapping']

    # Scenario: You need to clue your partner to these cards:
    target_positions = [(1, 2), (3, 0)]  # Two cards you want them to guess

    print(f"\nTarget cards: {target_positions}")

    # Get required phonemes
    required = mapping.encode_coords(target_positions)
    print(f"Required phonemes: {required}")

    # Find words
    words = phonecode.find_words_with_phonemes(
        required, max_results=10, common_only=True, sort_by_frequency=True
    )

    print(f"\nBest clue words:")
    for i, (word, phonemes, freq) in enumerate(words[:5], 1):
        print(f"  {i}. {word.upper():15} (phonemes: {'-'.join(phonemes)})")

    # Step 4: Verify a word decodes correctly
    print("\n" + "=" * 70)
    print("STEP 4: VERIFY DECODING")
    print("=" * 70)

    if words:
        test_word = words[0][0]
        decoded = mapping.decode_word_to_coords(test_word)
        print(f"\nIf you say '{test_word.upper()}':")
        print(f"  Your partner should decode it as: {decoded}")
        print(f"  Target was: {target_positions}")
        print(f"  Match: {set(decoded) == set(target_positions)}")


def emergency_procedures():
    """What to do when you can't find a word."""
    print("\n" + "=" * 70)
    print("EMERGENCY PROCEDURES")
    print("=" * 70)

    print("\nIf you can't find a word with the right phonemes:")
    print("  1. Try a 2-phoneme word (easier than 4-phoneme)")
    print("  2. Encode just ONE card per clue")
    print("  3. Fall back to regular semantic Codenames clues")
    print("  4. Use pre-computed word lists for common combinations")

    print("\nPre-compute before game:")
    print("  - All single-card words")
    print("  - Common 2-card combinations")
    print("  - Have backup words ready")


def practice_examples():
    """Practice examples to test understanding."""
    print("\n" + "=" * 70)
    print("PRACTICE EXAMPLES")
    print("=" * 70)

    # Create simple mapping for examples
    consonants = ['P', 'T', 'K', 'F', 'S']
    vowels = ['IY', 'AE', 'AA', 'OW', 'UW']
    mapping = phonecode.GridMapping(consonants, vowels)

    print("\nGrid reference:")
    print("       IY    AE    AA    OW    UW")
    print("  P   (0,0) (0,1) (0,2) (0,3) (0,4)")
    print("  T   (1,0) (1,1) (1,2) (1,3) (1,4)")
    print("  K   (2,0) (2,1) (2,2) (2,3) (2,4)")
    print("  F   (3,0) (3,1) (3,2) (3,3) (3,4)")
    print("  S   (4,0) (4,1) (4,2) (4,3) (4,4)")

    # Practice decoding
    print("\n" + "-" * 70)
    print("DECODING PRACTICE")
    print("-" * 70)

    test_words = ["peace", "fast", "site", "coat"]

    for word in test_words:
        phonemes = phonecode.get_phonemes(word)
        if phonemes:
            coords = mapping.decode_word_to_coords(word)
            print(f"\n'{word}' → phonemes: {'-'.join(phonemes[0])}")
            print(f"         → coordinates: {coords}")

    # Practice encoding
    print("\n" + "-" * 70)
    print("ENCODING PRACTICE")
    print("-" * 70)

    target_coords = [(0, 1), (2, 3)]  # P+AE, K+OW
    required = mapping.encode_coords(target_coords)
    print(f"\nTarget: {target_coords}")
    print(f"Need phonemes: {required}")
    print(f"That's P + AE + K + OW")

    words = phonecode.find_words_with_phonemes(required, max_results=5)
    print(f"\nPossible words:")
    for word, _, _ in words:
        print(f"  - {word}")


def tips_and_tricks():
    """Advanced tips."""
    print("\n" + "=" * 70)
    print("TIPS & TRICKS")
    print("=" * 70)

    print(
        """
1. MEMORIZATION TRICKS:
   - Think of consonants as rows: "Peter Takes Kites For Sue"
   - Think of vowels as cols: "I ATTACK" (IY AE AA OW UW)
   
2. DURING GAMEPLAY:
   - Pre-sort your cards by difficulty
   - Start with high-value 2-card combinations
   - Keep a cheat sheet of common words
   
3. OPTIMIZATION:
   - Use high-frequency words (easier for partner)
   - Prefer short words (4-6 letters ideal)
   - Avoid ambiguous pronunciations
   
4. PARTNERSHIP:
   - Practice decoding together beforehand
   - Agree on pronunciation standards
   - Have hand signals for "couldn't find word"
   
5. ADVANCED:
   - Learn which phoneme pairs have the most words
   - Create a database of 2-card optimal words
   - Consider card position in grid for natural clusters
"""
    )


def main():
    """Run the complete guide."""
    print("\n" + "=" * 80)
    print(" " * 20 + "PHONECODE QUICK START")
    print("=" * 80)

    print("\nThis guide will walk you through using phonecode for Codenames.")
    print("Make sure you've run: phonecode.download_required_data()")

    input("\nPress Enter to continue...")

    try:
        codenames_workflow()
        emergency_procedures()
        practice_examples()
        tips_and_tricks()

        print("\n" + "=" * 80)
        print(" " * 25 + "GUIDE COMPLETE!")
        print("=" * 80)
        print("\nYou're ready to dominate Codenames with phonetic encoding!")
        print("\nNext steps:")
        print("  1. Practice the memorization")
        print("  2. Run demo_phonecode.py for more examples")
        print("  3. Generate your pre-game word lists")
        print("  4. Test with a partner")

    except RuntimeError as e:
        print(f"\nError: {e}")
        print("\nPlease run: phonecode.download_required_data()")


if __name__ == '__main__':
    main()

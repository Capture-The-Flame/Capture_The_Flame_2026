#!/bin/sh
NUM_COMMITS=30
NUM_REPEATS=1
REPO="/mnt/c/Users/edmur/Desktop/Capture_the_Flame_2026/My_Challenges/The_Swamp"
FROM_FILE="Once upon a time, there was a lovely princess. But she had an enchantment upon her of a fearful sort. Which would only be broken by love's first kiss. She was locked away in a castle, guarded by a terrible fire breathing dragon. Many brave knights attempted to free her from this dreadful prison, but none prevailed. She waited in the Dragon's Keep, in the highest room of the tallest tower. For her true love and true love's first kiss. And so it came to pass that a brave knight came to her rescue, and with a kiss broke the powerful enchantment. The whole kingdom celebrated on their wedding day."
FILE="forbidden_scroll.txt"
BRANCH="main"

WORDS=($FROM_FILE)

for r in $(seq 1 $NUM_REPEATS); do
    for word in "${WORDS[@]}"; do

        echo -n "$word " >> "$FILE"
        git add "$FILE"
        git commit -m "THE PROPHECY GROWS"
        git push origin "$BRANCH"
    done
done
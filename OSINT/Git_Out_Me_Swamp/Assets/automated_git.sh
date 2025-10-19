#!/bin/bash
NUM_COMMITS=200
REPO="/mnt/c/Users/edmur/Desktop/Capture_the_Flame_2026/My_Challenges/The_Swamp"
FILE="forbidden_scroll.txt"
BRANCH="main"

cd "$REPO" || { echo "Repo not found!"; exit 1; }
for i in $(seq 1 $NUM_COMMITS); do
    echo " Commit $i of $NUM_COMMITS..."

    echo " " >> "$FILE"

    git add "$FILE"
    git commit -m "THE PROPHECY GROWS"
    git push origin "$BRANCH"

done
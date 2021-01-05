import sys
import os
from fuzzywuzzy import fuzz
import textwrap

VERSION = "0.1.0-alpha"
DATA = ""

MATCH_DEFAULT = "moro 5"
DEBUG = False


def main(match, verseNum, width):
    file = open(DATA + "lds-scriptures.txt")
    if DEBUG: print(match)
    d = {}
    scores = []
    for line in file.readlines():
        ref, verse = line.split("     ")
        first, v = ref.split(":")
        verse = verse.strip()
        if first in d:
            d[first].append(verse)
        else:
            partialRatio = fuzz.partial_ratio(match.lower(), first.lower())
            tokenRatio = fuzz.token_sort_ratio(match, first)
            contains = False
            if first.lower().startswith(match.lower().split()[0]):
                contains = True
            total = partialRatio + tokenRatio
            scores.append((first, total, partialRatio, tokenRatio, contains))
            d[first] = [verse]

    scores.sort(key=lambda a: a[1], reverse=False)
    scores = scores[-10:]
    final = scores[0]
    for score in scores:
        if score[4]:
            final = score
    if DEBUG: print (final)
    displayVerse(final[0], d[final[0]], verseNum[0], verseNum[1], width)


def displayVerse(chapter, verseList, startVerse, endVerse, width):
    if startVerse == 0:
        startVerse = 1
        endVerse = len(verseList)

    if startVerse >= len(verseList):
        print(chapter + ":" + str(startVerse) + " doesn't exist")
        return
    finalVerseString = ""
    if endVerse != startVerse:
        finalVerseString = "-" + str(endVerse)
    print (chapter + ":" + str(startVerse) + finalVerseString)
    count = startVerse
    for verse in verseList[startVerse - 1:endVerse]:
        print(textwrap.fill(str(count) + " " + verse, width))
        count += 1


if __name__ == "__main__":
    y = 70  # default value if the console cannot be found
    try:
        y = os.get_terminal_size().columns - 2
    except(OSError):
        pass
    match = ""
    if DEBUG:
        match = MATCH_DEFAULT  # default case

    verse = (0, 0)
    if len(sys.argv) > 1:
        match = ""
        for arg in sys.argv[1:]:
            if ":" in arg:
                chapter, verse = arg.split(":")
                arg = chapter
                if "-" in verse:
                    f, t = verse.split("-")
                    verse = (int(f), int(t))
                else:
                    verse = (int(verse), int(verse))
            match += arg + " "
    else:
        if not DEBUG:
            print("Not enough arguments, please enter 'book chapter:verse'")
            exit(0)
    main(match, verse, y)
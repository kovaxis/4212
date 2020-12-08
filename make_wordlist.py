
import sys

if len(sys.argv) < 1 + 4:
    raise Exception(
        "usage: py make_wordlist.py <input> <min length> <prefix length> <prefer function>")

inpath = sys.argv[1]
minlen = int(sys.argv[2])
prefixlen = int(sys.argv[3])
prefname = sys.argv[4]

# Prefer function
prefer = ({
    'shortest': lambda old, new: len(new) < len(old),
    'longest': lambda old, new: len(new) > len(old),
    'first': lambda old, new: False,
    'last': lambda old, new: True,
})[prefname]

# Group words by their prefix
file = open(inpath, "r")
by_prefix = {}
for word in file.readlines():
    word = word.strip()
    by_prefix.setdefault(word[:prefixlen], []).append(word)
file.close()


# Resolve prefix conflicts through `prefer`
wordlist = []
for prefix, words in by_prefix.items():
    preferred = None
    any_long_enough = False
    for word in words:
        if preferred == None or prefer(preferred, word):
            preferred = word
        if len(word) >= minlen:
            any_long_enough = True
    if any_long_enough:
        wordlist.append(preferred)

# Print entire wordlist as a space-separated string
print(f"{len(wordlist)} words:")
print('"', end="")
first = True
for word in wordlist:
    if first:
        first = False
    else:
        print(" ", end="")
    print(word, end="")
print('"')

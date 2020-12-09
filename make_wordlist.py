
import sys

if len(sys.argv) < 1 + 5:
    raise Exception(
        "usage: py make_wordlist.py <input> <output> <min length> <prefix length> <prefer function> [choice file]")

[_, inpath, outpath, minlen, prefixlen, prefname] = sys.argv[:6]
minlen = int(minlen)
prefixlen = int(prefixlen)
choicepath = None
if len(sys.argv) > 6:
    choicepath = sys.argv[6]

# Prefer function
prefer = ({
    'shortest': lambda old, new: len(new) < len(old),
    'longest': lambda old, new: len(new) > len(old),
    'first': lambda old, new: False,
    'last': lambda old, new: True,
    'manual': None,
})[prefname]

# Group words by their prefix
file = open(inpath, "r")
by_prefix = {}
for word in file.readlines():
    word = word.strip()
    by_prefix.setdefault(word[:prefixlen], []).append(word)
file.close()

# Load saved choices
saved_choices = {}
if choicepath:
    try:
        file = open(choicepath, "r")
        for line in file.readlines():
            [pre, word] = line.split('=')
            saved_choices[pre.strip()] = word.strip()
        file.close()
    except IOError:
        print("failed to open savefile")

# Resolve prefix conflicts through `prefer`
wordlist = []
choicefile = None
if choicepath != None:
    choicefile = open(choicepath, "a")
for prefix, words in by_prefix.items():
    if all(map(lambda w: len(w) < minlen, words)):
        continue
    preferred = None
    if prefer == None:
        saved = saved_choices.get(prefix, None)
        if saved != None:
            if saved != "":
                wordlist.append(saved)
            continue
        i = 0
        while i < len(words):
            w = words[i]
            for j in range(len(words)-1, i, -1):
                if w == words[j]:
                    del words[j]
            i += 1
        words.sort(key=lambda w: len(w))
        print()
        for i in range(len(words)):
            print(f"{i+1}. {words[i]}")
        num = None
        while num == None or num < 0 or num > len(words):
            try:
                num = int(input())
            except ValueError:
                pass
        if num > 0:
            preferred = words[num - 1]
        if choicefile:
            choicefile.write(f"{prefix} = {preferred or ''}\n")
            choicefile.flush()
    else:
        for word in words:
            if preferred == None or prefer(preferred, word):
                preferred = word
    if preferred != None:
        wordlist.append(preferred)
if choicefile:
    choicefile.close()

# Write entire wordlist as a space-separated string
file = open(outpath, "a")
file.write(f"{len(wordlist)} words:\n")
file.write('"')
first = True
for word in wordlist:
    if first:
        first = False
    else:
        file.write(" ")
    file.write(word)
file.write('"\n')
file.close()

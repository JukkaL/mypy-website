# Usage: wordfreq.alo N FILE ...
#
# Display the N most frequent words in file(s). Assume that the files are
# text files encoded using the platform default encoding.

import sys
import re

def main():
    if not sys.argv[2:]:
        raise RuntimeError('Usage: wordfreq.alo N FILE ...')

    d = {}
    n = int(sys.argv[1])

    for fnam in sys.argv[2:]:
        s = open(fnam, 'r').read()
        for word in re.sub('\W', ' ', s).split():
            d[word] = d.get(word, 0) + 1

    l = [(freq, word) for word, freq in d.items()] # Use _list comprehension_

    for freq, word in reversed(sorted(l)[-n:]): # Tuple unpacking
        print('%-6d %s' % (freq, word))

main()

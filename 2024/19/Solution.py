import collections
import heapq
import functools
import bisect


def read_input(path: str = 'input.txt'):
    towels = []
    patterns = []
    reached_patterns = False
    with open(path) as filet:
        for line in filet.readlines():
            line = line.rstrip()

            if not line:
                reached_patterns = True
                continue

            if reached_patterns:
                patterns.append(line)
            else:
                towels.extend(line.split(', '))
    return towels, patterns


class TrieNode:

    def __init__(self, character: str = None, word: str = None):

        self.character = character
        if word is None:
            self.word = ""
        else:
            self.words= word
        self.children = dict()
        self.is_root = character is None

    def set_word(self, word: str):
        self.word = word
        return self

    def add_word(self, word: str):
        assert self.is_root, 'We can only add words from the root.'

        # iterate through the word and create nodes if necessary
        curr = self
        for ch in word:

            # check whether we already have the current character in the Trie
            # if not create it
            if ch not in curr.children:
                curr.children[ch] = TrieNode(ch)
            curr = curr.children[ch]

        # add the word to the root we finalized in
        curr.set_word(word)
        return self


def main1(debug: bool = False):
    result = 0

    # get the towels and the patterns
    towels, patterns = read_input()

    # go through the towels and add them to the Trie
    root = TrieNode()
    for towel in towels:
        root.add_word(towel)

    # go through the patterns we have to do and do dfs
    for pattern in patterns:

        # make a dfs through the word
        @functools.cache
        def dfs(cdx):
            if cdx == len(pattern):
                return True

            # go through the Trie and create possibility every time
            # that we meet and node that contains a word
            curr = root
            for idx, ch in enumerate(pattern[cdx:], cdx):

                # check whether the current character is in the Trie
                if ch in curr.children:
                    curr = curr.children[ch]
                else:
                    break

                # check whether we reached a complete word
                if curr.word and dfs(idx+1):
                    return True
            return False
        # make the dfs through the Trie
        result += dfs(0)
    print(f'The result for solution 1 is: {result}')


def main2():
    result = 0

    # get the towels and the patterns
    towels, patterns = read_input()

    # go through the towels and add them to the Trie
    root = TrieNode()
    for towel in towels:
        root.add_word(towel)

    # go through the patterns we have to do and do dfs
    for pattern in patterns:

        # make a dfs through the word
        @functools.cache
        def dfs(cdx):
            if cdx == len(pattern):
                return 1

            # go through the Trie and create possibility every time
            # that we meet and node that contains a word
            curr = root
            cn = 0
            for idx, ch in enumerate(pattern[cdx:], cdx):

                # check whether the current character is in the Trie
                if ch in curr.children:
                    curr = curr.children[ch]
                else:
                    break

                # check whether we reached a complete word
                cn += bool(curr.word) and dfs(idx + 1)
            return cn

        # make the dfs through the Trie
        result += dfs(0)
    print(f'The result for solution 2 is: {result}')


if __name__ == '__main__':
    main1(True)
    main2()

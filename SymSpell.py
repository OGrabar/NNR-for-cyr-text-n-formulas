from symspellpy.symspellpy import SymSpell, Verbosity

__all__ = ['createSymSpell', 'lookupSymSpell']
__version__ = '0.1.0'


def createSymSpell(dict='ru-100k.txt', encoding='utf-8'):
    symspell = SymSpell(max_dictionary_edit_distance=2, prefix_length=5)
    symspell.load_dictionary(dict, encoding=encoding, term_index=0, count_index=1)
    return symspell


def lookupSymSpell(symspell, word):
    return [_.__str__() for _ in symspell.lookup(word, Verbosity.ALL)]

# http://www.manulex.org/fr/home.html
#
# F : fréquence brute, nombre de mots comptés
# U : Fréquence estimée d'Usage pour 1 million de mots
# SFI : Standard Frequency Index :
#    Un SFI de 90 signifie une rencontre (une occurrence) tous les 10 mots lus.
#    Un SFI de 80 traduit une rencontre tous les 100 mots. Un SFI de 70, tous les 1000 mots, etc...
#
# Auteur : Jonathan Bonnaud
# Date : Mars 2017

import csv
import nltk


def get_csv_file():
    return open('Manulex_formes_ortho.csv')


def get_dict_reader(csv_f):
    return csv.DictReader(csv_f)


def print_words_freq(csv_f, t):
    for r in get_dict_reader(csv_f):
        print(r['FORMES ORTHOGRAPHIQUES'], end=' ')
        print(r['CP {}'.format(t)], end=' ')
        print(r['CE1 {}'.format(t)], end=' ')
        print(r['CE2-CM2 {}'.format(t)])


def get_total_mots(csv_f):
    rd = get_dict_reader(csv_f)
    tot = 0
    for r in rd:
        tot = rd.line_num
    return tot-1


def print_results(typ, tot, voc_cp, voc_ce1, voc_ce2cm2):
    print("Pourcentage de mots fréquents/connus avec {}:".format(typ))
    print("pour le CP (6 ans) :", round(len(voc_cp) / tot, 3), "| nombre de mots moyen connus:", len(voc_cp))
    print("pour le CE1 (7 ans) :", round(len(voc_ce1) / tot, 3), "| nombre de mots moyen connus:", len(voc_ce1))
    print("pour le CE2-CM2 (8-10 ans) :", round(len(voc_ce2cm2) / tot, 3), "| nombre de mots moyen connus:", len(voc_ce2cm2))
    print("\n======================================================================\n")


def reinit_values(voc_cp, voc_ce1, voc_ce2cm2):
    voc_cp.clear()
    voc_ce1.clear()
    voc_ce2cm2.clear()


def test_with_values_f(b=True):
    reinit_values(vocab_CP, vocab_CE1, vocab_CE2CM2)
    typ_freq = 'F'
    """si le nb d'occur > 0 alors il est considéré comme connu"""
    rd = get_dict_reader(get_csv_file())
    for r in rd:
        if r['CP F'] != '':
            vocab_CP.append(r['FORMES ORTHOGRAPHIQUES'])
        if r['CE1 F'] != '':
            vocab_CE1.append(r['FORMES ORTHOGRAPHIQUES'])
        if r['CE2-CM2 F'] != '':
            vocab_CE2CM2.append(r['FORMES ORTHOGRAPHIQUES'])
    if b:
        print_results(typ_freq, total_mots, vocab_CP, vocab_CE1, vocab_CE2CM2)


def test_with_values_u(threshold_u, b=True):
    reinit_values(vocab_CP, vocab_CE1, vocab_CE2CM2)
    typ_freq = 'U'
    rd = get_dict_reader(get_csv_file())
    for r in rd:
        if r['CP {}'.format(typ_freq)] != '' and float(
                r['CP {}'.format(typ_freq)].replace('\xa0', '')) >= threshold_u:
            vocab_CP.append(r['FORMES ORTHOGRAPHIQUES'])
        if r['CE1 {}'.format(typ_freq)] != '' and float(
                r['CE1 {}'.format(typ_freq)].replace('\xa0', '')) >= threshold_u:
            vocab_CE1.append(r['FORMES ORTHOGRAPHIQUES'])
        if r['CE2-CM2 {}'.format(typ_freq)] != '' and float(
                r['CE2-CM2 {}'.format(typ_freq)].replace('\xa0', '')) >= threshold_u:
            vocab_CE2CM2.append(r['FORMES ORTHOGRAPHIQUES'])
    if b:
        print_results(typ_freq, total_mots, vocab_CP, vocab_CE1, vocab_CE2CM2)


def test_with_values_sfi(threshold_sfi, b=True):
    reinit_values(vocab_CP, vocab_CE1, vocab_CE2CM2)
    typ_freq = 'SFI'
    rd = get_dict_reader(get_csv_file())
    for r in rd:
        if r['CP {}'.format(typ_freq)] != '' and float(r['CP {}'.format(typ_freq)]) >= threshold_sfi:
            vocab_CP.append(r['FORMES ORTHOGRAPHIQUES'])
        if r['CE1 {}'.format(typ_freq)] != '' and float(r['CE1 {}'.format(typ_freq)]) >= threshold_sfi:
            vocab_CE1.append(r['FORMES ORTHOGRAPHIQUES'])
        if r['CE2-CM2 {}'.format(typ_freq)] != '' and float(r['CE2-CM2 {}'.format(typ_freq)]) >= threshold_sfi:
            vocab_CE2CM2.append(r['FORMES ORTHOGRAPHIQUES'])
    if b:
        print_results(typ_freq, total_mots, vocab_CP, vocab_CE1, vocab_CE2CM2)


def write_to_csv(method):
    "écrit dans un fichier au format csv pour la création de graphiques"

    with open('test_values_{}.csv'.format(method), 'w') as csvfw:
        writer = csv.DictWriter(csvfw, fieldnames=[method, 'CP', 'CE1', 'CE2-CM2'])
        writer.writeheader()
        if method == 'sfi':
            for i in range(0, 90, 1):
                print("{}%".format(i))
                test_with_values_sfi(i, False)
                writer.writerow({method: i,
                                 'CP': len(vocab_CP),
                                 'CE1': len(vocab_CE1),
                                 'CE2-CM2': len(vocab_CE2CM2)})
        elif method == 'u':
            for i in range(0, 10000, 1):
                print("{}%".format(i))
                test_with_values_u(i, False)
                writer.writerow({method: i,
                                 'CP': len(vocab_CP),
                                 'CE1': len(vocab_CE1),
                                 'CE2-CM2': len(vocab_CE2CM2)})


def test_with_text(text_path):
    """ A partir des données récoltées, combien de mots sont connus dans un texte donné"""
    import re
    text = open("../{}".format(text_path)).read()
    words = nltk.word_tokenize(text)
    print("TEXTE : ", text_path)
    print("{} mots dans le texte".format(len(words)))

    for i, ww in enumerate(words):
        words[i] = ww.lower()

    # split words like [l'hotel] to [l', hotel]
    rg = re.compile("([a-z]+')").split
    words = [part for ww in words for part in rg(ww) if part]

    # split words like [pense-t-il] to [pense, t, il]
    words = [s for w in words for s in w.split('-')]

    words = [s for w in words for s in w.split('_')]

    freq_dist = nltk.FreqDist(words)

    print("{} mots différents (formes ortho) dans le texte\n".format(len(freq_dist)))

    ponct = ['.', ',', '--', '!', '?', '«', '»', ';', ':', '...', '-', '(', ')', '—', '', '_']
    for p in ponct:
        freq_dist.pop(p, None)

    # print(freq_dist.most_common(500))

    mots_CP = []
    mots_CE1 = []
    mots_CE2CM2 = []

    inconnus_CP = []
    inconnus_CE1 = []
    inconnus_CE2CM2 = []

    for w in freq_dist:
        if w in vocab_CP:
            mots_CP.append(w)
        else:
            inconnus_CP.append(w)
        if w in vocab_CE1:
            mots_CE1.append(w)
        else:
            inconnus_CE1.append(w)
        if w in vocab_CE2CM2:
            mots_CE2CM2.append(w)
        else:
            inconnus_CE2CM2.append(w)

    print("Pourcentage mots fréquents CP : ", round(len(mots_CP) / len(freq_dist), 5), "| nombre de mots connus :",
          len(mots_CP))
    # print(inconnus_CP)
    print("Pourcentage mots fréquents CE1 : ", round(len(mots_CE1) / len(freq_dist), 5), "| nombre de mots connus :",
          len(mots_CE1))
    # print(inconnus_CE1)
    print("Pourcentage mots fréquents CE2-CM2: ", round(len(mots_CE2CM2) / len(freq_dist), 5), "| nombre de mots connus :",
          len(mots_CE2CM2))
    # print(inconnus_CE2CM2)
    print()


if __name__ == '__main__':
    """ Valeurs possibles de type_freq : F, U, SFI"""
    vocab_CP = []
    vocab_CE1 = []
    vocab_CE2CM2 = []

    csv_file = get_csv_file()
    total_mots = get_total_mots(csv_file)

    """On s'intéresse d'abord à Manulex - nombre de mots connus parmi tous les mots de la base"""

    print("\nNombre de mots total dans Manulex : {}\n".format(total_mots))

    test_with_values_sfi(48)

    # print(vocab_CP)
    # print(vocab_CE1)
    # print(vocab_CE2CM2)

    """=============================================================================================================="""

    test_with_text('20000lieuessousmer')
    test_with_text('petitchaperonrouge')
    test_with_text('chevremonsieurseguin')

"""
Module pour gérer le dictionnaire dioula et créer la base de connaissances RAG
"""

# Le dictionnaire complet dioula sera stocké ici
DIOULA_DICTIONARY = """
a pron. 1 • Second person plural pronoun ('you, your, you all', etc.); vous.
2 • your, yours; votre, vos.
Usage: In Jula, one typically uses "a" in greetings regardless of the number of people (e.g., "A ni sɔgɔma!") Emphatic: aw. Variant: a' ('Orthographic variant').

à pron. 1 • he, she, it; il, elle.
2 • his, her, its; son, sa.
Emphatic: àle.

abada adv. 1 • never (in negative sentences); jamais. Ne ̀ tɛ shɔ̀ dun abada. I never eat beans. Je ne mange jamais de haricots.
2 • forever, eternally (in affirmative sentences); toujours.
n. eternity; éternité.
Variant: habada.

baara vt. 1 • work on something; travailler quelque chose. yɔrɔ baara work the field. cultiver le terrain, le sarcler.
2 • cast a spell upon; ensorceler.
baara n. work; travail.
baara kɛ vt.con. work; travailler. Denw tɛ baara ̀ kɛ. U bɛ kàlan ̀ kɛ. Children don't work. They study. Les enfants ne travaillent pas. Ils étudient.

bana n. sickness, illness, disease; maladie.

bi n. today; aujourd'hui.

den n. child, offspring.
denmisɛn child, kid; enfant.

dɔɔnin n. a little, a small amount, or a bit; peu, un peu.
adv. a bit, from time to time; de temps en temps.
dɔɔnin-dɔɔnin adv. 1 • slowly; lentement.
2 • softly; doucement.
3 • alright, ok; un peu.

dùgu n. 1 • land, ground, earth; terre.
2 • village, town, city; village, ville.

fɔ vt. 1 • say; dire.
2 • speak a language; parler une langue.
3 • play an instrument; jouer d'un instrument de musique.

i pron. 2nd person singular pronoun ("you", "your"); tu.

ji n. water; eau.

kalan vt. 1 • read; lire.
2 • study; étudier.
3 • teach; enseigner, apprendre.

ko cop. quotative speech copula; copule de la parole.

kuma vi. talk, speak; parler.

ma n. mom (as a term of address); maman.

min det. relative marker (i.e., "that", "which", "who", "where", "when", "how" in English); marqueur relatif.

mɔgɔ n. person, human; homme, être humain, personne.

muso n. woman, wife; femme, épouse.

n pro. I; je.

ni conj. 1 • when; quand.
2 • if; si.
3 • and; et.
4 • with; avec.

nǎ vi. come; venir.

sɔgɔma n. morning; matin.

taa vi. 1 • go; aller.
2 • leave; partir.

ye mp. transitive perfective marker; marque de l'accompli transitive.

"""

def parse_dictionary_entry(entry):
    """Parse une entrée du dictionnaire pour extraire les informations clés"""
    lines = entry.strip().split('\n')
    if not lines:
        return None

    first_line = lines[0]
    word = first_line.split()[0] if first_line else ""

    return {
        "word": word,
        "full_entry": entry.strip(),
        "context": " ".join(lines)
    }

def get_dictionary_entries():
    """Retourne toutes les entrées du dictionnaire parsées"""
    entries = []
    current_entry = []

    for line in DIOULA_DICTIONARY.split('\n'):
        line = line.strip()
        if not line:
            if current_entry:
                entry_text = '\n'.join(current_entry)
                parsed = parse_dictionary_entry(entry_text)
                if parsed:
                    entries.append(parsed)
                current_entry = []
        else:
            current_entry.append(line)

    # Ajouter la dernière entrée si elle existe
    if current_entry:
        entry_text = '\n'.join(current_entry)
        parsed = parse_dictionary_entry(entry_text)
        if parsed:
            entries.append(parsed)

    return entries

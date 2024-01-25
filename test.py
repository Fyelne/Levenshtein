def levenshtein_distance(str1, str2):
    m = len(str1)
    n = len(str2)
 
    prev_row = [j for j in range(n + 1)]
    curr_row = [0] * (n + 1)
 
    for i in range(1, m + 1):
        curr_row[0] = i
 
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                curr_row[j] = prev_row[j - 1]
            else:
                curr_row[j] = 1 + min(
                    curr_row[j - 1],  # Insert
                    prev_row[j],      # Remove
                    prev_row[j - 1]   # Replace
                )
 
        prev_row = curr_row.copy()
 
    return curr_row[n]

def load_dictionary(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return set(word.strip() for word in file)

def correcteur_orthographique(texte, dictionnaire, seuil_similarity=2):
    mots_du_texte = texte.split()
    texte_corrige = []

    for mot in mots_du_texte:
        if mot.lower() not in dictionnaire:
            suggestions = get_suggestions(mot, dictionnaire, seuil_similarity)
            texte_corrige.append(suggestions[0] if suggestions else mot)
        else:
            texte_corrige.append(mot)

    return ' '.join(texte_corrige)

def get_suggestions(mot, dictionnaire, seuil_similarity):
    suggestions = []
    for dict_mot in dictionnaire:
        distance = levenshtein_distance(mot.lower(), dict_mot.lower())
            
        if distance <= seuil_similarity:
            suggestions.append((dict_mot, distance))
    
    suggestions.sort(key=lambda x: x[1]) 
    return [suggestion[0] for suggestion in suggestions]

if __name__ == "__main__":
    dictionnaire_fr = load_dictionary("mots.txt")
    
    # take random words from the dictionary and add some spelling mistakes (insertion, deletion, replacement)
    mots = list(dictionnaire_fr)
    mots_avec_erreurs = mots[:40]
    for i in range(10):
        # insertion
        mot = mots_avec_erreurs[i]
        mots_avec_erreurs[i] = mot[0] + mot[1] + mot[0] + mot[1:]
    for i in range(10, 20):
        # deletion
        mot = mots_avec_erreurs[i]
        mots_avec_erreurs[i] = mot[1:]
    for i in range(20, 30):
        # replacement
        mot = mots_avec_erreurs[i]
        mots_avec_erreurs[i] = mot[0] + 'a' + mot[2:]
    
    # create a text with the words with spelling mistakes
    success = 0
    for i in range(len(mots_avec_erreurs)):
        if correcteur_orthographique(mots_avec_erreurs[i], dictionnaire_fr) == mots[i]:
            success += 1
    print("Accuracy: ", success / len(mots_avec_erreurs))
    if success / len(mots_avec_erreurs) >= 0.8:
        print("Test passed")
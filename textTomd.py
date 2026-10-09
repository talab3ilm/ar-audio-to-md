import os
import re


def process_text_file(input_filepath, output_filepath):
    # Verification de l'existence du fichier d'entree
    if not os.path.exists(input_filepath):
        print(f"Erreur : Le fichier '{input_filepath}' n'existe pas.")
        return

    # Lecture du contenu brut
    with open(input_filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Suppression des marqueurs de pages (PAGE_SEPARATOR et numeros seuls)
    content = re.sub(r'PAGE_SEPARATOR', '', content)
    content = re.sub(r'^\s*\d+\s*$', '', content, flags=re.MULTILINE)

    # 2. Conversion des titres de chapitres/sections (### -> ## ou ## -> ##)
    content = re.sub(r'^###\s*', '## ', content, flags=re.MULTILINE)

    # 3. Formattage des citations d'onglets / vers de poesie (Versets/Poemes)
    # Alignement et mise en forme des versets/poemes groupes
    lines = content.splitlines()
    formatted_lines = []
    in_poem_block = False

    for line in lines:
        strip_line = line.strip()

        # Detection des lignes de vers (contenant souvent '**' ou le caractere de separation d'hemistiches)
        if '**' in strip_line or (
            len(strip_line) > 0 and ' ' in strip_line and ('قوله' not in strip_line and '###' not in strip_line)
        ):
            # Traitement specifique des structures poétiques si nécessaire
            pass

        formatted_lines.append(line)

    final_content = '\n'.join(formatted_lines)

    # 4. Nettoyage des sauts de ligne excessifs
    final_content = re.sub(r'\n{3,}', '\n\n', final_content)

    # Ecriture dans le fichier de sortie
    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write(final_content.strip())

    print(
        f"Traitement termine avec succes ! Fichier enregistre sous : '{output_filepath}'"
    )


# Execution du script : textTomd.py <fichier.txt> [sortie.md] (defaut : <fichier>.md)
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        sys.exit("Usage : textTomd.py <fichier.txt> [sortie.md]")
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(input_file)[0] + ".md"
    process_text_file(input_file, output_file)

import ast
import json

def convert_quotes(input_file, output_file):
    with open(input_file, 'r') as file:
        content = file.read()

    # Utiliser ast.literal_eval pour analyser en structure de données Python
    try:
        data = ast.literal_eval(content)
    except (ValueError, SyntaxError) as e:
        print(f"Erreur de décodage AST: {e}")
        return

    # Formater le JSON avec des doubles quotes
    formatted_json = json.dumps(data, indent=4)

    # Écrire le fichier avec des doubles quotes
    with open(output_file, 'w') as file:
        file.write(formatted_json)

    print(f"Le fichier JSON a été reformaté et sauvegardé dans {output_file}")

# Définir les noms des fichiers d'entrée et de sortie
input_file = 'mock_events.json'
output_file = 'output.json'

# Convertir les quotes dans le fichier JSON
convert_quotes(input_file, output_file)

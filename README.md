# Eine Website mit Seitengenerator in Python

Verwendet:

* Einstellungen im YAML-Format: [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation)
* Seitenvorlagen im Mustache-Format: [Chevron](https://github.com/noahmorrison/chevron)
* Seiten mit [Markdown](https://github.com/Python-Markdown/markdown)
  ... und Frontmatter: [Python Frontmatter](https://python-frontmatter.readthedocs.io/) 

## Seitenstruktur

Einstellungen erfolgen in einer Datei `config.yaml`. Beispiel:

    title: "Hühner & Katzen"
    pages: ./quelle/seiten
    images: ./quelle/bilder
    assets: ./quelle/statisch
    templates: ./templates
    output: ./site

    image_formats: 
    - '1024x'
    - '128x64'

Hier wird die Seite "Hühner & Katzen" in einem Zielordner `output` zusammengestellt. 

Seiten liegen in einem Quellordner im Markdown-Format. Mithilfe von Seitenvorlagen werden daraus HTML-Seiten im Zielordner erzeugt. 

Aus Bildern in einem Quellordner werden verschiedene Formate im Zielordner erzeugt. 

Dateien aus dem Ordner `assets` werden ohne Änderung in den Zielordner kopiert.    

## Aufruf

    python3 -mvenv env
    source env/bin/activate
    ./generate.py

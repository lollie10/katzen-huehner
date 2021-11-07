# Eine Website mit Seitengenerator in Python

Verwendet:

* Einstellungen im YAML-Format: [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation)
* Seitenvorlagen im Mustache-Format: [Chevron](https://github.com/noahmorrison/chevron)
* Seiten mit [Markdown](https://github.com/Python-Markdown/markdown)
  ... und Frontmatter: [Python Frontmatter](https://python-frontmatter.readthedocs.io/) 
* Bilder verkleinern mit [Pillow](https://pillow.readthedocs.io/) 

## Seitenstruktur

Einstellungen erfolgen in einer Datei `config.yaml`. Beispiel:

    title: "Hühner & Katzen"
    pages: ./quelle/seiten
    images: ./quelle/bilder
    assets: ./quelle/statisch
    templates: ./templates
    output: ./docs

    image_sizes: 
    - 600
    - 80

    menu:
    - title: Katzen
        href: /
        img: /images/katze-80.jpg
    - title: Hühner
        href: /seite2.html
        img: /images/huhn-80.jpg

Die generierte Seiten liegen unter https://oschettler.github.io/katzen-huehner/


Hier wird die Seite "Hühner & Katzen" in einem Zielordner `output` zusammengestellt. 

Seiten liegen in einem Quellordner im Markdown-Format. Mithilfe von Seitenvorlagen werden daraus HTML-Seiten im Zielordner erzeugt. 

Aus Bildern in einem Quellordner werden verschiedene Formate im Zielordner erzeugt. 

Dateien aus dem Ordner `assets` werden ohne Änderung in den Zielordner kopiert.    

## Aufruf

Vorbereiten:

    python3 -mvenv env
    source env/bin/activate
    pip install -r requirements.txt

HTML erzeugen:

    ./generate.py

## Bilder

* https://unsplash.com/photos/7GX5aICb5i4
* https://unsplash.com/photos/auijD19Byq8

## Lizenz

Copyright 2021 Olav Schettler

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#!/usr/bin/env python3

'''
Einfacher Generator für statische Websites

- Seiten in Markdown-Dateien mit Frontmatter
- Vorlagen im Mustache-Format
- Bilder werden in verschiedene Größen verkleinert
'''

import chevron
import frontmatter
import functools
import http.server
import markdown
import os
from PIL import Image, ImageOps
import shutil
import sys
import webbrowser
import yaml

config = {}
templates = {}

def load_config():
    '''
    Einstellungen aus Datei config.yaml lesen
    '''
    global config
    config = yaml.load(open('config.yaml'), Loader=yaml.Loader)


def load_templates():
    '''
    Seitenvorlagen lesen
    '''
    global templates

    dir = config['templates']
    for filename in os.listdir(dir):
        name = os.path.splitext(filename)[0]
        templates[name] = open(os.path.join(dir, filename)).read()
        

def generate_pages(root_dir, dir = '.'):
    '''
    HTML-Seiten erzeugen und ins Zielverzeichnis kopieren. 
    
    Dateien im Markdown-Format werden nach HTML gewandelt und
    über die Seitenvorlage 'article' in eine vollständige 
    HTML-Datei mit Kopf und Fuß gewandelt.
    '''
    source_dir = os.path.join(root_dir, dir)
    out_dir = os.path.join(config['output'], dir)
    os.makedirs(out_dir, exist_ok=True) 
    
    with os.scandir(source_dir) as it:
        for entry in it:
            if entry.name.startswith('.'):
                continue
            if entry.is_dir():
                generate_pages(root_dir, os.path.join(dir, entry.name))
            else:
                source_path = os.path.join(source_dir, entry.name)
                
                if entry.name.endswith('.md'):
                    out_filename = os.path.splitext(entry.name)[0] + '.html'
                    out_path = os.path.join(out_dir, out_filename)
                    print(f"Generiere {out_path}")

                    with open(out_path, 'w') as out:
                        article = frontmatter.load(source_path)

                        if 'filter' in article:
                            mod = __import__(article['filter'], fromlist=[None])
                            filter = getattr(mod, 'filter')
                            article.metadata = filter(article.metadata)

                        content = markdown.markdown(article.content)
                        template = article['template'] if 'template' in article else 'article'

                        html = chevron.render(
                            templates[template],
                            {
                                'article': article,
                                'site': config,
                                'content': content
                            }
                        )
                        out.write(html)
                else:
                    out_path = os.path.join(out_dir, entry.name)
                    print(f"Kopiere {out_path}")
                    shutil.copyfile(source_path, out_path)


def generate_images(root_dir, dir = '.'):
    '''
    Bilder in verschiedene Größen verkleinern und ins Zielverzeichnis kopieren.
    '''
    source_dir = os.path.join(root_dir, dir)
    out_dir = os.path.join(config['output'], 'images', dir)
    os.makedirs(out_dir, exist_ok=True) 
    
    with os.scandir(source_dir) as it:
        for entry in it:
            if entry.name.startswith('.'):
                continue
            if entry.is_dir():
                generate_images(root_dir, os.path.join(dir, entry.name))
            else:
                source_path = os.path.join(source_dir, entry.name)
                base, ext = os.path.splitext(entry.name)

                for size in config['image_sizes']:
                    out_path = os.path.join(out_dir, base + '-' + str(size) + ext)
                    print(f"Bild {out_path}")

                    image = Image.open(source_path)
                    #image.thumbnail((size, size))
                    thumb = ImageOps.fit(image, (size, size), Image.ANTIALIAS)
                    thumb.save(out_path)


if __name__ == '__main__':
    load_config()

    if len(sys.argv) == 2 and sys.argv[1] == 'serve':
        # Wenn 'serve' angegeben, starte einen Webserver und öffne den Browser
        port = 8000
        print(f'Webserver auf http://localhost:{port}')
        webbrowser.open(f'http://localhost:{port}')
        handler = functools.partial(
            http.server.SimpleHTTPRequestHandler, directory=config['output']
        )
        httpd = http.server.HTTPServer(('', port), handler)
        httpd.serve_forever()
    else:
        # Sonst wandle Seiten, Bilder und kopiere sie zusammen mit den statischen Dateien 
        load_templates()
        generate_pages(config['pages'])
        generate_images(config['images'])
        shutil.copytree(config['assets'], config['output'], dirs_exist_ok=True)

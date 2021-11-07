#!/usr/bin/env python3

'''
Einfacher Generator für statische Websites

- Seiten in Markdown-Dateien mit Frontmapper
- Vorlagen im Mustache-Format
- 
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
    global config
    config = yaml.load(open('config.yaml'), Loader=yaml.Loader)


def load_templates():
    global templates

    dir = config['templates']
    for filename in os.listdir(dir):
        name = os.path.splitext(filename)[0]
        templates[name] = open(os.path.join(dir, filename)).read()
        

def generate_pages(root_dir, dir = '.'):
    source_dir = os.path.join(root_dir, dir)
    out_dir = os.path.join(config['output'], dir)
    os.makedirs(out_dir, exist_ok=True) 
    
    for dirname, dirnames, filenames in os.walk(source_dir):
        for subdir in dirnames:
            generate_pages(root_dir, os.path.join(dir, subdir))

        for filename in filenames:
            source_path = os.path.join(source_dir, filename)
            
            if filename.endswith('.md'):
                out_filename = os.path.splitext(filename)[0] + '.html'
                out_path = os.path.join(out_dir, out_filename)
                print(f"Generiere {out_path}")

                with open(out_path, 'w') as out:
                    article = frontmatter.load(source_path)
                    content = markdown.markdown(article.content)
                    html = chevron.render(
                        templates['article'],
                        {
                            'article': article,
                            'site': config,
                            'content': content
                        }
                    )
                    out.write(html)
            else:
                out_path = os.path.join(out_dir, filename)
                print(f"Kopiere {out_path}")
                shutil.copyfile(source_path, out_path)


def generate_images(root_dir, dir = '.'):
    source_dir = os.path.join(root_dir, dir)
    out_dir = os.path.join(config['output'], 'images', dir)
    os.makedirs(out_dir, exist_ok=True) 
    
    for dirname, dirnames, filenames in os.walk(source_dir):
        for subdir in dirnames:
            generate_images(root_dir, os.path.join(dir, subdir))

        for filename in filenames:
            source_path = os.path.join(source_dir, filename)
            base, ext = os.path.splitext(filename)

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
        port = 8000
        print(f'Webserver auf http://localhost:{port}')
        webbrowser.open(f'http://localhost:{port}')
        handler = functools.partial(
            http.server.SimpleHTTPRequestHandler, directory=config['output']
        )
        httpd = http.server.HTTPServer(('', port), handler)
        httpd.serve_forever()
    else:
        load_templates()
        generate_pages(config['pages'])
        generate_images(config['images'])
        shutil.copytree(config['assets'], config['output'], dirs_exist_ok=True)

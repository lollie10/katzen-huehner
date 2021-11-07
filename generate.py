#!/usr/bin/env python3

'''
Einfacher Generator für statische Websites

- Seiten in Markdown-Dateien mit Frontmapper
- Vorlagen im Mustache-Format
- 
'''

import yaml

def load_config():
    global config
    config = yaml.load(open('config.yaml'), Loader=yaml.Loader)


if __name__ == '__main__':
    load_config()
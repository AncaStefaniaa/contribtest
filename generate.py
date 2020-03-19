# generate site from static pages, loosely inspired by Jekyll
# run like this:
#   ./generate.py test/source output
# the generated `output` should be the same as `test/expected_output`
import json
import os
import logging
import sys
from pathlib import Path
import jinja2
from jinja2 import FileSystemLoader, Environment



#variabile ce retin calea catre directorul curent, respectiv source pentru a elimina sys.argv
root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, "test\source")

log = logging.getLogger(__name__)

def list_files(folder_path):
    for name in os.listdir(folder_path):
        base, ext = os.path.splitext(name)
        if ext != '.rst':
            continue
        yield os.path.join(folder_path, name)

def read_file(file_path):
    #aici erau deschise in modul binar fisierele si nu se puteau
    #face operatiile, am schimbat in 'r'
    with open(file_path, 'r') as f:
        raw_metadata = ""
        for line in f:
            if line.strip() == '---':
                break
            raw_metadata += line
        content = ""
        for line in f:
            content += line
    return json.loads(raw_metadata), content

def write_output(name, html):
    # TODO should not use sys.argv here, it breaks encapsulation
    # aici vom deschide fisierele in care sa scriem avand calea declarata
    # initial, in modul "w" pentru a rescrie datele in limbaj html
    with open(os.path.join(templates_dir + '/file/' + name), "w") as f:
        f.write(html)


def generate_site(folder_path):
    log.info("Generating site from %r", folder_path)
    jinja_env = jinja2.Environment(loader=FileSystemLoader(folder_path + '\layout'))
    for file_path in list_files(folder_path):
        metadata, content = read_file(file_path)
        #nu exista template_name in fisierele rst
        #am adaugat cheia layout
        template_name = metadata['layout']
        template = jinja_env.get_template(template_name)
        data = dict(metadata, content = content)
        #in html am pastrat codul html pe care l-am obtinut
        #prin aplicarea functiei render pe datelele noastre din
        #dictionar
        html = template.render(**data, clear = True)
        write_output(template_name, html)
        log.info("Writing %r with template %r", os.name, template_name)


def main():
    #apelare folosind calea definita
    generate_site(templates_dir)

if __name__ == '__main__':
    logging.basicConfig()
    main()

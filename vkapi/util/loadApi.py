# coding: utf-8
import urllib, urllib2
import logging
import colorer
from BeautifulSoup import BeautifulSoup
import re
import os
from template import build_api
import ConfigParser

"""This module will parse the wiki of vkontakte and load all function definition
   in order to generate a dict of all functions. It then pass it to a template 
   that will generate a module that can be used to access the vkapi directly with
   python on the server side.
"""

# Load config
top_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
config_path = os.path.join(top_path, 'config.ini')
config = ConfigParser.ConfigParser({
    'here': top_path,
})
config.read(config_path)


#Start logging for debug
logging.debug(True)

# API url to extract
base_address = config.get('main', 'base_address')
wiki_page = config.get('main', 'wiki_page')
api_url = '%s/%s' % (base_address, wiki_page)

def filter_name(text):
    """A filter that convert non ascii chars to ascii.
       It is used for function names and attributes. Character
       encoding shouldn't matter anywhere else.
    """
    return text.replace('с'.decode('utf-8'),'c')

def guess_type(name):
    """Guess the type of the parameter. If it ends in 'ids', it is
    mostly a list of ids (cids, ids, pids...) while the rest can be handled
    as string most of the times. It would be good if the input type was 
    present in the wikipage, so I can easily parse them and set a valid format.
    """
    if name.endswith('ids'):
        return 'strlist'
    else:
        return 'string'

def main():
    """Main function that does the loading
           1. Download the first wiki page
           2. Download all other wiki pages related by function names
           3. Parse every function definition into a dict
           4. Generate the api with a template
           5. Enjoy
    """

    temp_path = config.get('main', 'temp')
    temp_files = config.get('main', 'temp_files')

    if not os.path.exists(temp_path):
        os.mkdir(temp_path)

    if not os.path.exists(temp_files):
        os.mkdir(temp_files)

    load_spec(temp_path, temp_files)
    methods = load_methods(temp_path, temp_files)
    generated = build_api(methods)
    
    vk = open('vk.py', 'w')
    vk.write(generated.encode('utf-8'))
    vk.close()

def convert(name):
    """Convert camelcase name to underscore separated words"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def load_spec(base_path, files_path):
    """Loads the specifications of all the functions
       (Main wiki pages for methods)
    """

    print 'Downloading specification'
    api_spec = urllib.urlopen(api_url)
    # TODO unsure if received html code is cp1251 or utf-8... even if 
    #      it is written cp1251 in the <meta> tag...
    html = api_spec.read().decode('cp1251').encode('utf-8')
    #html = api_spec.read().encode('utf-8')
    soup = BeautifulSoup(html)

    spec = open(os.path.join(base_path, 'spec'), 'w')
    spec.write(html)
    spec.close()
    print 'Specification file saved'

    print 'Loading methods'

    for ul in soup.findAll('ul', {'class': 'listing'}):
        for li in ul.findAll('li'):
            # We take the first link in the list 
            # Sometimes there is more than one link but 
            # we only need the first one.
            a = li.find('a', href=re.compile('pages.php'))
            if not os.path.isabs(a['href']):
                a['href'] = '/%s' % a['href']

            func_name = convert(a.contents[0])

            method = urllib.urlopen('%s%s' % (base_address, a['href'])).read().decode('cp1251').encode('utf-8')
            fout = open(os.path.join(files_path, func_name), 'w')
            fout.write(method)
            fout.close()
            print '%s: Saved' % func_name

    print 'Finished'

def load_methods(base_path, files_path):
    """Loads all functions and add them to a dict of methods"""
    methods = {}
    for root, dirs, files in os.walk(files_path):
        for filename in files:
            method = load_method(base_path, files_path, filename)
            if method[0] and method[1]:
                func_name = filename.split('.')
                namespace = methods
                for i, subname in enumerate(func_name):
                    if not i == len(func_name) - 1:
                        namespace[subname] = namespace.get(subname, {})
                        namespace = namespace[subname]
                    else:
                        namespace[subname] = method[1]
    return methods


def load_method(base_path, files_path, filename):
    """Loads a method with the filename as parameter"""
    logging.info('Loading: %s' % filename)
    func_name = filename

    #html2 = open(filename, 'r').read().decode('cp1251', 'replace').encode('utf-8')
    # TODO be certain that we really receive utf-8 instead of cp1251
    #      decoding cp1251 break the script with invalid chars... unsure of the real encoding
    html2 = open(os.path.join(files_path, filename), 'r').read().decode('utf-8')
    html2 = BeautifulSoup(html2)


    table = html2.find('table', {'class': 'wikiTable'})

    if not table:
        logging.error('Error: %s table not there' % func_name)
        return (None, None)

    real_name = html2.find('div', {'class': 'wikiTitle'})
    if not real_name:
        logging.error('Error: %s func name not present' % func_name)
        return (None, None)
    else:
        real_name = real_name.contents[0]

    params = {
        '@method': real_name,
    }

    for tr in table.findAll('tr'):
        tds = tr.findAll('td')
        if tds:
            name = tds[0].center.contents[0]
            required = tds[1].center != None

            #If set to true in the config, it will filter all methods
            #name for invalid chars. If set to false it might create an
            #invalid api files or it might even break the script.
            if config.getboolean('main', 'filter'):
                name = filter_name(name)

            if name in ['sig', 'api_id', 'v', 'format', 'test_mode']:
                continue

            params[name] = {
                'required': required,
                'type': guess_type(name),
            }

    logging.info('%s: Loaded' % func_name)

    return (func_name, params)
    #except:
    #    logging.error('Error loading: %s' % func_name)
    #return (None, None)


if __name__ == '__main__':
    main()

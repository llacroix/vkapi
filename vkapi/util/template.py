from mako.template import Template
from mako.runtime import Context
from StringIO import StringIO

def build_api(methods):
    from loadApi import config
    template_path = config.get('main', 'template')
    programming_language = config.get('default', 'languages')
    tplt = os.path.join(template_path, programming_language, 'api.mako')
    mytemplate = Template(filename=os.path.join(tplt))
    buf = StringIO()
    ctx = Context(buf, methods=methods)
    mytemplate.render_context(ctx)
    return buf.getvalue()

if __name__ == '__main__':
    methods = {
        'audio': {
            'search': {
                'sort': {'required': False, 'type': None}, 
                'count': {'required': False, 'type': None}, 
                'lyrics': {'required': False, 'type': None}, 
                'q': {'required': True, 'type': None}, 
                'offset': {'required': False, 'type': None}, 
                '@method': 'search'
            }, 
            'save': {
                'hash': {'required': True, 'type': None}, 
                'title': {'required': False, 'type': None}, 
                'artist': {'required': False, 'type': None}, 
                'server': {'required': True, 'type': None}, 
                '@method': 'save', 
                'audio': {'required': True, 'type': None}
            }, 
            'get': {
                'need_user': {'required': False, 'type': None}, 
                'aids': {'required': False, 'type': None}, 
                '@method': 'get', 
                'gid': {'required': False, 'type': None}, 
                'uid': {'required': False, 'type': None}
            }, 
            'edit': {
                'title': {'required': True, 'type': None}, 
                'text': {'required': True, 'type': None}, 
                'oid': {'required': True, 'type': None}, 
                'aid': {'required': True, 'type': None}, 
                '@method': 'edit', 
                'artist': {'required': True, 'type': None}, 
                'no_search': {'required': True, 'type': None}
            }, 
            'get_lyrics': {
                'lyrics_id': {'required': False, 'type': None}, 
                '@method': 'getLyrics',
            }, 
            'add': {
                'aid': {'required': True, 'type': None}, 
                '@method': 'add', 
                'oid': {'required': True, 'type': None}, 
                'gid': {'required': True, 'type': None}
            }, 
            'get_by_id': {
                '@method': 'getById', 
                'audios': {'required': False, 'type': None}
            }, 
            'delete': {
                'aid': {'required': True, 'type': None}, 
                '@method': 'delete', 
                'oid': {'required': True, 'type': None}
            }, 
            'get_upload_server': {
                '@method': 'getUploadServer',
            }
        }
    }
    template = build_api(methods)
    fout = open('vk.py', 'w')
    fout.write(template.encode('utf-8'))
    fout.close()
    print template

## coding: utf-8
# coding: utf-8
import urllib, urllib2
from hashlib import md5
import simplejson

def vk_intlist(arg):
    return vk_strlist(arg)

def vk_int(arg):
    return int(arg)

def vk_str(arg):
    return unicode(arg)

def vk_strlist(arg):
    for id, element in enumerate(arg):
        arg[id] = vk_str(element)
    return ','.join(arg)

def vk_bool(arg):
    if arg:
        return 1
    else:
        return 0

class vkapi(object):

    def __init__(self, user_id, viewer_id, secret, auth_key, api_url, api_id, test_mode=False):
        self.secret = secret
        self.user_id = user_id
        self.viewer_id = viewer_id
        self.api_url = api_url
        self.test_mode = test_mode

        self.api_args = {
            'auth_key': auth_key,
            'v': '2.0',
            'format': 'json',
            'api_id': api_id
        }
        if test_mode:
            self.api_args['test_mode'] = 1

        % for method, params in methods.items():
            % if not params.get('@method'):
        self.${method} = vkapi.__${method}(self)
            % endif
        % endfor

    def _build_sig(self, params):
        par = params.items()
        par.sort()
        par_str = ''

        for key, value in par:
            par_str += '%s=%s' % (key, value)

        sig = '%(viewer_id)s%(params)s%(secret)s' % {'viewer_id': self.viewer_id, 'secret': self.secret, 'params': par_str}
        return md5(sig).hexdigest()

    def _build_url(self, params):

        sig = self._build_sig(params)
        params['sig'] = sig

        return '%s?%s' % (self.api_url,  urllib.urlencode(params))


    def send(self, url):
        ret = urllib.urlopen(url).read()
        return simplejson.loads(ret)


    def do_request(self, params):
        params.update(self.api_args)

        url = self._build_url(params)

        result = self.send(url)
    
        if result.get('response'):
            return result['response']
        else:
            print result
            raise RuntimeError('Erreur de réception')

    % for key, value in methods.items():
        % if value.get('@method'):
            ${build_def(key, value)}
        % else:
            ${build_namespace(key, value)}
        % endif
    % endfor


<%def name="build_def(name, params, level=0)"><%
required = [(k, v) for k, v in params.items() if k != '@method' and v.get('required')]
optional = [(k, v) for k, v in params.items() if k != '@method' and not v.get('required')]
real_name = params.get('@method')

def build_args(required, optional):
    req = ['self'] + dict(required).keys()
    opt = ['%s=None' % k for k, v in optional]
    return ', '.join(req + opt)

formatter = {                                                                                                                                                                
    'int': 'vk_int',
    'intlist': 'vk_intlist',
    'string': 'vk_str',
    'strlist': 'vk_strlist',
    'bool': 'vk_bool',
}

%>
${indent(level)}    def ${name}(${build_args(required, optional)}):
${indent(level)}        params = {
${indent(level)}            'method': "${real_name}",
                        % for variable, params in required:
${indent(level)}            '${variable}': ${formatter.get(params.get('type'), 'vk_str')}(${variable}),
                        % endfor
${indent(level)}        }
                        % for variable, params in optional:
${indent(level)}        if ${variable}:
${indent(level)}            params["${variable}"] = ${formatter.get(params.get('type'), 'vk_str')}(${variable})
                        % endfor
${indent(level)}        return self.do_request(params)
</%def>

<%def name="build_namespace(name, methods, level=0)">
${indent(level)}    class __${name}(object):
${indent(level)}        def __init__(self, parent):
${indent(level)}            self.secret = parent.secret
${indent(level)}            self.user_id = parent.user_id
${indent(level)}            self.viewer_id = parent.viewer_id
${indent(level)}            self.api_url = parent.api_url
${indent(level)}            self.test_mode = parent.test_mode
${indent(level)}            self.api_args = parent.api_args
${indent(level)}            self._build_sig = parent._build_sig
${indent(level)}            self._build_url = parent._build_url
${indent(level)}            self.send = parent.send
${indent(level)}            self.do_request = parent.do_request

                    % for key, value in methods.items():
                        % if value.get('@method'):
${indent(level)}            ${build_def(key, value, level=level+1)}
                        % else:
${indent(level)}            ${build_namespace(key, value, level=level+1)}
                        % endif
                    % endfor
</%def>

<%def name="indent(level)">${''.join([' ' for i in range(level * 4)])}</%def>

##  def get_profiles(self, uids, fields=None, name_case=None):
##      params = {
##          "method": "getProfiles",
##          "uids": vk_intlist(uids),
##      }
##    
##      if fields:
##          params["fields"] = vk_strlist(fields)
##      if name_case:
##          params["name_case"] = vk_str(name_case)
##      return self.do_request(params)

# coding: utf-8
import urllib, urllib2
from hashlib import md5

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

        self.secure = vkapi.__secure(self)
        self.wall = vkapi.__wall(self)
        self.video = vkapi.__video(self)
        self.questions = vkapi.__questions(self)
        self.offers = vkapi.__offers(self)
        self.language = vkapi.__language(self)
        self.photos = vkapi.__photos(self)
        self.friends = vkapi.__friends(self)
        self.pages = vkapi.__pages(self)
        self.notes = vkapi.__notes(self)
        self.activity = vkapi.__activity(self)
        self.audio = vkapi.__audio(self)

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
        return eval(ret)

    def do_request(self, params):
        params.update(self.api_args)

        url = self._build_url(params)

        result = self.send(url)
    
        if result.get('response'):
            return result['response']
        else:
            print result
            raise RuntimeError('Erreur de réception')

            
    class __secure(object):
        def __init__(self, parent):
            self.secret = parent.secret
            self.user_id = parent.user_id
            self.viewer_id = parent.viewer_id
            self.api_url = parent.api_url
            self.test_mode = parent.test_mode
            self.api_args = parent.api_args
            self._build_sig = parent._build_sig
            self._build_url = parent._build_url
            self.send = parent.send
            self.do_request = parent.do_request

            
        def get_transactions_history(self, timestamp, random, date_to=None, date_from=None, uid_to=None, uid_from=None, limit=None, type=None):
            params = {
                'method': "secure.getTransactionsHistory",
                'timestamp': vk_str(timestamp),
                'random': vk_str(random),
            }
            if date_to:
                params["date_to"] = vk_str(date_to)
            if date_from:
                params["date_from"] = vk_str(date_from)
            if uid_to:
                params["uid_to"] = vk_str(uid_to)
            if uid_from:
                params["uid_from"] = vk_str(uid_from)
            if limit:
                params["limit"] = vk_str(limit)
            if type:
                params["type"] = vk_str(type)
            return self.do_request(params)

            
        def set_counter(self, timestamp, random, uid, counter):
            params = {
                'method': "secure.setCounter",
                'timestamp': vk_str(timestamp),
                'random': vk_str(random),
                'uid': vk_str(uid),
                'counter': vk_str(counter),
            }
            return self.do_request(params)

            
        def send_sms_notification(self, timestamp, message, random, uid):
            params = {
                'method': "secure.sendSMSNotification",
                'timestamp': vk_str(timestamp),
                'message': vk_str(message),
                'random': vk_str(random),
                'uid': vk_str(uid),
            }
            return self.do_request(params)

            
        def save_app_status(self, status, timestamp, random, uid):
            params = {
                'method': "secure.saveAppStatus",
                'status': vk_str(status),
                'timestamp': vk_str(timestamp),
                'random': vk_str(random),
                'uid': vk_str(uid),
            }
            return self.do_request(params)

            
        def get_sms(self, timestamp, random, uid, date_from=None, date_to=None):
            params = {
                'method': "secure.getSMS",
                'uid': vk_str(uid),
                'timestamp': vk_str(timestamp),
                'random': vk_str(random),
            }
            if date_from:
                params["date_from"] = vk_str(date_from)
            if date_to:
                params["date_to"] = vk_str(date_to)
            return self.do_request(params)

            
        def delete_language_value(self, timestamp, random, key):
            params = {
                'method': "secure.deleteLanguageValue",
                'timestamp': vk_str(timestamp),
                'random': vk_str(random),
                'key': vk_str(key),
            }
            return self.do_request(params)

            
        def get_sms_history(self, timestamp, random, uid=None, date_from=None, limit=None, date_to=None):
            params = {
                'method': "secure.getSMSHistory",
                'timestamp': vk_str(timestamp),
                'random': vk_str(random),
            }
            if uid:
                params["uid"] = vk_str(uid)
            if date_from:
                params["date_from"] = vk_str(date_from)
            if limit:
                params["limit"] = vk_str(limit)
            if date_to:
                params["date_to"] = vk_str(date_to)
            return self.do_request(params)

            
        def add_rating(self, timestamp, rate, random, message, uid):
            params = {
                'method': "secure.addRating",
                'uid': vk_str(uid),
                'timestamp': vk_str(timestamp),
                'random': vk_str(random),
                'rate': vk_str(rate),
                'message': vk_str(message),
            }
            return self.do_request(params)

            
        def send_notification(self, timestamp, message, random, uids):
            params = {
                'method': "secure.sendNotification",
                'timestamp': vk_str(timestamp),
                'message': vk_str(message),
                'random': vk_str(random),
                'uids': vk_strlist(uids),
            }
            return self.do_request(params)

            
        def get_app_balance(self, timestamp, random):
            params = {
                'method': "secure.getAppBalance",
                'timestamp': vk_str(timestamp),
                'random': vk_str(random),
            }
            return self.do_request(params)

            
        def withdraw_votes(self, timestamp, votes, random, uid):
            params = {
                'method': "secure.withdrawVotes",
                'timestamp': vk_str(timestamp),
                'votes': vk_str(votes),
                'random': vk_str(random),
                'uid': vk_str(uid),
            }
            return self.do_request(params)

            
        def get_app_status(self, uid):
            params = {
                'method': "secure.getAppStatus",
                'uid': vk_str(uid),
            }
            return self.do_request(params)

            
        def set_language_value(self, timestamp, random, key, value, description=None, locale=None):
            params = {
                'method': "secure.setLanguageValue",
                'timestamp': vk_str(timestamp),
                'random': vk_str(random),
                'value': vk_str(value),
                'key': vk_str(key),
            }
            if description:
                params["description"] = vk_str(description)
            if locale:
                params["locale"] = vk_str(locale)
            return self.do_request(params)

            
        def get_balance(self, timestamp, random, uid):
            params = {
                'method': "secure.getBalance",
                'timestamp': vk_str(timestamp),
                'random': vk_str(random),
                'uid': vk_str(uid),
            }
            return self.do_request(params)


            
    class __wall(object):
        def __init__(self, parent):
            self.secret = parent.secret
            self.user_id = parent.user_id
            self.viewer_id = parent.viewer_id
            self.api_url = parent.api_url
            self.test_mode = parent.test_mode
            self.api_args = parent.api_args
            self._build_sig = parent._build_sig
            self._build_url = parent._build_url
            self.send = parent.send
            self.do_request = parent.do_request

            
        def get_photo_upload_server(self):
            params = {
                'method': "wall.getPhotoUploadServer",
            }
            return self.do_request(params)

            
        def save_post(self, wall_id, hash=None, photo=None, server=None, post_id=None, photo_id=None, message=None):
            params = {
                'method': "wall.savePost",
                'wall_id': vk_str(wall_id),
            }
            if hash:
                params["hash"] = vk_str(hash)
            if photo:
                params["photo"] = vk_str(photo)
            if server:
                params["server"] = vk_str(server)
            if post_id:
                params["post_id"] = vk_str(post_id)
            if photo_id:
                params["photo_id"] = vk_str(photo_id)
            if message:
                params["message"] = vk_str(message)
            return self.do_request(params)


            
    def send_message(self, message, session=None):
        params = {
            'method': "sendMessage",
            'message': vk_str(message),
        }
        if session:
            params["session"] = vk_str(session)
        return self.do_request(params)

            
    def get_user_settings(self):
        params = {
            'method': "getUserSettings",
        }
        return self.do_request(params)

            
    class __video(object):
        def __init__(self, parent):
            self.secret = parent.secret
            self.user_id = parent.user_id
            self.viewer_id = parent.viewer_id
            self.api_url = parent.api_url
            self.test_mode = parent.test_mode
            self.api_args = parent.api_args
            self._build_sig = parent._build_sig
            self._build_url = parent._build_url
            self.send = parent.send
            self.do_request = parent.do_request

            
        def search(self, q, sort=None, count=None, offset=None, hd=None):
            params = {
                'method': "video.search",
                'q': vk_str(q),
            }
            if sort:
                params["sort"] = vk_str(sort)
            if count:
                params["count"] = vk_str(count)
            if offset:
                params["offset"] = vk_str(offset)
            if hd:
                params["hd"] = vk_str(hd)
            return self.do_request(params)

            
        def get_tags(self, vid, owner_id=None):
            params = {
                'method': "video.getTags",
                'vid': vk_str(vid),
            }
            if owner_id:
                params["owner_id"] = vk_str(owner_id)
            return self.do_request(params)

            
        def get(self, count=None, uid=None, videos=None, width=None, offset=None):
            params = {
                'method': "video.get",
            }
            if count:
                params["count"] = vk_str(count)
            if uid:
                params["uid"] = vk_str(uid)
            if videos:
                params["videos"] = vk_str(videos)
            if width:
                params["width"] = vk_str(width)
            if offset:
                params["offset"] = vk_str(offset)
            return self.do_request(params)

            
        def edit(self, oid, name, vid, desc):
            params = {
                'method': "video.edit",
                'oid': vk_str(oid),
                'name': vk_str(name),
                'vid': vk_str(vid),
                'desc': vk_str(desc),
            }
            return self.do_request(params)

            
        def edit_comment(self, message, cid, owner_id=None):
            params = {
                'method': "video.editComment",
                'message': vk_str(message),
                'cid': vk_str(cid),
            }
            if owner_id:
                params["owner_id"] = vk_str(owner_id)
            return self.do_request(params)

            
        def remove_tag(self, vid, tag_id, owner_id):
            params = {
                'method': "video.removeTag",
                'tag_id': vk_str(tag_id),
                'vid': vk_str(vid),
                'owner_id': vk_str(owner_id),
            }
            return self.do_request(params)

            
        def delete_comment(self, cid, owner_id=None):
            params = {
                'method': "video.deleteComment",
                'cid': vk_str(cid),
            }
            if owner_id:
                params["owner_id"] = vk_str(owner_id)
            return self.do_request(params)

            
        def put_tag(self, uid, vid, owner_id):
            params = {
                'method': "video.putTag",
                'uid': vk_str(uid),
                'vid': vk_str(vid),
                'owner_id': vk_str(owner_id),
            }
            return self.do_request(params)

            
        def add(self, oid, vid):
            params = {
                'method': "video.add",
                'oid': vk_str(oid),
                'vid': vk_str(vid),
            }
            return self.do_request(params)

            
        def get_comments(self, vid, count=None, offset=None, owner_id=None):
            params = {
                'method': "video.getComments",
                'vid': vk_str(vid),
            }
            if count:
                params["count"] = vk_str(count)
            if offset:
                params["offset"] = vk_str(offset)
            if owner_id:
                params["owner_id"] = vk_str(owner_id)
            return self.do_request(params)

            
        def get_user_videos(self, count=None, uid=None, offset=None):
            params = {
                'method': "video.getUserVideos",
            }
            if count:
                params["count"] = vk_str(count)
            if uid:
                params["uid"] = vk_str(uid)
            if offset:
                params["offset"] = vk_str(offset)
            return self.do_request(params)

            
        def save(self, name=None, description=None):
            params = {
                'method': "video.save",
            }
            if name:
                params["name"] = vk_str(name)
            if description:
                params["description"] = vk_str(description)
            return self.do_request(params)

            
        def create_comment(self, message, vid, owner_id=None):
            params = {
                'method': "video.createComment",
                'message': vk_str(message),
                'vid': vk_str(vid),
            }
            if owner_id:
                params["owner_id"] = vk_str(owner_id)
            return self.do_request(params)

            
        def delete(self, oid, vid):
            params = {
                'method': "video.delete",
                'oid': vk_str(oid),
                'vid': vk_str(vid),
            }
            return self.do_request(params)


            
    class __questions(object):
        def __init__(self, parent):
            self.secret = parent.secret
            self.user_id = parent.user_id
            self.viewer_id = parent.viewer_id
            self.api_url = parent.api_url
            self.test_mode = parent.test_mode
            self.api_args = parent.api_args
            self._build_sig = parent._build_sig
            self._build_url = parent._build_url
            self.send = parent.send
            self.do_request = parent.do_request

            
        def search(self, sort=None, count=None, text=None, offset=None, need_profiles=None, name_case=None, type=None):
            params = {
                'method': "questions.search",
            }
            if sort:
                params["sort"] = vk_str(sort)
            if count:
                params["count"] = vk_str(count)
            if text:
                params["text"] = vk_str(text)
            if offset:
                params["offset"] = vk_str(offset)
            if need_profiles:
                params["need_profiles"] = vk_str(need_profiles)
            if name_case:
                params["name_case"] = vk_str(name_case)
            if type:
                params["type"] = vk_str(type)
            return self.do_request(params)

            
        def get(self, sort=None, count=None, uids=None, qid=None, need_profiles=None, name_case=None, offset=None):
            params = {
                'method': "questions.get",
            }
            if sort:
                params["sort"] = vk_str(sort)
            if count:
                params["count"] = vk_str(count)
            if uids:
                params["uids"] = vk_strlist(uids)
            if qid:
                params["qid"] = vk_str(qid)
            if need_profiles:
                params["need_profiles"] = vk_str(need_profiles)
            if name_case:
                params["name_case"] = vk_str(name_case)
            if offset:
                params["offset"] = vk_str(offset)
            return self.do_request(params)

            
        def add_answer(self, qid, uid, text):
            params = {
                'method': "questions.addAnswer",
                'qid': vk_str(qid),
                'uid': vk_str(uid),
                'text': vk_str(text),
            }
            return self.do_request(params)

            
        def get_types(self):
            params = {
                'method': "questions.getTypes",
            }
            return self.do_request(params)

            
        def get_outbound(self, sort=None, count=None, need_profiles=None, name_case=None, offset=None):
            params = {
                'method': "questions.getOutbound",
            }
            if sort:
                params["sort"] = vk_str(sort)
            if count:
                params["count"] = vk_str(count)
            if need_profiles:
                params["need_profiles"] = vk_str(need_profiles)
            if name_case:
                params["name_case"] = vk_str(name_case)
            if offset:
                params["offset"] = vk_str(offset)
            return self.do_request(params)

            
        def edit(self, qid, type, text):
            params = {
                'method': "questions.edit",
                'qid': vk_str(qid),
                'type': vk_str(type),
                'text': vk_str(text),
            }
            return self.do_request(params)

            
        def add(self, text, type):
            params = {
                'method': "questions.add",
                'text': vk_str(text),
                'type': vk_str(type),
            }
            return self.do_request(params)

            
        def get_answer_votes(self, aid, uid, sort=None, count=None, need_profiles=None, offset=None):
            params = {
                'method': "questions.getAnswerVotes",
                'uid': vk_str(uid),
                'aid': vk_str(aid),
            }
            if sort:
                params["sort"] = vk_str(sort)
            if count:
                params["count"] = vk_str(count)
            if need_profiles:
                params["need_profiles"] = vk_str(need_profiles)
            if offset:
                params["offset"] = vk_str(offset)
            return self.do_request(params)

            
        def join_answer(self, aid, uid):
            params = {
                'method': "questions.joinAnswer",
                'aid': vk_str(aid),
                'uid': vk_str(uid),
            }
            return self.do_request(params)

            
        def delete_answer(self, aid, uid):
            params = {
                'method': "questions.deleteAnswer",
                'aid': vk_str(aid),
                'uid': vk_str(uid),
            }
            return self.do_request(params)

            
        def mark_as_viewed(self, aids=None):
            params = {
                'method': "questions.markAsViewed",
            }
            if aids:
                params["aids"] = vk_strlist(aids)
            return self.do_request(params)

            
        def get_answers(self, qid, sort=None, count=None, need_profiles=None, offset=None):
            params = {
                'method': "questions.getAnswers",
                'qid': vk_str(qid),
            }
            if sort:
                params["sort"] = vk_str(sort)
            if count:
                params["count"] = vk_str(count)
            if need_profiles:
                params["need_profiles"] = vk_str(need_profiles)
            if offset:
                params["offset"] = vk_str(offset)
            return self.do_request(params)

            
        def delete(self, qid):
            params = {
                'method': "questions.delete",
                'qid': vk_str(qid),
            }
            return self.do_request(params)


            
    def get_variable(self, key, user_id=None, session=None):
        params = {
            'method': "getVariable",
            'key': vk_str(key),
        }
        if user_id:
            params["user_id"] = vk_str(user_id)
        if session:
            params["session"] = vk_str(session)
        return self.do_request(params)

            
    def get_groups(self):
        params = {
            'method': "getGroups",
        }
        return self.do_request(params)

            
    def set_user_score(self, score):
        params = {
            'method': "setUserScore",
            'score': vk_str(score),
        }
        return self.do_request(params)

            
    def get_countries(self, cids):
        params = {
            'method': "getCountries",
            'cids': vk_strlist(cids),
        }
        return self.do_request(params)

            
    def set_sms_prefix(self, prefix):
        params = {
            'method': "setSMSPrefix",
            'prefix': vk_str(prefix),
        }
        return self.do_request(params)

            
    def get_user_info(self):
        params = {
            'method': "getUserInfo",
        }
        return self.do_request(params)

            
    def is_app_user(self, uid=None):
        params = {
            'method': "isAppUser",
        }
        if uid:
            params["uid"] = vk_str(uid)
        return self.do_request(params)

            
    def parse_wiki(self, Text):
        params = {
            'method': "parseWiki",
            'Text': vk_str(Text),
        }
        return self.do_request(params)

            
    class __offers(object):
        def __init__(self, parent):
            self.secret = parent.secret
            self.user_id = parent.user_id
            self.viewer_id = parent.viewer_id
            self.api_url = parent.api_url
            self.test_mode = parent.test_mode
            self.api_args = parent.api_args
            self._build_sig = parent._build_sig
            self._build_url = parent._build_url
            self.send = parent.send
            self.do_request = parent.do_request

            
        def search(self, interests=None, text=None, sex=None, city=None, age_from=None, district=None, religion=None, station=None, online=None, edu_form=None, status=None, edu_status=None, photo=None, age_to=None, company=None, group=None, count=None, school=None, name=None, country=None, university=None, politic=None, position=None):
            params = {
                'method': "offers.search",
            }
            if interests:
                params["interests"] = vk_str(interests)
            if text:
                params["text"] = vk_str(text)
            if sex:
                params["sex"] = vk_str(sex)
            if city:
                params["city"] = vk_str(city)
            if age_from:
                params["age_from"] = vk_str(age_from)
            if district:
                params["district"] = vk_str(district)
            if religion:
                params["religion"] = vk_str(religion)
            if station:
                params["station"] = vk_str(station)
            if online:
                params["online"] = vk_str(online)
            if edu_form:
                params["edu_form"] = vk_str(edu_form)
            if status:
                params["status"] = vk_str(status)
            if edu_status:
                params["edu_status"] = vk_str(edu_status)
            if photo:
                params["photo"] = vk_str(photo)
            if age_to:
                params["age_to"] = vk_str(age_to)
            if company:
                params["company"] = vk_str(company)
            if group:
                params["group"] = vk_str(group)
            if count:
                params["count"] = vk_str(count)
            if school:
                params["school"] = vk_str(school)
            if name:
                params["name"] = vk_str(name)
            if country:
                params["country"] = vk_str(country)
            if university:
                params["university"] = vk_str(university)
            if politic:
                params["politic"] = vk_str(politic)
            if position:
                params["position"] = vk_str(position)
            return self.do_request(params)

            
        def get(self, uids=None):
            params = {
                'method': "offers.get",
            }
            if uids:
                params["uids"] = vk_strlist(uids)
            return self.do_request(params)

            
        def edit(self, message):
            params = {
                'method': "offers.edit",
                'message': vk_str(message),
            }
            return self.do_request(params)

            
        def get_inbound_responses(self, count=None, offset=None):
            params = {
                'method': "offers.getInboundResponses",
            }
            if count:
                params["count"] = vk_str(count)
            if offset:
                params["offset"] = vk_str(offset)
            return self.do_request(params)

            
        def refuse(self, uid):
            params = {
                'method': "offers.refuse",
                'uid': vk_str(uid),
            }
            return self.do_request(params)

            
        def accept(self, uid):
            params = {
                'method': "offers.accept",
                'uid': vk_str(uid),
            }
            return self.do_request(params)

            
        def get_outbound_responses(self, count=None, offset=None):
            params = {
                'method': "offers.getOutboundResponses",
            }
            if count:
                params["count"] = vk_str(count)
            if offset:
                params["offset"] = vk_str(offset)
            return self.do_request(params)

            
        def set_response_viewed(self, uids):
            params = {
                'method': "offers.setResponseViewed",
                'uids': vk_strlist(uids),
            }
            return self.do_request(params)

            
        def delete_responses(self, uids):
            params = {
                'method': "offers.deleteResponses",
                'uids': vk_strlist(uids),
            }
            return self.do_request(params)

            
        def close(self):
            params = {
                'method': "offers.close",
            }
            return self.do_request(params)

            
        def open(self):
            params = {
                'method': "offers.open",
            }
            return self.do_request(params)


            
    def get_sms_prefix(self):
        params = {
            'method': "getSMSPrefix",
        }
        return self.do_request(params)

            
    def get_user_info_ex(self):
        params = {
            'method': "getUserInfoEx",
        }
        return self.do_request(params)

            
    def get_messages(self, messages_to_get=None, session=None):
        params = {
            'method': "getMessages",
        }
        if messages_to_get:
            params["messages_to_get"] = vk_str(messages_to_get)
        if session:
            params["session"] = vk_str(session)
        return self.do_request(params)

            
    def get_server_time(self):
        params = {
            'method': "getServerTime",
        }
        return self.do_request(params)

            
    def get_groups_full(self, gids):
        params = {
            'method': "getGroupsFull",
            'gids': vk_strlist(gids),
        }
        return self.do_request(params)

            
    class __language(object):
        def __init__(self, parent):
            self.secret = parent.secret
            self.user_id = parent.user_id
            self.viewer_id = parent.viewer_id
            self.api_url = parent.api_url
            self.test_mode = parent.test_mode
            self.api_args = parent.api_args
            self._build_sig = parent._build_sig
            self._build_url = parent._build_url
            self.send = parent.send
            self.do_request = parent.do_request

            
        def get_values(self, keys=None, all=None, language=None):
            params = {
                'method': "language.getValues",
            }
            if keys:
                params["keys"] = vk_str(keys)
            if all:
                params["all"] = vk_str(all)
            if language:
                params["language"] = vk_str(language)
            return self.do_request(params)


            
    class __photos(object):
        def __init__(self, parent):
            self.secret = parent.secret
            self.user_id = parent.user_id
            self.viewer_id = parent.viewer_id
            self.api_url = parent.api_url
            self.test_mode = parent.test_mode
            self.api_args = parent.api_args
            self._build_sig = parent._build_sig
            self._build_url = parent._build_url
            self.send = parent.send
            self.do_request = parent.do_request

            
        def edit_album(self, aid, title, description=None, privacy=None, comment_privacy=None):
            params = {
                'method': "photos.editAlbum",
                'title': vk_str(title),
                'aid': vk_str(aid),
            }
            if description:
                params["description"] = vk_str(description)
            if privacy:
                params["privacy"] = vk_str(privacy)
            if comment_privacy:
                params["comment_privacy"] = vk_str(comment_privacy)
            return self.do_request(params)

            
        def create_album(self, title, description=None, privacy=None, comment_privacy=None):
            params = {
                'method': "photos.createAlbum",
                'title': vk_str(title),
            }
            if description:
                params["description"] = vk_str(description)
            if privacy:
                params["privacy"] = vk_str(privacy)
            if comment_privacy:
                params["comment_privacy"] = vk_str(comment_privacy)
            return self.do_request(params)

            
        def reorder_albums(self, aid, after, before, oid=None):
            params = {
                'method': "photos.reorderAlbums",
                'aid': vk_str(aid),
                'after': vk_str(after),
                'before': vk_str(before),
            }
            if oid:
                params["oid"] = vk_str(oid)
            return self.do_request(params)

            
        def get(self, aid, uid, pids=None):
            params = {
                'method': "photos.get",
                'aid': vk_str(aid),
                'uid': vk_str(uid),
            }
            if pids:
                params["pids"] = vk_strlist(pids)
            return self.do_request(params)

            
        def make_cover(self, aid, pid, oid=None):
            params = {
                'method': "photos.makeCover",
                'pid': vk_str(pid),
                'aid': vk_str(aid),
            }
            if oid:
                params["oid"] = vk_str(oid)
            return self.do_request(params)

            
        def get_albums(self, aids=None, uid=None):
            params = {
                'method': "photos.getAlbums",
            }
            if aids:
                params["aids"] = vk_strlist(aids)
            if uid:
                params["uid"] = vk_str(uid)
            return self.do_request(params)

            
        def move(self, pid, target_aid, oid=None):
            params = {
                'method': "photos.move",
                'pid': vk_str(pid),
                'target_aid': vk_str(target_aid),
            }
            if oid:
                params["oid"] = vk_str(oid)
            return self.do_request(params)

            
        def reorder_photos(self, after, pid, before, oid=None):
            params = {
                'method': "photos.reorderPhotos",
                'pid': vk_str(pid),
                'after': vk_str(after),
                'before': vk_str(before),
            }
            if oid:
                params["oid"] = vk_str(oid)
            return self.do_request(params)

            
        def save_profile_photo(self, photo, hash, server):
            params = {
                'method': "photos.saveProfilePhoto",
                'photo': vk_str(photo),
                'hash': vk_str(hash),
                'server': vk_str(server),
            }
            return self.do_request(params)

            
        def get_by_id(self, photos=None):
            params = {
                'method': "photos.getById",
            }
            if photos:
                params["photos"] = vk_str(photos)
            return self.do_request(params)

            
        def save(self, aid, hash, photos_list, server):
            params = {
                'method': "photos.save",
                'aid': vk_str(aid),
                'photos_list': vk_str(photos_list),
                'hash': vk_str(hash),
                'server': vk_str(server),
            }
            return self.do_request(params)

            
        def get_profile_upload_server(self):
            params = {
                'method': "photos.getProfileUploadServer",
            }
            return self.do_request(params)

            
        def get_upload_server(self, aid, save_big=None):
            params = {
                'method': "photos.getUploadServer",
                'aid': vk_str(aid),
            }
            if save_big:
                params["save_big"] = vk_str(save_big)
            return self.do_request(params)


            
    def get_user_balance(self):
        params = {
            'method': "getUserBalance",
        }
        return self.do_request(params)

            
    def get_high_scores(self):
        params = {
            'method': "getHighScores",
        }
        return self.do_request(params)

            
    class __friends(object):
        def __init__(self, parent):
            self.secret = parent.secret
            self.user_id = parent.user_id
            self.viewer_id = parent.viewer_id
            self.api_url = parent.api_url
            self.test_mode = parent.test_mode
            self.api_args = parent.api_args
            self._build_sig = parent._build_sig
            self._build_url = parent._build_url
            self.send = parent.send
            self.do_request = parent.do_request

            
        def get_app_users(self):
            params = {
                'method': "friends.getAppUsers",
            }
            return self.do_request(params)

            
        def get(self, fields=None, name_case=None):
            params = {
                'method': "friends.get",
            }
            if fields:
                params["fields"] = vk_str(fields)
            if name_case:
                params["name_case"] = vk_str(name_case)
            return self.do_request(params)


            
    class __pages(object):
        def __init__(self, parent):
            self.secret = parent.secret
            self.user_id = parent.user_id
            self.viewer_id = parent.viewer_id
            self.api_url = parent.api_url
            self.test_mode = parent.test_mode
            self.api_args = parent.api_args
            self._build_sig = parent._build_sig
            self._build_url = parent._build_url
            self.send = parent.send
            self.do_request = parent.do_request

            
        def save(self, Text, gid, pid):
            params = {
                'method': "pages.save",
                'pid': vk_str(pid),
                'gid': vk_str(gid),
                'Text': vk_str(Text),
            }
            return self.do_request(params)

            
        def get(self, gid, pid, need_html=None):
            params = {
                'method': "pages.get",
                'pid': vk_str(pid),
                'gid': vk_str(gid),
            }
            if need_html:
                params["need_html"] = vk_str(need_html)
            return self.do_request(params)

            
        def get_version(self, gid, hid, need_html=None):
            params = {
                'method': "pages.getVersion",
                'hid': vk_str(hid),
                'gid': vk_str(gid),
            }
            if need_html:
                params["need_html"] = vk_str(need_html)
            return self.do_request(params)

            
        def get_titles(self, gid):
            params = {
                'method': "pages.getTitles",
                'gid': vk_str(gid),
            }
            return self.do_request(params)

            
        def get_history(self, gid, pid):
            params = {
                'method': "pages.getHistory",
                'pid': vk_str(pid),
                'gid': vk_str(gid),
            }
            return self.do_request(params)

            
        def save_access(self, edit, gid, pid, view):
            params = {
                'method': "pages.saveAccess",
                'edit': vk_str(edit),
                'pid': vk_str(pid),
                'gid': vk_str(gid),
                'view': vk_str(view),
            }
            return self.do_request(params)


            
    def execute(self, code):
        params = {
            'method': "execute",
            'code': vk_str(code),
        }
        return self.do_request(params)

            
    def set_name_in_menu(self, name):
        params = {
            'method': "setNameInMenu",
            'name': vk_str(name),
        }
        return self.do_request(params)

            
    def put_variable(self, key, value, user_id=None, session=None):
        params = {
            'method': "putVariable",
            'value': vk_str(value),
            'key': vk_str(key),
        }
        if user_id:
            params["user_id"] = vk_str(user_id)
        if session:
            params["session"] = vk_str(session)
        return self.do_request(params)

            
    class __notes(object):
        def __init__(self, parent):
            self.secret = parent.secret
            self.user_id = parent.user_id
            self.viewer_id = parent.viewer_id
            self.api_url = parent.api_url
            self.test_mode = parent.test_mode
            self.api_args = parent.api_args
            self._build_sig = parent._build_sig
            self._build_url = parent._build_url
            self.send = parent.send
            self.do_request = parent.do_request

            
        def get(self, sort=None, count=None, uid=None, nids=None, offset=None):
            params = {
                'method': "notes.get",
            }
            if sort:
                params["sort"] = vk_str(sort)
            if count:
                params["count"] = vk_str(count)
            if uid:
                params["uid"] = vk_str(uid)
            if nids:
                params["nids"] = vk_strlist(nids)
            if offset:
                params["offset"] = vk_str(offset)
            return self.do_request(params)

            
        def create_comment(self, message, nid, reply_to=None, owner_id=None):
            params = {
                'method': "notes.createComment",
                'message': vk_str(message),
                'nid': vk_str(nid),
            }
            if reply_to:
                params["reply_to"] = vk_str(reply_to)
            if owner_id:
                params["owner_id"] = vk_str(owner_id)
            return self.do_request(params)

            
        def get_friends_notes(self, count=None, offset=None):
            params = {
                'method': "notes.getFriendsNotes",
            }
            if count:
                params["count"] = vk_str(count)
            if offset:
                params["offset"] = vk_str(offset)
            return self.do_request(params)

            
        def edit_comment(self, message, cid, owner_id=None):
            params = {
                'method': "notes.editComment",
                'message': vk_str(message),
                'cid': vk_str(cid),
            }
            if owner_id:
                params["owner_id"] = vk_str(owner_id)
            return self.do_request(params)

            
        def delete_comment(self, cid, owner_id=None):
            params = {
                'method': "notes.deleteComment",
                'cid': vk_str(cid),
            }
            if owner_id:
                params["owner_id"] = vk_str(owner_id)
            return self.do_request(params)

            
        def restore_comment(self, cid, owner_id=None):
            params = {
                'method': "notes.restoreComment",
                'cid': vk_str(cid),
            }
            if owner_id:
                params["owner_id"] = vk_str(owner_id)
            return self.do_request(params)

            
        def edit(self, text, nid, title, privacy=None, comment_privacy=None):
            params = {
                'method': "notes.edit",
                'text': vk_str(text),
                'title': vk_str(title),
                'nid': vk_str(nid),
            }
            if privacy:
                params["privacy"] = vk_str(privacy)
            if comment_privacy:
                params["comment_privacy"] = vk_str(comment_privacy)
            return self.do_request(params)

            
        def add(self, text, title, privacy=None, comment_privacy=None):
            params = {
                'method': "notes.add",
                'text': vk_str(text),
                'title': vk_str(title),
            }
            if privacy:
                params["privacy"] = vk_str(privacy)
            if comment_privacy:
                params["comment_privacy"] = vk_str(comment_privacy)
            return self.do_request(params)

            
        def get_comments(self, nid, sort=None, count=None, offset=None, owner_id=None):
            params = {
                'method': "notes.getComments",
                'nid': vk_str(nid),
            }
            if sort:
                params["sort"] = vk_str(sort)
            if count:
                params["count"] = vk_str(count)
            if offset:
                params["offset"] = vk_str(offset)
            if owner_id:
                params["owner_id"] = vk_str(owner_id)
            return self.do_request(params)

            
        def get_by_id(self, nid, need_wiki=None, owner_id=None):
            params = {
                'method': "notes.getById",
                'nid': vk_str(nid),
            }
            if need_wiki:
                params["need_wiki"] = vk_str(need_wiki)
            if owner_id:
                params["owner_id"] = vk_str(owner_id)
            return self.do_request(params)

            
        def delete(self, nid):
            params = {
                'method': "notes.delete",
                'nid': vk_str(nid),
            }
            return self.do_request(params)


            
    def get_variables(self, count, key, user_id=None, session=None):
        params = {
            'method': "getVariables",
            'count': vk_str(count),
            'key': vk_str(key),
        }
        if user_id:
            params["user_id"] = vk_str(user_id)
        if session:
            params["session"] = vk_str(session)
        return self.do_request(params)

            
    def get_ads(self, count=None, type=None, apps_ids=None, min_price=None):
        params = {
            'method': "getAds",
        }
        if count:
            params["count"] = vk_str(count)
        if type:
            params["type"] = vk_str(type)
        if apps_ids:
            params["apps_ids"] = vk_strlist(apps_ids)
        if min_price:
            params["min_price"] = vk_str(min_price)
        return self.do_request(params)

            
    def get_cities(self, cids):
        params = {
            'method': "getCities",
            'cids': vk_strlist(cids),
        }
        return self.do_request(params)

            
    def get_profiles(self, uids, fields=None, name_case=None):
        params = {
            'method': "getProfiles",
            'uids': vk_strlist(uids),
        }
        if fields:
            params["fields"] = vk_str(fields)
        if name_case:
            params["name_case"] = vk_str(name_case)
        return self.do_request(params)

            
    class __activity(object):
        def __init__(self, parent):
            self.secret = parent.secret
            self.user_id = parent.user_id
            self.viewer_id = parent.viewer_id
            self.api_url = parent.api_url
            self.test_mode = parent.test_mode
            self.api_args = parent.api_args
            self._build_sig = parent._build_sig
            self._build_url = parent._build_url
            self.send = parent.send
            self.do_request = parent.do_request

            
        def get_history(self, uid=None):
            params = {
                'method': "activity.getHistory",
            }
            if uid:
                params["uid"] = vk_str(uid)
            return self.do_request(params)

            
        def set(self, text):
            params = {
                'method': "activity.set",
                'text': vk_str(text),
            }
            return self.do_request(params)

            
        def delete_history_item(self, aid):
            params = {
                'method': "activity.deleteHistoryItem",
                'aid': vk_str(aid),
            }
            return self.do_request(params)

            
        def get_news(self, count=None, timestamp=None, offset=None):
            params = {
                'method': "activity.getNews",
            }
            if count:
                params["count"] = vk_str(count)
            if timestamp:
                params["timestamp"] = vk_str(timestamp)
            if offset:
                params["offset"] = vk_str(offset)
            return self.do_request(params)

            
        def get(self, uid=None):
            params = {
                'method': "activity.get",
            }
            if uid:
                params["uid"] = vk_str(uid)
            return self.do_request(params)


            
    class __audio(object):
        def __init__(self, parent):
            self.secret = parent.secret
            self.user_id = parent.user_id
            self.viewer_id = parent.viewer_id
            self.api_url = parent.api_url
            self.test_mode = parent.test_mode
            self.api_args = parent.api_args
            self._build_sig = parent._build_sig
            self._build_url = parent._build_url
            self.send = parent.send
            self.do_request = parent.do_request

            
        def restore(self, aid, oid=None):
            params = {
                'method': "audio.restore",
                'aid': vk_str(aid),
            }
            if oid:
                params["oid"] = vk_str(oid)
            return self.do_request(params)

            
        def search(self, q, sort=None, count=None, lyrics=None, offset=None):
            params = {
                'method': "audio.search",
                'q': vk_str(q),
            }
            if sort:
                params["sort"] = vk_str(sort)
            if count:
                params["count"] = vk_str(count)
            if lyrics:
                params["lyrics"] = vk_str(lyrics)
            if offset:
                params["offset"] = vk_str(offset)
            return self.do_request(params)

            
        def save(self, audio, hash, server, title=None, artist=None):
            params = {
                'method': "audio.save",
                'hash': vk_str(hash),
                'server': vk_str(server),
                'audio': vk_str(audio),
            }
            if title:
                params["title"] = vk_str(title)
            if artist:
                params["artist"] = vk_str(artist)
            return self.do_request(params)

            
        def get(self, need_user=None, aids=None, gid=None, uid=None):
            params = {
                'method': "audio.get",
            }
            if need_user:
                params["need_user"] = vk_str(need_user)
            if aids:
                params["aids"] = vk_strlist(aids)
            if gid:
                params["gid"] = vk_str(gid)
            if uid:
                params["uid"] = vk_str(uid)
            return self.do_request(params)

            
        def edit(self, artist, text, oid, title, aid, no_search):
            params = {
                'method': "audio.edit",
                'title': vk_str(title),
                'text': vk_str(text),
                'oid': vk_str(oid),
                'aid': vk_str(aid),
                'artist': vk_str(artist),
                'no_search': vk_str(no_search),
            }
            return self.do_request(params)

            
        def get_lyrics(self, lyrics_id=None):
            params = {
                'method': "audio.getLyrics",
            }
            if lyrics_id:
                params["lyrics_id"] = vk_str(lyrics_id)
            return self.do_request(params)

            
        def add(self, aid, oid, gid):
            params = {
                'method': "audio.add",
                'aid': vk_str(aid),
                'oid': vk_str(oid),
                'gid': vk_str(gid),
            }
            return self.do_request(params)

            
        def get_by_id(self, audios=None):
            params = {
                'method': "audio.getById",
            }
            if audios:
                params["audios"] = vk_str(audios)
            return self.do_request(params)

            
        def delete(self, aid, oid):
            params = {
                'method': "audio.delete",
                'aid': vk_str(aid),
                'oid': vk_str(oid),
            }
            return self.do_request(params)

            
        def reorder(self, aid, after, before, oid=None):
            params = {
                'method': "audio.reorder",
                'aid': vk_str(aid),
                'after': vk_str(after),
                'before': vk_str(before),
            }
            if oid:
                params["oid"] = vk_str(oid)
            return self.do_request(params)

            
        def get_upload_server(self):
            params = {
                'method': "audio.getUploadServer",
            }
            return self.do_request(params)











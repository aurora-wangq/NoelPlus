import json

class MessageSegment(dict):
    def __init__(self, type = '', data = {}):
        self['type'] = type
        self['data'] = data
    
    def __str__(self):
        return json.dumps(self)
    
    def text(s):
        return MessageSegment('text', s)
    
    def mention(s):
        return MessageSegment('mention', s)

    def image(img):
        return MessageSegment('image', img)
    
    def ncm(id):
        return MessageSegment('ncm', id)
        
class Message(dict):
    def __init__(self, msg, sender):
        if isinstance(msg, list) or isinstance(msg, Message):
            self['message'] = msg
        elif isinstance(msg, MessageSegment):
            self['message'] = [ msg ]
        elif isinstance(msg, str):
            self['message'] = [ MessageSegment.text(msg) ]
        else:
            raise NotImplementedError("Unknown type")
        self['sender'] = sender

    def __str__(self):
        return json.dumps([ x for x in self])
    
class Event(dict):
    def __init__(self, type, data):
        self['type'] = type
        self['data'] = data
    
    def __str__(self) -> str:
        return json.dumps(self)
    
    def message(msg: Message):
        return Event('message', msg)
    
    def modification(data):
        return Event('modification', data)

    def notice(s: str):
        return Event('notice', s)
    
    def info(s: str):
        return Event('info', s)
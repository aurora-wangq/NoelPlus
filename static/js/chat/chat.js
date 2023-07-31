var quill = new Quill('.editor', {
    modules: {
        toolbar: {
            container: '#quill-toolbar'
        }
    },
    theme: 'snow',
    placeholder: '阿巴阿巴（°∀。）...\n不要从外部直接拖入图片哦，点击上方图片标志选择图片'
});


document.querySelector('.mention-button').addEventListener('click', e => {
    let value = prompt('输入要提及的用户名');
    let index = 0;

    if (value === null) {
        return;
    }
    if (quill.getSelection()) {
        index = quill.getSelection().index;
    }
    else {
        index = quill.getLength();
    }

    quill.updateContents(new Delta().retain(index).insert({
        'mention': value
    }), Quill.sources.USER);

    quill.setSelection(index + 1, 0);
});

document.getElementById('insert-ncm-button').addEventListener('click', e => {
    let s = document.getElementById('insert-ncm-input').value;
    let value, index;

    if (s == '') {
        return;
    }
    if (quill.getSelection()) {
        index = quill.getSelection().index;
    }
    else {
        index = quill.getLength();
    }

    if (/^\d+$/.test(value)) {
        value = s;
    }
    else if (s.match(/https:\/\/music\.163\.com\/(#\/)?song\?id=\d+(&userid=\d+)?/)) {
        value = s.match(/song\?id=(\d+)/)[1];
    }
    else {
        mdui.snackbar('未知的ID或链接格式');
        return;
    }

    quill.updateContents(new Delta().retain(index).insert({
        'ncm': value
    }), Quill.sources.USER);

    quill.setSelection(index + 1, 0);

});

var font_sizes = {
    "normal": "1.0em",
    "small": "0.75em",
    "large": "1.5em",
    "huge": "2.5em"
};

function validateImage(src) {
    if (src.startsWith('file:///')) {
        return false;
    }
    else if (src.startsWith('data:image/') && src.indexOf('base64') != -1) {
        return true;
    }
    else {
        return false;
    }
}

class Message {
    constructor() {
        this.messageContainer = document.createElement('div');
        this.messageContainer.classList.add('mdui-row', 'message-content', 'mdui-col-offset-xs-1');
        this.headerContainer = document.createElement('div');
        this.headerContainer.classList.add('mdui-row', 'message-header');
    }

    static col(element, ...column) {
        var div = document.createElement('div');
        div.classList.add(...column.map(x => 'mdui-col-' + x));
        div.appendChild(element);
        return div;
    }

    setSender(sender) {
        if (sender.avatar) {
            var avatar = document.createElement('img');
            avatar.classList.add('message-avatar', 'mdui-center');
            avatar.setAttribute('source-user', sender.username);
            avatar.src = '/media/' + sender.avatar;
            avatar.addEventListener('dblclick', e => {
                let sel = quill.getSelection();
                if (sel) {
                    quill.updateContents(new Delta().retain(sel.index).insert({
                        'mention': e.target.getAttribute('source-user')
                    }), 'user');
                    quill.setSelection(sel.index + 1);
                }
                else {
                    quill.updateContents(new Delta().retain(quill.getLength() - 1).insert({
                        'mention': e.target.getAttribute('source-user')
                    }), 'user');
                    quill.setSelection(quill.getLength() - 1);
                }
            });
            this.headerContainer.appendChild(Message.col(avatar, 'md-1', 'xs-2'));
        }
        var col = document.createElement('div');
        col.classList.add('mdui-col-md-11', 'mdui-col-xs-10', 'mdui-valign');
        if (sender.username) {
            var username = document.createElement('span');
            username.innerText = '@' + sender.username;
            username.classList.add('message-username');
            col.appendChild(username);
        }
        if (sender.title) {
            var title = document.createElement('span');
            title.classList.add('user-title', 'user-title-level-' + sender.title_level);
            title.innerText = sender.title;
            col.appendChild(title);
        }
        this.headerContainer.appendChild(col);
    }

    appendText(text, attr) {
        var tag = document.createElement('span');
        tag.innerText = text;
        if (attr) {
            var createParent = (tag, child, ...attributes) => {
                var parent = document.createElement(tag);
                parent.appendChild(child);
                for (var name in attributes) {
                    parent.setAttribute(name, attributes[name]);
                }
                return parent;
            }
            if (attr.bold) {
                tag = createParent('b', tag);
            }
            if (attr.underline) {
                tag = createParent('u', tag);
            }
            if (attr.italic) {
                tag = createParent('i', tag);
            }
            if (attr.link) {
                tag = createParent('a', tag, { 'href': attr.link });
            }
            if (attr.strike) {
                tag = createParent('s', tag);
            }
            if (attr.size) {
                tag.style.fontSize = font_sizes[attr.size];
            }
        }
        this.messageContainer.appendChild(tag);
    }

    appendMention(text) {
        var span = document.createElement('span');
        span.classList.add('mention');
        if (text == sender.data.username) {
            span.classList.add('mention-hit');
        }
        span.innerText = '@' + text;
        this.messageContainer.appendChild(span);
    }

    appendImage(src) {
        var img = document.createElement('img');
        img.setAttribute('src', src);
        this.messageContainer.appendChild(img);
    }

    appendNCM(id) {
        var iframe = document.createElement('iframe');
        iframe.classList.add('ncm-player');
        iframe.setAttribute('width', '330');
        iframe.setAttribute('height', '86');
        iframe.setAttribute('marginwidth', '0');
        iframe.setAttribute('marginheight', '0');
        iframe.src = `//music.163.com/outchain/player?type=2&id=${id}&auto=0&height=66`;
        this.messageContainer.appendChild(iframe);
    }

    get empty() {
        return this.messageContainer.children.length == 0;
    }

    get container() {
        if (this.messageContainer.children.length == 0) {
            return null;
        }
        var container = document.createElement('div');
        container.classList.add('mdui-container', 'message');
        if (this.headerContainer.children.length) {
            container.appendChild(this.headerContainer);
        }
        container.appendChild(this.messageContainer);
        return container;
    }
}

class Sender {
    #username = document.getElementById('input-username').value;
    #nickname = document.getElementById('input-nickname').value;
    #avatar = document.getElementById('input-useravatar').value;
    #title = document.getElementById('input-usertitle').value;
    #title_level = document.getElementById('input-usertitle_level').value;

    constructor() { }

    get data() {
        return {
            username: this.#username,
            nickname: this.#nickname,
            avatar: this.#avatar,
            title: this.#title,
            title_level: this.#title_level
        }
    }
}

if (location.port) {
    path = `${location.hostname}:${location.port}/room/1/`;
}
else {
    path = `${location.hostname}/room/1/`;
}

var socket = new WebSocket(`ws://${path}`);
var sender = new Sender();
var lastSender = null;
var loading = false;

socket.onmessage = function (event) {
    var _ = JSON.parse(event.data);
    var type = _.type;
    var data = _.data;

    if (type == 'info') {
        if (data == 'history.begin') {
            loading = true;
        }
        if (data == 'history.end') {
            document.querySelector('.status-indicator-ready').classList.toggle('mdui-hidden');
            document.querySelector('.status-indicator-loading').classList.toggle('mdui-hidden');
            loading = false;
        }
    }
    else if (type == 'notice') {
        lastSender = null;
        var base = document.createElement('div');
        base.classList.add('notice');
        base.appendChild(document.createTextNode(data));
        document.querySelector('.message-container').appendChild(base);
    }
    else if (type == 'message') {
        msg = new Message();
        if (data.sender && data.sender.username != lastSender) {
            msg.setSender(data.sender);
            lastSender = data.sender.username;
        }
        data.message.forEach(i => {
            if (i.type == 'text') {
                msg.appendText(i.data, i.attr)
            }
            else if (i.type == 'mention') {
                msg.appendMention(i.data);
            }
            else if (i.type == 'image') {
                msg.appendImage(i.data);
            }
            else if (i.type == 'ncm') {
                msg.appendNCM(i.data);
            }
        });

        if (msg.empty) return;

        document.querySelector('.message-container').appendChild(msg.container);
    }

    if (document.getElementById('autoscroll-checkbox').checked) {
        var elem = document.querySelector('.message-container');
        if (loading) {
            elem.scroll({
                top: elem.scrollHeight,
                behavior: 'instant'
            });
        }
        else {
            elem.scroll({
                top: elem.scrollHeight,
                behavior: 'smooth'
            });
        }
    }
}

document.querySelector('.editor').addEventListener('keydown', (e) => {
    if (e.key == 'Enter' && e.ctrlKey) {
        document.getElementById('send-button').click();
    }
});

socket.onopen = function (event) {
    socket.send(JSON.stringify({
        "type": "init",
        "data": {
            "sender": sender.data
        }
    }));
}

socket.onclose = function (event) {
    document.querySelector('.status-indicator-ready').classList.toggle('mdui-hidden');
    document.querySelector('.status-indicator-fail').classList.toggle('mdui-hidden');
    quill.disable();
}

function send() {
    let delta = quill.getContents();
    msg = [];
    if (delta.ops.length == 1 && delta.ops[0].insert.trim().length == 0) {
        mdui.snackbar('消息不能为空');
        return;
    }
    delta.ops.forEach(x => {
        if (x.insert.image) {
            if (!validateImage(x.insert.image)) {
                mdui.snackbar('Unrecognized image');
                return;
            }
            msg.push({
                'type': 'image',
                'data': x.insert.image
            });
        }
        else if (x.insert.mention) {
            msg.push({
                'type': 'mention',
                'data': x.insert.mention
            });
        }
        else if (x.insert.ncm) {
            msg.push({
                'type': 'ncm',
                'data': x.insert.ncm
            });
        }
        else if (typeof x.insert == 'string') {
            msg.push({
                'type': 'text',
                'data': x.insert,
                'attr': x.attributes
            });
        }
    });
    socket.send(JSON.stringify({
        "type": "message",
        "data": {
            "sender": sender.data,
            "message": msg
        }
    }));
    quill.deleteText(0, quill.getLength());
}

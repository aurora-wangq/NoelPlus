let Embed = Quill.import('blots/embed');
let Delta = Quill.import('delta');
let Icon = Quill.import('ui/icons');

class Mention extends Embed {
    static create(value) {
        let node = super.create();
        node.setAttribute('mention', value);
        node.innerText = '@' + value;
        return node;
    }

    static value(node) {
        return node.attributes.mention.value;
    }
}
Mention.blotName = 'mention';
Mention.tagName = 'span';
Mention.className = 'mention';

class NCMPlayer extends Embed {
    static create(value) {
        let node = super.create();
        node.setAttribute('ncmid', value);
        node.classList.add('ncm-player');
        node.setAttribute('width', '330');
        node.setAttribute('height', '86');
        node.setAttribute('marginwidth', '0');
        node.setAttribute('marginheight', '0');
        node.setAttribute('src', `//music.163.com/outchain/player?type=2&id=${value}&auto=0`);
        return node;
    }

    static value(node) {
        return node.attributes.ncmid.value;
    }
}

NCMPlayer.blotName = 'ncm';
NCMPlayer.tagName = 'iframe';

Quill.register(Mention);
Quill.register(NCMPlayer);

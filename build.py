"""Build mypy website (html and css).

Use Python 2 to run this.

Needs sass. Use "sudo gem install sass" to install.

NOTES:

This is pretty crufty and was originally translated from an old script
written in Alore. Much of this doesn't make sense any more.
"""

import shutil
from re import sub, DOTALL, match, search
import re
import subprocess
from textwrap import dedent

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

news_items = load(open('news.yaml'), Loader=Loader)['items']

pages = ['index', 'examples', 'tutorial', 'about', 'news', 'faq', 'contact',
         'roadmap', 'news',

         'overview'  # legacy
         ]
files = ['site.css']
static_dirs = ['static']

out_dir = 'out'

default_title = 'mypy'
default_keywords = 'mypy, python static typing, python optional typing'
default_description = 'Mypy is an experimental Python variant with seamless dynamic and static typing.'

KW = ['class', 'for', 'in', 'return', 'if', 'else', 'void', 'pass',
      'def', 'any', 'member', 'while', 'static', 'import', 'raise', 'not',
      'yield', 'break', 'interface', 'from', 'with', 'as']

def build_page(p):
    t = open('template.html').read()
    content = open('%s.html' % p).read()
    content, meta = format_content(content)
    t = t.replace('$content$', content)
    t = t.replace('$title$', meta.get('title', default_title))
    t = t.replace('$keywords$', meta.get('keywords', default_keywords))
    t = t.replace('$description$', meta.get('description',
                                            default_description))
    if '$contents' in t:
        t = t.replace('$contents$', build_contents(t))
    if '$latestnews$' in t:
        t = t.replace('$latestnews$', build_latest_news())
    if '$news$' in t:
        t = t.replace('$news$', build_news())
    f = open('%s/%s.html' % (out_dir, p), 'w')
    f.write(t)
    f.close()


def format_content(s):
    meta = {}

    s = sub(r'\$code!([^!]*)!', lambda m: render_code(m.group(1)),
            s, flags=DOTALL)
    s = sub(r'\$email\(([^)]*)\)\$', lambda m: obfuscate_email(m.group(1)), s)
    s = sub(r'\$include\(([^)]*)\)\$', lambda m: include(m.group(1)), s)
    s = sub(r'\$example\(([^)]*)\)\$', lambda m: example(m.group(1)), s)

    for tag in 'title', 'keywords', 'description':
        m = search(r'\$%s ([^$]*)\$' % tag, s)
        if m:
            meta[tag] = m.group(1)
            s = s.replace(m.group(), '')

    return s, meta

def render_code(s):
    s = s.rstrip()
    s = dedent(s)
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')

    for kw in KW:
        s = sub(r'\b%s\b' % kw, r'<span class="kw">%s</span>' % kw, s)

    for kw in ('list', 'str', 'print', 'int', 'float', 'tuple', 'bool',
               'bytes', 'dict', 'object', 'Dict', 'List', 'Iterator', 'Any',
               'Set', 'typevar', 'Generic', 'Iterable', 'Sequence'):
        s = sub(r'\b%s\b' % kw, r'<span class="pr">%s</span>' % kw, s)

    s = sub(r"('[^']*')", r'<span class="st">\1</span>', s)
    s = sub(r'(""".*""")', r'<span class="st">\1</span>', s, flags=DOTALL)

    s = sub(r'(#.*)', r'<span class="co">\1</span>', s)
    s = sub(r'(""".*?""")', r'<span class="st">\1</span>', s)

    s = sub(r'\|\|(.*?)\|\|', r'<span class="hili">\1</span>', s)

    return '<pre class="ex">%s</pre>' % s


def include(fnam):
    return open(fnam, 'r').read()


def example(fnam):
    f1 = render_code(open('demo/%s.py' % fnam, 'r').read())
    f2 = render_code(open('demo/%s-s.py' % fnam, 'r').read())
    return '''
    <div class="ex-left">
    <div class="sample-header">Mypy with dynamic typing</div>
    %s
    </div>
    <div class="ex-right">
    <div class="sample-header">Mypy with static typing</div>
    %s
    </div>
    <div class="clear"></div>
    ''' % (f1, f2)


def build_contents(t):
    """Collect all <h2> titles using a regxp and build <li> items."""
    res = []
    for id, text in re.findall(r'<h2(.*?)>(.*?)</h2>', t):
        if text != 'Contents':
            m = match(r' +id="(.*)"$', id)
            assert m, "Missing id in {}".format(text)
            res.append('<li><a href="#{}">{}</a>'.format(m.group(1), text))
    return '<ul>\n' + '\n'.join(res) + '</ul>'


def main():
    for p in pages:
        build_page(p)

    subprocess.check_call(['sass', 'site.scss:site.css'])

    for f in files:
        shutil.copy(f, out_dir + '/')
    for d in static_dirs:
        dn = out_dir + '/' + d
        shutil.rmtree(dn)
        shutil.copytree(d, dn)


# Inline JavaScript code should encoded as CDATA for proper XHTML.
# Include the comments to work with old browsers.
JS_BEGIN = '/* <![CDATA[ */'
JS_END = '/* ]]> */'


# Obfuscate an email address by creating a JavaScript fragment that constructs
# the address + a fallback solution for browsers not supporting javascript.
#
# Expects the following CSS classes, with needed properties in parentheses:
#  * adr (no wrapping)
#  * hid (hide)
#  * char (vertical image alignemnt)
def obfuscate_email(email):
    html = ObfuscateEmailHTML(email)
    js = ObfuscateEmailJS(email)
    return ("<script type=""text/javascript"">" + JS_BEGIN + js + JS_END +
            "</script>" + "<noscript>" + html + "</noscript>")


def ObfuscateEmailJS(email):
    for ch in "xz-_#":
        if not ch in email:
            repl = ch
            break
    if len(email) < 5:
        raise ValueError("Unsupported email address")

    obfuscated = (email[:2] + repl + email[2:5] + repl + email[5:8] + repl +
                  email[8:])

    res = (
        "var addr = ('{}' + '{}').replace(/{}/g, '');".format(
            obfuscated[:4], obfuscated[4:], repl) +
        "document.write('<a href=\"mailto:'+addr+'\">'+addr+'<'+'/a>');")

    return res


def ObfuscateEmailHTML(email):
    user, domain = email.split("@")
    return ('<span class="adr">\n' +
            ('{}<span class="x">{}</span><span class="hid">xxx</span>' +
             '<img class="char" src="char.png" alt="" />{}').
            format(user[:2], user[2:], domain) +
            "\n</span>")


def build_news():
    res = []
    for item in news_items:
        res.append('<h2>%s</h2>\n' % item['title'])
        res.append('<p><b>%s</b>\n<p>%s<p>- %s' % (item['date'], item['text'], item['author']))
    return '\n'.join(res)


def build_latest_news():
    res = []
    for item in news_items[:4]:
        res.append('<p><b>%s</b>\n' % item['title'])
        res.append('<p><b>%s</b>: %s -%s' % (item['date'], item['text'], item['author']))
    return '\n'.join(res)


if __name__ == '__main__':
   main()

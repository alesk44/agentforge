from html.parser import HTMLParser
from pathlib import Path
import re

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.scripts = []
        self.styles = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'): self.ids.add(attrs['id'])
        if tag == 'script' and attrs.get('src'): self.scripts.append(attrs['src'])
        if tag == 'link' and attrs.get('rel') == 'stylesheet': self.styles.append(attrs.get('href',''))

html = Path('index.html').read_text(encoding='utf-8')
parser = Page()
parser.feed(html)
required = {'agents','how','pricing','contact','demoPanel','contactForm','language'}
missing = sorted(required - parser.ids)
assert not missing, f'Missing required HTML ids: {missing}'
for asset in parser.scripts + parser.styles:
    if asset.startswith(('http://','https://')): continue
    assert Path(asset).is_file(), f'Missing local asset: {asset}'
js = Path('app.js').read_text(encoding='utf-8')
assert 'addEventListener' in js and 'samples' in js, 'Interactive demo code missing'
assert 'no live AI call' in html or 'aucun appel IA réel' in js, 'Demo disclaimer missing'
print('AgentForge smoke checks passed: sections, local assets, interactive demos, demo disclaimer.')
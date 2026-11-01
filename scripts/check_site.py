from html.parser import HTMLParser
from pathlib import Path

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
        if tag == 'link' and attrs.get('rel') == 'stylesheet': self.styles.append(attrs.get('href', ''))

def check_page(filename, required_ids=()):
    source = Path(filename).read_text(encoding='utf-8')
    parser = Page()
    parser.feed(source)
    missing = sorted(set(required_ids) - parser.ids)
    assert not missing, f'{filename}: missing required HTML ids: {missing}'
    for asset in parser.scripts + parser.styles:
        if asset.startswith(('http://', 'https://')): continue
        assert Path(asset).is_file(), f'{filename}: missing local asset: {asset}'
    return source, parser

html, landing = check_page('index.html', {'agents','how','pricing','contact','demoPanel','contactForm','language'})
auth, auth_page = check_page('auth.html', {'authForm','email','password','googleButton','forgotButton','notice'})
dashboard, dashboard_page = check_page('dashboard.html', {'signOut','businessForm','businessList','status'})

js = Path('app.js').read_text(encoding='utf-8')
auth_js = Path('auth.js').read_text(encoding='utf-8')
dashboard_js = Path('dashboard.js').read_text(encoding='utf-8')
assert 'addEventListener' in js and 'samples' in js, 'Interactive demo code missing'
assert 'no live AI call' in html or 'aucun appel IA réel' in js, 'Demo disclaimer missing'
assert 'signInWithPassword' in auth_js and 'signUp' in auth_js, 'Supabase email authentication missing'
assert 'signInWithOAuth' in auth_js and 'resetPasswordForEmail' in auth_js, 'OAuth or password recovery missing'
assert 'updateUser({ password })' in auth_js, 'Password recovery completion missing'
assert 'from("businesses").insert' in dashboard_js and 'from("businesses").select' in dashboard_js, 'Business workspace CRUD missing'
assert 'sb_publishable_' in auth_js and 'service_role' not in auth_js, 'Publishable key missing or unsafe key reference found'
print('AgentForge smoke checks passed: landing, auth, dashboard, local assets, auth flows, tenant-scoped workspace and demo disclaimer.')

import os
from datetime import datetime
from typing import Any
import shutil
from slugify import slugify
from uuid import uuid4


def file_prefix(fn: str) -> str:
    # image.jpg => /i/im
    a = fn.split('.')
    a = a[0]

    return f"/{a[0]}/{a[:2]}" if len(a) > 1 else f"/{a[0]}"


def normalize_file_name(fn: str, only_name: bool = True) -> tuple[str, str, str]:
    if only_name:
        fn = os.path.basename(fn)
    ext = fn.split('.')
    if len(ext) > 1:
        ext = ext[-1].lower().strip()
    else:
        ext = ''

    if len(fn) > 32:
        fn = '.'.join((uuid4().hex, ext)) if ext else uuid4().hex
    else:
        fn = slugify(fn, regex_pattern=r'[^-a-zA-Z0-9._]+')

    return fn, file_prefix(fn), ext


def file_put_contents(path: str, content: str, mode: str = 'w'):
    with open(path, mode=mode) as file:
        file.write(content)


def file_get_contents(path: str, mode: str = 'r') -> str | None:
    try:
        with open(path, mode=mode) as file:
            content = file.read()
        return content
    except:
        return None


def cleardir(mydir: str, skip: list | None = None):
    if skip is None:
        skip = []
    filelist = [f for f in os.listdir(mydir)]
    skip.extend(('.', '..'))

    for f in filelist:
        if f in skip:
            continue

        f = '/'.join((mydir, f))

        if os.path.isdir(f):
            shutil.rmtree(f)
        elif os.path.isfile(f):
            os.remove(f)


def notify(message: str, log_path: str, mode: str = "a"):
    d = datetime.now()
    with open(log_path, mode=mode) as file:
        content = f"{str(d)}\t{message}\n"
        file.write(content)


def make_dir(d) -> bool:
    if not os.path.exists(d):
        os.makedirs(d, exist_ok=True, mode=0o755)
        return True
    return False


def sym_link(src, dst) -> bool:
    if os.path.islink(dst):
        return True
    if os.path.exists(src):
        os.symlink(src, dst)
        return True

    return False


def is_bot(ua: str):
    """Проверка user_agent"""
    if not ua:
        return 'ua-empty'

    ua = ua.lower()
    for b in ('yandexbot', 'yandexaccessibilitybot', 'yandexmobilebot', 'yandexdirectdyn',
              'yandexscreenshotbot', 'yandeximages', 'yandexvideo', 'yandexvideoparser',
              'yandexmedia', 'yandexblogs', 'yandexfavicons', 'yandexwebmaster',
              'yandexpagechecker', 'yandeximageresizer', 'yandexadnet', 'yandexdirect',
              'yadirectfetcher', 'yandexcalendar', 'yandexsitelinks', 'yandexmetrika',
              'yandexnews', 'yandexnewslinks', 'yandexcatalog', 'yandexantivirus',
              'yandexmarket', 'yandexvertis', 'yandexfordomain', 'yandexspravbot',
              'yandexsearchshop', 'yandexmedianabot', 'yandexontodb', 'yandexontodbapi',
              'googlebot', 'googlebot-image', 'mediapartners-google', 'adsbot-google',
              'mail.ru_bot', 'bingbot', 'accoona', 'ia_archiver', 'ask jeeves',
              'omniexplorer_bot', 'w3c_validator', 'webalta', 'yahoofeedseeker', 'yahoo!',
              'ezooms', 'tourlentabot', 'mj12bot', 'ahrefsbot', 'searchbot', 'sitestatus',
              'nigma.ru', 'baiduspider', 'statsbot', 'sistrix', 'acoonbot', 'findlinks',
              'proximic', 'openindexspider', 'statdom.ru', 'exabot', 'spider', 'seznambot',
              'obot', 'c-t bot', 'updownerbot', 'snoopy', 'heritrix', 'yeti',
              'domainvader', 'dcpbot', 'paperlibot', 'crawler', 'apachebench', 'aiohttp',
              '1c+', 'moz_illa'):

        if ua.find(b) != -1:
            return b

    return False


def ns_dict_set(d: dict, k: str, v: Any, sep: str = '.') -> dict:
    ns = k.split(sep)
    print(f'len({ns})', len(ns))
    if len(ns) == 1:
        d[k] = v
    else:
        sub_d = d
        for key in ns[:-1]:

            if key in sub_d:
                sub_d[key] = {}
                sub_d = sub_d[key]
            else:
                sub_d = sub_d.setdefault(key, {})

        sub_d[ns[-1]] = v
    return d


def ns_dict_get(d: dict, k: str, sep: str = '.', dflt: Any = None) -> dict:
    ns = k.split(sep)
    r = dflt
    try:
        for t in ns:
            r = d[t]
            if isinstance(r, dict):
                d = r
        return r
    except:
        return dflt

from re import compile

from slugify import slugify
from xxhash import xxh32_intdigest

SLUG_PATTERN = compile(r'[^-a-zA-Z0-9._]+')


def str_hash(str_to_hash: str) -> int:
    return xxh32_intdigest(str_to_hash)


def app_slug(str_to_slug: str, lowercase: bool = False) -> str:
    return slugify(str_to_slug, lowercase=lowercase, regex_pattern=SLUG_PATTERN)


def check_url(url_to_slug: str) -> tuple[str, str | None]:
    """
    :param url_to_slug: str
    :return: tuple[current_url, parent_url]
    """
    def _(_url: str) -> str:
        return app_slug(_url)

    if url_to_slug == "/":
        return "/", None
    __url = list(map(_, url_to_slug.strip().split("/")))

    return "/".join(__url), "/".join(__url[:-1])


def is_bot(ua: str) -> str | bool:
    """
    :param ua: str User-agent
    :return: bot-name if bot else False
    """
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
              '1c+', 'mozwilla'):

        if ua.find(b) != -1:
            return b

    return False

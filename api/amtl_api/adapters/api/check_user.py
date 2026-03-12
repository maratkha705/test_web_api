def is_bot(user_agent: str):
    """
    Если пользователь хороший бот
    """
    if not user_agent:
        return 'ua-empty'

    user_agent = user_agent.lower()
    for b in ('yandexbot', 'yandexaccessibilitybot', 'yandexmobilebot',
              'yandexdirectdyn', 'yandexscreenshotbot', 'yandeximages',
              'yandexvideo', 'yandexvideoparser', 'yandexmedia', 'yandexblogs',
              'yandexfavicons', 'yandexwebmaster', 'yandexpagechecker',
              'yandeximageresizer', 'yandexadnet', 'yandexdirect',
              'yadirectfetcher', 'yandexcalendar', 'yandexsitelinks',
              'yandexmetrika', 'yandexnews', 'yandexnewslinks', 'yandexvertis',
              'yandexantivirus', 'yandexmarket', 'yandexcatalog',
              'yandexfordomain', 'yandexspravbot', 'yandexsearchshop',
              'yandexmedianabot', 'yandexontodb', 'yandexontodbapi',
              'googlebot', 'googlebot-image', 'mediapartners-google',
              'adsbot-google', 'mail.ru_bot', 'bingbot', 'accoona',
              'ia_archiver', 'ask jeeves', 'omniexplorer_bot', 'w3c_validator',
              'webalta', 'yahoofeedseeker', 'yahoo!', 'ezooms', 'tourlentabot',
              'mj12bot', 'ahrefsbot', 'searchbot', 'sitestatus', 'nigma.ru',
              'baiduspider', 'statsbot', 'sistrix', 'acoonbot', 'findlinks',
              'proximic', 'openindexspider', 'statdom.ru', 'exabot', 'spider',
              'seznambot', 'obot', 'c-t bot', 'updownerbot', 'snoopy', 'yeti',
              'domainvader', 'dcpbot', 'paperlibot', 'crawler', 'apachebench',
              'aiohttp', '1c+', 'heritrix', 'moz_illa'):

        if user_agent.find(b) != -1:
            return b

    return False

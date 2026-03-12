from os import path
from sys import exc_info
from slugify import slugify
import geoip2.database


def get_geodata(ip: str = None, f: str = 'ru'):

    pth = path.dirname(path.realpath(__file__))

    if ip is None or ip.startswith('127.0') or ip.startswith('0.0'):
        ip = '178.205.189.155'

    with geoip2.database.Reader(f'{pth}/GeoLite2-City.mmdb') as reader:

        try:
            res = reader.city(ip)

            if res is None:
                return {
                    "error": f"IP <{ip}> not found",
                    "detail": "Reader returned None",
                    "file": "/".join(path.realpath(__file__).split("/")[-3:]),
                    "ex_type": None,
                }
            g = {
                'country': res.country.iso_code,
                'city_name': res.city.name,
                'province': (res.country.name, res.subdivisions.most_specific.name),
                'city_names': res.city.names,
                'country_names': res.country.names,
                'subdivision_names': res.subdivisions.most_specific.names,
                'postal_code': res.postal.code,
                'lat': res.location.latitude,
                'lon': res.location.longitude,
                'net': str(res.traits.network),
                'region_id': None,
                'target_city_name': None,
                'target_province': None,
            }

            if res.city.name is not None:
                g['region_id'] = '/'.join(list(map(slugify, g['province'])))
                if f in res.city.names:
                    g['target_city_name'] = res.city.names.get(f)
                    g['target_province'] = (res.country.names.get(f), res.subdivisions.most_specific.names.get(f))

            return g

        except Exception as ex:
            exc_type, _, exc_tb = exc_info()
            exc_fn: str = exc_tb.tb_frame.f_code.co_filename
            return {
                "error": f"IP <{ip}> not found",
                "detail": repr(ex),
                "file": f"{'/'.join(exc_fn.split('/')[-4:])}:{exc_tb.tb_lineno}",  # noqa
                "ex_type": exc_type
            }


if __name__ == '__main__':
    from time import time
    t = time()
    geo = get_geodata(ip="188.225.123.142")
    for k, v in geo.items():
        print(k, ":", v)

    print('~~\nTime (ms):', (time()-t)*1000)

# from typing import Union, Any
from collections.abc import Callable

# from collections import defaultdict
from lxml.etree import iterparse
# from datetime import datetime
from slugify import slugify


class XmlParser(object):

    def __init__(self, xmlfile: str, **kw) -> None:
        self.xmlfile = xmlfile
        self.cnt = 0

    def parse_it(self, handlers: dict[str, Callable] | None = None):
        if handlers is None:
            handlers = {}
        for event, elem in iterparse(
            self.xmlfile,
            events=('start', 'end')
        ):

            if event == 'start':
                if elem.tag in handlers:
                    self.cnt += 1
                    r = handlers[elem.tag](elem)

            elif event == 'end':
                # p = elem.getparent()
                # print('clear:',
                #      elem.tag, 'text:', elem.text,
                #      list(elem), self.cnt, p)

                elem.clear()

                # if p is not None:
                #    p.remove(elem)

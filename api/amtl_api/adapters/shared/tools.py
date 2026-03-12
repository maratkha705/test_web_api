import attr


def component(original_cls: type = None, init: bool = True):
    """ """

    def _decorate(cls):
        cls.__component__ = True

        if init:
            cls = attr.dataclass(cls, eq=False, kw_only=True)

        return cls

    if original_cls:
        return _decorate(original_cls)

    return _decorate

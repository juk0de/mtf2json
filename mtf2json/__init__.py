# this enables direct import from 'mtf2json' (instead of 'mtf2json.mtf2json')
from .mtf2json import read_mtf, write_json, version, mm_commit, statistics  # noqa
from .error import ConversionError  # noqa

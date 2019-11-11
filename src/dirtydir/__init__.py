# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = 'unknown'
finally:
    del get_distribution, DistributionNotFound


from dirtydir import main


def list_changed():
    main.list_dir(True, verbose=False)


def list_unchanged():
    main.list_dir(False, verbose=False)


def lock_subfolder(subfolder):
    main.lock_subfolder(subfolder)

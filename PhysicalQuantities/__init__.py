# -*- coding: utf-8 -*-
"""
Physical Quantities for Python and IPython

Usage in Python:
================

    import PhysicalQuantities as pq
    a = pq.PhysicalQuantity(1.0, 'm')
or simply    
    a = pq.Q(1.0, 'm')

The value of a physical quantity can by any number, list or numpy array.
The units are derived from SI base units and can be any combination,
including prefixes:
    a = pq.Q(1.0, 'm**2/s**3')
    
Lists or arrays can also be used and indexed:
    b = [1,2,3]
    c = a*b
    print c[0]    

Usage in IPython:
===============

    %load_ext PyPUnits.ipython
Then you can type directly:
    a = 1 mm
without explicitly calling a function constructor

"""
from __future__ import absolute_import
from .Quantity import *
import numpy as np

import pkg_resources
version = pkg_resources.require("PhysicalQuantities")[0].version

Q = PhysicalQuantity
U = PhysicalUnit

# Add additional units (SI units are predefined)
addprefixed(addunit('Hz', '1/s', 'Hertz', url='https://en.wikipedia.org/wiki/Hertz'),range='engineering')
addprefixed(addunit('N', 'm*kg/s**2', 'Newton', url='https://en.wikipedia.org/wiki/Newton_(unit)'),range='engineering')
addprefixed(addunit('Pa', 'N/m**2', 'Pascal', url='https://en.wikipedia.org/wiki/Pascal_(unit)'),range='engineering')
addprefixed(addunit('J', 'N*m', 'Joule', url='https://en.wikipedia.org/wiki/Joule'),range='engineering')
addprefixed(addunit('W', 'J/s', 'Watt', url='https://en.wikipedia.org/wiki/Watt'),range='engineering')
addprefixed(addunit('C', 's*A', 'Coulomb', url='https://en.wikipedia.org/wiki/Coulomb'),range='engineering')
addprefixed(addunit('V', 'W/A', 'Volt', url='https://en.wikipedia.org/wiki/Volt'),range='engineering')
addprefixed(addunit('F', 'C/V', 'Farad', url='https://en.wikipedia.org/wiki/Farad'),range='engineering')
addprefixed(addunit('Ohm', 'V/A', 'Ohm', url='https://en.wikipedia.org/wiki/Ohm_(unit)'),range='engineering')
addprefixed(addunit('S', 'A/V', 'Siemens', url='https://en.wikipedia.org/wiki/Siemens_(unit)'),range='engineering')
addprefixed(addunit('Wb', 'V*s', 'Weber', url='https://en.wikipedia.org/wiki/Weber_(unit)'),range='engineering')
addprefixed(addunit('T', 'Wb/m**2', 'Tesla', url='https://en.wikipedia.org/wiki/Tesla_(unit)'),range='engineering')
addprefixed(addunit('H', 'Wb/A', 'Henry', url='https://en.wikipedia.org/wiki/Henry_(unit)'),range='engineering')
addprefixed(addunit('lm', 'cd*sr', 'Lumen', url='https://en.wikipedia.org/wiki/Lumen_(unit)'),range='engineering')
addprefixed(addunit('lx', 'lm/m**2', 'Lux', url='https://en.wikipedia.org/wiki/Lux'),range='engineering')

# Angle units
unit_table['pi'] = np.pi
addunit('deg', 'pi*rad/180', 'Degree', url='http://en.wikipedia.org/wiki/Degree_%28angle%29')
addunit('arcmin', 'pi*rad/180/60', 'minutes of arc')
addunit('arcsec', 'pi*rad/180/3600', 'seconds of arc')
del unit_table['pi']
# Time
addunit('min', '60*s', 'Minute', url='https://en.wikipedia.org/wiki/Hour')
addunit('h', '60*60*s', 'Hour', url='https://en.wikipedia.org/wiki/Hour')


# numpy linspace wrapper for units
def linspace(start, stop, num = 50,  endpoint=True, retstep=False):
    """ A units-enabled linspace
    :param start: start value
    :param stop:  stop value
    :param num: number of points
    :param endpoint: include stop point
    :param retstep: if true, return (samples, step)
    :return: return equally spaced samples between start and stop
    """
    if not isinstance(start, PhysicalQuantity) and not isinstance(stop, PhysicalQuantity):
        return np.linspace(start, stop, num,  endpoint, retstep)

    if isinstance(start, PhysicalQuantity) and isinstance(stop, PhysicalQuantity):
        if start.base.unit != stop.base.unit:
            raise UnitError("Cannot match units")

    unit = None
    if isinstance(start, PhysicalQuantity):
        start_value = start.value
        unit = start.unit
    else:
        start_value = start

    if isinstance(stop, PhysicalQuantity):
        stop_value = stop.value
        unit = stop.unit
    else:
        stop_value = stop

    array = np.linspace(start_value, stop_value, num,  endpoint, retstep)

    if retstep:
        return PhysicalQuantity(array[0], unit), PhysicalQuantity(array[1], unit)
    else:
        return array * PhysicalQuantity(1, unit)

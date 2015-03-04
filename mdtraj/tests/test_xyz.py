##############################################################################
# MDTraj: A Python Library for Loading, Saving, and Manipulating
#         Molecular Dynamics Trajectories.
# Copyright 2012-2013 Stanford University and the Authors

# Authors: Christoph Klein
# Contributors:
#
# MDTraj is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 2.1
# of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with MDTraj. If not, see <http://www.gnu.org/licenses/>.
##############################################################################


import tempfile, os
import numpy as np

import mdtraj as md
from mdtraj.formats import XYZTrajectoryFile, xyzfile
from mdtraj.testing import get_fn, eq, DocStringFormatTester, raises
TestDocstrings = DocStringFormatTester(xyzfile, error_on_none=True)

fd, temp = tempfile.mkstemp(suffix='.xyz')
def teardown_module(module):
    """Remove the temporary file created by tests in this file
    this gets automatically called by nose. """
    os.close(fd)
    os.unlink(temp)

def test_read_0():
    with XYZTrajectoryFile(get_fn('frame0.xyz')) as f:
        xyz = f.read()
    with XYZTrajectoryFile(get_fn('frame0.xyz')) as f:
        xyz3 = f.read(stride=3)
    eq(xyz[::3], xyz3)

def test_read_1():
    reference = md.load(get_fn('frame0.dcd'), top=get_fn('native.pdb'))
    traj = md.load(get_fn('frame0.xyz'), top=get_fn('native.pdb'))

    eq(reference.xyz[0], traj.xyz[0], decimal=3)


def test_mdwrite():
    t = md.load(get_fn('frame0.dcd'), top=get_fn('native.pdb'))
    t.save(temp)

def test_multiread():
    reference = md.load(get_fn('frame0.xyz'), top=get_fn('native.pdb'))
    with XYZTrajectoryFile(get_fn('frame0.xyz')) as f:
        xyz0 = f.read(n_frames=1)
        xyz1 = f.read(n_frames=1)

    eq(reference.xyz[0], xyz0[0]/10)
    eq(reference.xyz[1], xyz1[0]/10)

def test_seek():
    reference = md.load(get_fn('frame0.xyz'), top=get_fn('native.pdb'))

    with XYZTrajectoryFile(get_fn('frame0.xyz')) as f:
        f.seek(1)
        eq(1, f.tell())
        xyz1 = f.read(n_frames=1)
        eq(reference.xyz[1], xyz1[0]/10)

        f.seek(10)
        eq(10, f.tell())
        xyz10 = f.read(n_frames=1)
        eq(reference.xyz[10], xyz10[0]/10)
        eq(11, f.tell())

        f.seek(-8, 1)
        xyz3 = f.read(n_frames=1)
        eq(reference.xyz[3], xyz3[0]/10)

        f.seek(4, 1)
        xyz8 = f.read(n_frames=1)
        eq(reference.xyz[8], xyz8[0]/10)

if __name__ == "__main__":
    test_read_0()
    test_read_1()
    test_mdwrite()
    test_multiread()
    test_seek()
import os
import glob
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext

def get_extensions():
    define_macros = [('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')]
    uncompress = Extension('scilpy.tractograms.uncompress',
                           ['scilpy/tractograms/uncompress.pyx'],
                           define_macros=define_macros)
    voxel_boundary_intersection =\
        Extension('scilpy.tractanalysis.voxel_boundary_intersection',
                  ['scilpy/tractanalysis/voxel_boundary_intersection.pyx'],
                  define_macros=define_macros)
    streamlines_metrics =\
        Extension('scilpy.tractanalysis.streamlines_metrics',
                  ['scilpy/tractanalysis/streamlines_metrics.pyx'],
                  define_macros=define_macros)
    return [uncompress, voxel_boundary_intersection, streamlines_metrics]


class CustomBuildExtCommand(build_ext):
    """ build_ext command to use when numpy headers are needed. """

    def run(self):
        # Now that the requirements are installed, get everything from numpy
        from Cython.Build import cythonize
        from numpy import get_include

        # Add everything requires for build
        self.swig_opts = None
        self.include_dirs = [get_include()]
        self.distribution.ext_modules[:] = cythonize(
            self.distribution.ext_modules)

        # Call original build_ext command
        build_ext.finalize_options(self)
        build_ext.run(self)

LEGACY_SCRIPTS = filter(lambda s: not os.path.basename(s) == "__init__.py",
                        glob.glob("scripts/legacy/*.py"))
SCRIPTS = filter(lambda s: not os.path.basename(s) == "__init__.py",
                 glob.glob("scripts/*.py"))

entry_point_legacy = []
if os.getenv('SCILPY_LEGACY') != 'False':
    entry_point_legacy = ["{}=scripts.legacy.{}:main".format(
                          os.path.basename(s),
                          os.path.basename(s).split(".")[0]) for s in LEGACY_SCRIPTS]

entry_point = ["{}=scripts.{}:main".format(
                  os.path.basename(s),
                  os.path.basename(s).split(".")[0]) for s in SCRIPTS]


setup(packages=find_packages(),
      cmdclass={'build_ext': CustomBuildExtCommand},
      ext_modules=get_extensions(),
      scripts=entry_point + entry_point_legacy,
    #   entry_points={
    #       'console_scripts': entry_point + entry_point_legacy
    #   },
      data_files=[('data/LUT',
                   ["data/LUT/freesurfer_desikan_killiany.json",
                    "data/LUT/freesurfer_subcortical.json",
                    "data/LUT/dk_aggregate_structures.json"])],
      include_package_data=True)

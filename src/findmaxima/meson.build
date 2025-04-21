
python = import('python').find_installation()

#numpy_include_dir = python.run_command(
#  [python.get_path('purelib'), '-c', 'import numpy; print(numpy.get_include())'],
#  check: true # Fail build if numpy is not found or get_include() fails
#).stdout.strip()


cymod = python.extension_module( 'cy_findmaxima',
        'cy_findmaxima.pyx',
        install: true,
        subdir: 'findmaxima'
 )

python_sources = [
  '__init__.py',
  'findmaxima.py',
  ]

python.install_sources(
  python_sources,
  pure: false,             # Will be installed next to binaries
  subdir: 'findmaxima'  # Folder relative to site-packages to install to
)

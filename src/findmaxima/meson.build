
python = import('python').find_installation()

numpy_include_dir = python.run_command(
  [python.get_path('purelib'), '-c', 'import numpy; print(numpy.get_include())'],
  check: true # Fail build if numpy is not found or get_include() fails
).stdout.strip()

cymod = python.extension_module(
  'findmaxima',
  'findmaxima.pyx',
  install: true,
  subdir: 'findmaxima'
  )

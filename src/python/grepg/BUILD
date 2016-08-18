python_binary(name='bin',
  dependencies=[
    'src/python/grepg/lib',
  ],
  platforms = ['linux-x86_64', 'macosx-10.4-x86_64'],
  source='main.py',
  entry_point = "grepg.main:main_run",
)

python_library(name='grepg-packaged',
  provides=setup_py(
    name='grepg',
    version='0.1.0',
    description='A python client for GrepPage',
    long_description='''grepg (pronounced Grep G) is a python client for GrepPage (www.greppage.com).
It allows you to access your cheat sheets without leaving the terminal.''',
    url='https://github.com/tejal29/grepg',
    namespace_packages=['grepg'],
    license='MIT License',
    zip_safe=True,
  ).with_binaries(
     grepg=':bin',
  )
)

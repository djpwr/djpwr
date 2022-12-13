from distutils.core import setup

setup(name="djpwr",
      version="1.0.0",
      description="Django for Power Users",
      license='MIT',
      author="Ruud de Klerk",
      author_email="ruud@codeveloped.nl",
      url='https://github.com/djpwr/djpwr',
      packages=['djpwr', 'djpwr.admin', 'djpwr.clock']
)

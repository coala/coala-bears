from setuptools import setup, find_packages

version = '1.0'

long_description = """
This is a long descpription.


Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed porttitor, neque
at dignissim condimentum, libero est dictum dolor, sit amet tempor urna
diam eget velit. Suspendisse at odio quam, ut vestibulum ipsum. Nulla
facilisi. Nullam nunc dolor, tempus in vulputate id, fringilla eget metus.
Pellentesque nulla nisl, imperdiet ac vulputate non, commodo tincidunt
purus. Aenean sollicitudin orci eget diam dignissim scelerisque. Donec quis
neque nisl, eu adipiscing velit. Aenean convallis ante sapien. Etiam vitae
viverra libero. Nullam ac ligula erat. Aliquam pellentesque, est eget
faucibus pharetra, urna orci rhoncus nisi, adipiscing elementum liber
lectus ut odio. Duis tincidunt mi quam, quis interdum enim. Nunc sed urna
urna, id lacinia turpis. Quisque malesuada, velit ut tincidunt lacinia,
dolor augue varius velit, in ultrices lectus enim et dolor. Fusce augue eros,
aliquet ac dapibus at, tincidunt vitae leo. Lorem ipsum dolor sit amet,
consectetur adipiscing elit. Vivamus sapien neque, fermentum sed ultrices
sit amet, fermentum nec est. Pellentesque imperdiet enim nec velit posuere
id dignissim massa molestie.
"""

setup(name='complete',
      version=version,
      description='This is a test package for pyroma.',
      long_description=long_description,
      classifiers=['Development Status :: 6 - Mature',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.1',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   ],
      keywords=['pypi', 'quality', 'example'],
      author='Jon Smith',
      author_email='jon@smith.com',
      url='http://jonsmith.com',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      install_requires=['zope.event'],
      tests_require=['six'],
      setup_requires=['setuptools'],
      zip_safe=True,
      test_suite='complete',
      )

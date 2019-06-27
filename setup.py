from setuptools import setup                                                                                      │


def parse_requirements(filename):                                                                                 │
    """ load requirements from a pip requirements file """                                                        │
    lineiter = (line.strip() for line in open(filename))                                                          │
    return [line for line in lineiter if line and not line.startswith("#")]                                       │


install_reqs = parse_requirements("requirements.txt")                                                             │

                                                                                                                  │
setup(name='yolo',                                                                                                │
      version='0.1',                                                                                              │
      description='yolo',                                                                                         │
      url='https://github.com/zuhlke-hk-topicteam-datascience/yolo',                                                         │
      author='Dominic Morgan',                                                                                    │
      author_email='onetonfoot@gmail.com',                                                                        │
      license='GNU',                                                                                              │
      packages=['yolo'],                                                                                          │
      install_requires=install_reqs,                                                                              │
      # for packages on github                                                                                    │
      dependency_links=[],                                                                                        │
      zip_safe=False)    
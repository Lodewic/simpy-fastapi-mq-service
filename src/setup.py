from setuptools import find_packages, setup

from simpy_fastapi_service import __version__


def read_requirements(filepath: str) -> list[str]:
    # get the dependencies and installs
    with open(filepath, encoding="utf-8") as f:
        # Make sure we strip all comments and options (e.g "--extra-index-url")
        # that arise from a modified pip.conf file that configure global options
        # when running kedro build-reqs
        requires = []
        for line in f:
            req = line.split("#", 1)[0].strip()
            if req and not req.startswith("--"):
                requires.append(req)
    return requires


core_requires = read_requirements("requirements/core.txt")
docs_requires = read_requirements("requirements/docs.txt")
test_requires = read_requirements("requirements/test.txt")
dev_dependencies = read_requirements("requirements/dev.txt")


setup(
    name="simpy_fastapi_service",
    version=__version__,
    packages=find_packages(
        include=["simulation_core", "simpy_fastapi_service"], exclude=["tests", "requirements"]
    ),
    install_requires=core_requires,
    extras_require={
        "docs": docs_requires,
        "test": test_requires,
        "dev": test_requires + dev_dependencies,
    },
)

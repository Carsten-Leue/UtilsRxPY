# UtilsRxPY

## Development Setup

Follow [these guidelines](https://github.ibm.com/ZaaS/scaas/wiki/Pip-Installable-Packages#configuration-for-consuming-packages) to setup access to the [HPHA PyPI artifactory](https://eu.artifactory.swg-devops.com/ui/repos/tree/General/sys-zaas-team-hpha-dev-pypi-virtual), e.g. 

using environment variables:
```bash
export PIP_INDEX_URL=https://eu.artifactory.swg-devops.com/artifactory/api/pypi/sys-zaas-team-dev-pypi-virtual/simple
```

or using a [pip config file](https://pip.pypa.io/en/stable/user_guide/#config-file):
```toml
[global]
index = https://eu.artifactory.swg-devops.com/artifactory/api/pypi/sys-zaas-team-dev-pypi-virtual/simple
index-url = https://eu.artifactory.swg-devops.com/artifactory/api/pypi/sys-zaas-team-dev-pypi-virtual/simple
```

Install [tox](https://tox.readthedocs.io/en/latest/install.html).

## Documentation

Refer to the [API docs](https://github.com/Carsten-Leue/UtilsRxPY)

## Build Setup

[![Build Status](https://sys-zaas-hp-jenkins.swg-devops.com/buildStatus/icon?job=hpha%2Fhpha_semantic%2FUtilsRxPY%2Fmaster)](https://sys-zaas-hp-jenkins.swg-devops.com/job/hpha/job/hpha_semantic/job/UtilsRxPY/job/master/)

### Builds

- [Jenkins Build](https://sys-zaas-hp-jenkins.swg-devops.com/job/hpha/job/hpha_semantic/job/UtilsRxPY/)

### Travis

Define the following environment variables:

- `PYPI_REPO`: URL to the repository, does not have to be a protected variable, e.g. `https://eu.artifactory.swg-devops.com/artifactory/api/pypi/sys-zaas-devops-taskforce-team-test-dev-pypi-virtual`
- `PYPI_USERNAME`: Username, should be protected, e.g. your IBM intranet URL
- `PYPI_PASSWORD`: Password, must be protected, e.g. your artifactory API token

### Git Workflow

Pushing to git will trigger a new build but not a new deployment. In order to deploy first update the version number using the [bumpversion](https://pypi.org/project/bump2version/) workflow, e.g. 

```bash
bumpversion patch
```

Then execute a tagged commit:

```bash
git push --tags
```

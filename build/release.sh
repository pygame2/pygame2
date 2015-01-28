#!/bin/bash
# Requires virtualenv to be located somewhere on the PATH

function join { local IFS="$1"; shift; echo "$*"; }

BUILD=$1

if [ -z "$TRAVIS_TAG" ]
then
  # Get current version and append the new build number
  IFS='.' read -ra VERS <<< "`git describe --tags HEAD`"
  VERSION=join . ${VERS[@]:0:2}
  VERSION=0.0.$BUILD
  
  git tag $VERSION
  git push --tags
else
  # Current build is for a tag
  ENV=pygame2-${TRAVIS_TAG}_pypy3_x86_64
  OUTFILE=$ENV.tar.xz
  
  cd build

  wget https://bitbucket.org/squeaky/portable-pypy/downloads/pypy3-2.4-linux_x86_64-portable.tar.bz2
  tar xaf pypy3-2.4-linux_x86_64-portable.tar.bz2
  
  virtualenv --no-setuptools -p pypy3-2.4-linux_x86_64-portable/bin/pypy $ENV
  
  curl -o get-pip.py https://bootstrap.pypa.io/get-pip.py
  . $ENV/bin/activate
  $ENV/bin/python get-pip.py
  
  $ENV/bin/pip install ..
  $ENV/bin/pip install -r ../requirements.txt
  
  virtualenv --relocatable $ENV
  
  tar cafh $OUTFILE $ENV
  
  ./github-release.sh "$TRAVIS_REPO_SLUG" "${TRAVIS_TAG}" $OUTFILE
  
  cd ..
fi



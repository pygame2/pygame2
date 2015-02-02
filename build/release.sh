#!/bin/bash
# Requires virtualenv to be located somewhere on the PATH


if [ -z "$TRAVIS_TAG" ]
then
  function join { local IFS="$1"; shift; echo "$*"; }
  
  # Get current version and append the new build number
  IFS='.' read -ra VERS <<< "`git describe --tags HEAD`"
  VERSION=join . ${VERS[@]:0:2}
  VERSION=0.0.$1
  
  git tag $VERSION
  git push --tags
fi
#else
  # Current build is for a tag
  #ENV=pygame2-${TRAVIS_TAG}_pypy3_x86_64
  #OUTFILE=$ENV.tar.xz
  #
  #cd build
  #
  #PYPY=pypy3-2.4-linux_x86_64-portable
  #wget https://bitbucket.org/squeaky/portable-pypy/downloads/$PYPY.tar.bz2
  #tar xaf $PYPY.tar.bz2
  #
  #$PYPY/bin/virtualenv-pypy --no-setuptools $ENV
  #
  #rm -rf $ENV/include && cp -r $PYPY/include $ENV
  #rm -rf $ENV/lib && cp -r $PYPY/lib $ENV
  #rm -rf $ENV/lib_pypy && cp -r $PYPY/lib_pypy $ENV
  #rm -rf $ENV/lib-python && cp -r $PYPY/lib-python $ENV
  #
  #curl -o get-pip.py https://bootstrap.pypa.io/get-pip.py
  #. $ENV/bin/activate
  #$ENV/bin/python get-pip.py
  #
  #$ENV/bin/pip install ..
  #$ENV/bin/pip install -r ../requirements.txt
  #
  #$PYPY/bin/virtualenv-pypy --relocatable $ENV
  #
  #sed -i 's/VIRTUAL_ENV=\"\(.*\)\"/VIRTUAL_ENV=$BASEDIR/g' $ENV/bin/activate
  #
  #tar cafh $OUTFILE $ENV
  #
  #./github-release.sh "$TRAVIS_REPO_SLUG" "${TRAVIS_TAG}" $OUTFILE
  #
  #cd ..
#fi


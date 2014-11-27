#!/bin/sh

_usage()
{
	echo "usage: $0 <pylint-src-dir> <rule>"
	exit 1
}

if [ X"$1" = X"" ]; then
	_usage
fi
if [ X"$2" = X"" ]; then
	_usage
fi
_pdir=$(cd -- "$1" 2>/dev/null && pwd || echo "/nonexistent") 
if [ X"$_pdir" = X"/nonexistent" ]; then
	echo "err: specify valid pylint source directory"
	exit 1
fi
_cdir=$(cd -- "$(dirname "$0")" && pwd)
_rule=$2

_find_rule()
{
	if [ X"$1" = X"" ]; then
		return
	fi
	cd "${_pdir}"
	echo "### $1"
	hg checkout "$1" 2>&1 > /dev/null
	grep -rH "$_rule" *
}

_find_rule pylint-version-0_13_0
_find_rule pylint-version-0_15_0
_find_rule pylint-version-0_15_1
_find_rule pylint-version-0_15_2
_find_rule pylint-version-0_17_0
_find_rule pylint-version-0.18.1
_find_rule pylint-version-0.19.0
_find_rule pylint-version-0.20.0
_find_rule pylint-version-0.21.0
_find_rule pylint-version-0.21.1
_find_rule pylint-version-0.21.2
_find_rule pylint-version-0.21.3
_find_rule pylint-version-0.21.4
_find_rule pylint-version-0.22.0
_find_rule pylint-version-0.23.0
_find_rule pylint-version-0.24.0
_find_rule pylint-version-0.25.0
_find_rule pylint-version-0.25.1
_find_rule pylint-version-0.25.2
_find_rule pylint-version-0.26.0
_find_rule pylint-version-0.27.0
_find_rule pylint-version-0.28.0
_find_rule pylint-version-1.0.0
_find_rule pylint-version-1.1.0
_find_rule pylint-1.2
_find_rule pylint-1.3
_find_rule pylint-1.3.1
_find_rule pylint-1.4

cd "${_pdir}"
hg checkout tip

cd "${_cdir}"

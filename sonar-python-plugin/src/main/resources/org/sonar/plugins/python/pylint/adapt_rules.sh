#!/bin/sh
_cdir=$(cd -- "$(dirname "$0")" && pwd)
cat "${_cdir}/rules_generated.xml" | python "${_cdir}/adapt_rules.py" > rules_adapted.xml


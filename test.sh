#!/bin/bash
MODS="output/*"
for f in $MODS
do
  xmllint $f > /dev/null
done

#!/bin/bash

cd `dirname $0`
working=`pwd`

# Ensure plugin directory exists and empty it
mkdir conf &> /dev/null
mkdir conf/plugin &> /dev/null
rm conf/plugin/* &> /dev/null

# Go through each plugin directory
for plugin in `find .. -maxdepth 1 -name "*Plugin" -exec basename {} \;`
do
  echo "Checking $plugin..."
  mkdir ../$plugin/bin &> /dev/null
  cd ../$plugin/bin
  if [ "$(ls -A)" ]; then
    echo " - $plugin has content, let's create!"
    zip -r $working/conf/plugin/$plugin.jar . &> /dev/null
  fi
  cd $working
done


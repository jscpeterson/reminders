#!/bin/bash
webpack
cp ../static/src/rulelist.js ../static/src/rulelist-old.js
cp dist/main.js ../static/src/rulelist.js
printf '\7'

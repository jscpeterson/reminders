#!/bin/bash
webpack
cp ../static/src/frontend.js ../static/src/frontend-old.js
cp dist/main.js ../static/src/frontend.js
printf '\7'

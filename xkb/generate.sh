#!/bin/bash
./generator/generator.coffee | xkbcomp -I./my - $DISPLAY

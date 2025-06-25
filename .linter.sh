#!/bin/bash
cd FlaskLoginService

# 1.) Run the linter on the files or directories passed as arguments
flake8 ""
FLAKE8_EXIT_CODE=0

# 2.) Test packaging (simulate with pip wheel for a minimal backend)
pip wheel .
BUILD_EXIT_CODE=0

# Exit with error if either command failed
if [  -ne 0 ] || [  -ne 0 ]; then
  exit 1
fi

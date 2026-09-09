#!/usr/bin/env bash
# Build helper when system g++/make are missing. Prefers zig c++ if present.
set -euo pipefail
cd "$(dirname "$0")"
INTERLEAVE="${FRACTAL_INTERLEAVE:-1}"
CXXFLAGS=(-O2 -std=c++11 -Wall -Wextra -pthread "-DFRACTAL_INTERLEAVE=${INTERLEAVE}")

if command -v g++ >/dev/null 2>&1; then
  CXX=(g++)
elif [[ -x /home/afnanasif/zig-linux-x86_64-0.13.0/zig ]]; then
  CXX=(/home/afnanasif/zig-linux-x86_64-0.13.0/zig c++)
else
  echo "No g++ or zig toolchain found." >&2
  exit 1
fi

mkdir -p objs
"${CXX[@]}" "${CXXFLAGS[@]}" -c main.cpp -o objs/main.o
"${CXX[@]}" "${CXXFLAGS[@]}" -c fractalSerial.cpp -o objs/fractalSerial.o
"${CXX[@]}" "${CXXFLAGS[@]}" -c fractalThread.cpp -o objs/fractalThread.o
"${CXX[@]}" "${CXXFLAGS[@]}" -o fractal objs/main.o objs/fractalSerial.o objs/fractalThread.o
echo "Built ./fractal (FRACTAL_INTERLEAVE=${INTERLEAVE})"

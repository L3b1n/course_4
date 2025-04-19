#!/bin/bash
set -eu
set -o pipefail

[[ $# -lt 2 ]] && echo "Usage: $0  <path/to/zipped .framework> <hdrs>..." && exit 1
zipped=$(python -c "import os; print(os.path.realpath('$1'))"); shift
name=$(basename "$zipped" .zip)
parent=$(dirname "$zipped")
named="$parent"/"$name".framework

unzip "$zipped" -d "$parent"

mkdir "$named"/Modules
cat << EOF >"$named"/Modules/module.modulemap
framework module $name {
  umbrella header "$name.h"

  export *
  module * { export * }

  link framework "AVFoundation"
  link framework "Accelerate"
  link framework "AssetsLibrary"
  link framework "CoreFoundation"
  link framework "CoreGraphics"
  link framework "CoreImage"
  link framework "CoreMedia"
  link framework "CoreVideo"
  link framework "GLKit"
  link framework "Metal"
  link framework "MetalKit"
  link framework "OpenGLES"
  link framework "QuartzCore"
  link framework "UIKit"
}
EOF

cat << EOF >"$named"/Headers/$name.h
#import <Foundation/Foundation.h>

FOUNDATION_EXPORT double ${name}VersionNumber;
FOUNDATION_EXPORT const unsigned char ${name}VersionString[];

EOF
until [[ $# -eq 0 ]]; do
  printf '#import "'"$1"'"\n' "$1" >>"$named"/Headers/$name.h
  shift
done

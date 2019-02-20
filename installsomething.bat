REM Electron's version.
set npm_config_target=3.1.3
REM The architecture of Electron, can be ia32 or x64.
set npm_config_arch=x64
set npm_config_target_arch=x64
REM Download headers for Electron.
set npm_config_disturl=https://atom.io/download/electron
REM Tell node-pre-gyp that we are building for Electron.
set npm_config_runtime=electron
REM Tell node-pre-gyp to build module from source code.
set npm_config_build_from_source=true
npm install wrtc
PAUSE
PAUSE
PAUSE
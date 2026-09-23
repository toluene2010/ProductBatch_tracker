[app]
title = Production Batch Tracker Entry
package.name = productionbatchtracker
package.domain = com.productionbatchtracker

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,txt
source.exclude_dirs = bin,.buildozer
version = 1.0.0

requirements = python3,kivy,requests,urllib3,chardet,idna,certifi,jnius

orientation = portrait
fullscreen = 0

android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.archs = arm64-v8a
android.allow_backup = True
android.accept_sdk_license = True
android.ndk = 25b
android.ndk_api = 21

[buildozer]
log_level = 2
warn_on_root = 1

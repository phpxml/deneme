[app]
title = My Application
package.name = myapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Sürümleri sabitleyerek hatayı engelliyoruz
requirements = python3,kivy==2.2.1,requests,urllib3,certifi,openssl

orientation = portrait
fullscreen = 0

# Android Ayarları
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1

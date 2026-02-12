[app]
title = RastreadorGPS
package.name = rastreador
package.domain = org.turastreador

source.dir = .
source.include_exts = py,kv,html,db,css,js

version = 1.0

android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION

android.archs = arm64-v8a, armeabi-v7a

# AGREGA pyjnius con versión específica y cython actualizado
requirements = python3,kivy,flask,plyer,requests,sqlalchemy,itsdangerous,jinja2,markupsafe,werkzeug,pyjnius,cython

# AGREGA estas líneas para usar python-for-android actualizado
p4a.branch = develop

orientation = portrait
fullscreen = 1

[buildozer]
log_level = 2
warn_on_root = 1
MICROSERVICES_ROOT=$$PWD"/"

CFLIB_PATH=/usr/local/cflib

CONFIG += user-service

exists($${MICROSERVICES_ROOT}/local.pri) {
    include($${MICROSERVICES_ROOT}/local.pri)
}

include($${CFLIB_PATH}/include.pri)

INCLUDEPATH += $${EXT_INCLUDES} $${MICROSERVICES_ROOT} build/gen .

CONFIG += c++11

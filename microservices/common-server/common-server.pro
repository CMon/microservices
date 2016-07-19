!include(../../config.pri):error("Could not find config.pri")

QT -= gui
QT += sql

HEADERS += \
    database.h \

TARGET = common_server_lib

useLibs(cflib_serialize cflib_util cflib_libev)
lib($${MICROSERVICES_ROOT}/lib)
serializeGen()

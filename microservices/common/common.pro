!include(../../config.pri):error("Could not find config.pri")

QT -= gui

HEADERS += \
    permission.h \
    user.h \

TARGET = common_lib

useLibs(cflib_serialize cflib_util cflib_libev)
lib($${MICROSERVICES_ROOT}/lib)
serializeGen()

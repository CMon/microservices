!include(../../config.pri):error("Could not find config.pri")

QT -= gui

HEADERS += \
    app.h \
    permission.h \
    user.h \

TARGET = common_lib

useLibs(cflib_serialize cflib_util)
lib($${MICROSERVICES_ROOT}/lib)
serializeGen()

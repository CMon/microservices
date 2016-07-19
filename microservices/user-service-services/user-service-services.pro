!include(../../config.pri):error("Could not find config.pri")

QT -= gui
QT += network

HEADERS += \
    user-service-interface.h \

SOURCES += \
    user-service-interface.cpp \

TARGET = user_service_services_lib

useLibs(cflib_crypt)
lib($${MICROSERVICES_ROOT}/lib)
serializeGen()

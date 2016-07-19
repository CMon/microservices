!include(../../config.pri):error("Could not find config.pri")

QT       += network sql
QT       -= gui

TARGET = server

CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app

SOURCES += \
    dbapp.cpp \
    dbpermission.cpp \
    dbuser.cpp \
    main.cpp \

HEADERS += \
    dbapp.h \
    dbpermission.h \
    dbuser.h \


useLibs($${MICROSERVICES_ROOT}/lib, user_service_services_lib common_server_lib common_lib)

useLibs(cflib_db cflib_net cflib_crypt cflib_serialize cflib_util cflib_libev)
app()

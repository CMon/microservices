!include(../config.pri):error("Could not find config.pri")

addSubdir(common)
addSubdir(common-server)

CONFIG(user-service) {
    message("Building user-service")
    addSubdir(user-service-services, common-server common )
    addSubdir(user-service-server, common-server common )
}

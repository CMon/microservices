#pragma once

#include <cflib/net/rmiservice.h>
#include <common/permission.h>

class UserServiceInterface : public QObject, public cflib::net::RMIService<QString>
{
	Q_OBJECT
	SERIALIZE_CLASS

rmi:
//	createUser;
//	createApp;
//	addPermission(userId, appId, permissionId, data);
//	queryUsers;
//	queryApps;
	bool ping();


	QList<Permission> loginUser(const QString & username, const QString & password, const int appId);
};

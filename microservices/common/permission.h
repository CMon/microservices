#pragma once

#include <QByteArray>

class Permission
{
public:
	Permission(int permissionId, const QByteArray & data);

private:
	int permissionId_;
	QByteArray permissionData_;
};

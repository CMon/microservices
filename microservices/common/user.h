#pragma once

#include <common/permission.h>

#include <QList>
#include <QString>

class User {

private:
	int userId_;
	QString username_;
	QString password_;
	QList<Permission> permissions_;
};

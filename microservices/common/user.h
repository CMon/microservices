#pragma once

#include <common/permission.h>

#include <cflib/serialize/serialize.h>

#include <QList>
#include <QString>

class User 
{
	SERIALIZE_CLASS
public:
	User();
	User(const quint64 & id, const QString & login, const Permissions & permissions, const QString & firstName, const QString & lastName, bool isDeleted);
	
	quint64 userId() const;
	
	QString login() const;
	
	Permissions permissions() const;
	void setPermissions(const Permissions & permissions);
	
	QString firstName() const;
	void setFirstName(const QString & firstName);
	
	QString lastName() const;
	void setLastName(const QString & lastName);
	
	bool isDeleted() const;
	void setIsDeleted(bool isDeleted);
	
private serialized:
	quint64 userId_;
	QString login_;
	Permissions permissions_;
	QString firstName_;
	QString lastName_;
	bool    isDeleted_;
};

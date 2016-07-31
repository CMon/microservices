#include "user.h"



quint64 User::userId() const
{
	return userId_;
}

QString User::login() const
{
	return login_;
}

Permissions User::permissions() const
{
	return permissions_;
}

void User::setPermissions(const Permissions & permissions)
{
	permissions_ = permissions;
}

QString User::firstName() const
{
	return firstName_;
}

void User::setFirstName(const QString & firstName)
{
	firstName_ = firstName;
}

QString User::lastName() const
{
	return lastName_;
}

void User::setLastName(const QString & lastName)
{
	lastName_ = lastName;
}

bool User::isDeleted() const
{
	return isDeleted_;
}

void User::setIsDeleted(bool isDeleted)
{
	isDeleted_ = isDeleted;
}

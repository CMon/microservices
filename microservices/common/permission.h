#pragma once

#include <common/app.h>

#include <cflib/serialize/serialize.h>

#include <QByteArray>

class Permission
{
	SERIALIZE_CLASS
public:
	enum {
		InvalidPermission = -1
	} SpecialPermissions;
	Permission() : permissionId_(InvalidPermission) {}
	Permission(int permissionId, const QByteArray & data);

	int permissionId() const;
	QByteArray permissionData() const;
	
	bool isValid() const;
	
	bool operator==(const Permission & rhs) const;
	bool operator!=(const Permission & rhs) const { return !operator==(rhs); }
	
	QString toString() const;
	
private serialized:
	int permissionId_;
	QByteArray permissionData_;
};

inline uint qHash(const Permission & permission, uint seed = 0)
{
	return qHash(permission.toString(), seed);
}

/**
 * @brief The Permissions class
 * 
 * This class stores a set of applications with their corresponding permissions. If an app inside the permissions structure
 * is going to be empty it will be removed as well.
 */
class Permissions
{
	SERIALIZE_CLASS
	
public:
	/**
	 * @brief Permissions with no permission set
	 */
	Permissions() {}
	/**
	 * @brief Permissions with one permission set
	 * @param app the application this permission is for
	 * @param permission the initial permission that is set
	 */
	Permissions(const App & app, const Permission & permission);
	/**
	 * @brief Permissions with a set of permissions set
	 * @param app the application this permissions are for
	 * @param permissions the initial permissions that are set
	 */
	Permissions(const App & app, const QSet<Permission> & permissions);
	
	/**
	 * @brief contains checks if this set contains the given permission
	 * @param app the application this permission is checked for
	 * @param permission the permission that is checked for containment
	 * @return true if found, false if not
	 */
	bool contains(const App & app, const Permission & permission) const;
	/**
	 * @brief insert the given permission
	 * @param app the application this permission is added for
	 * @param permission the permission that is inserted
	 */
	void insert(const App & app, const Permission & permission);
	/**
	 * @brief remove the given permission, and if the app does not contain any permissions anymore this is removed as well
	 * @param app the application this permission is removed from
	 * @param permission the permission that should be removed
	 */
	void remove(const App & app, const Permission & permission);

	bool operator==(const Permissions & rhs) const { return permissions_ == rhs.permissions_; }
	bool operator!=(const Permissions & rhs) const { return !operator ==(rhs); }

private serialized:
	QHash<App, QSet<Permission>> permissions_;
};

#include "permission.h"

Permission::Permission(int permissionId, const QByteArray & data)
    : permissionId_(permissionId),
      permissionData_(data)
{
	if (permissionId_ == InvalidPermission) {
		permissionData_.clear();
	} 
}

int Permission::permissionId() const
{
	return permissionId_;
}

QByteArray Permission::permissionData() const
{
	return permissionData_;
}

bool Permission::isValid() const
{
	return permissionId_ != InvalidPermission;
}

bool Permission::operator==(const Permission & rhs) const 
{ 
	return
	        permissionId_ == rhs.permissionId_ &&
	        permissionData_ == rhs.permissionData_; 
}

QString Permission::toString() const
{
	return QString::number(permissionId_) + ":" + qPrintable(permissionData_);
}

Permissions::Permissions(const App & app, const Permission & permission)
{
	permissions_[app] << permission;
}

Permissions::Permissions(const App & app, const QSet<Permission> & permissions)
{
	permissions_[app] = permissions;
}

bool Permissions::contains(const App & app, const Permission & permission) const
{
	if (!permissions_.contains(app)) return false;
	return permissions_.value(app).contains(permission);
}

void Permissions::insert(const App & app, const Permission & permission)
{
	permissions_[app].insert(permission);
}

void Permissions::remove(const App & app, const Permission & permission)
{
	if (!permissions_.contains(app)) return;
	
	permissions_[app].remove(permission);
	if (permissions_.value(app).isEmpty()) permissions_.remove(app);
}

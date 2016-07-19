#pragma once

class User;
class Permission;

namespace DB {
bool addPermission(const User & user, const Permission & permission);
}

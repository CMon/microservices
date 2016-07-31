#include "app.h"

App::App(const quint64 & appId, const QString & name)
    : appId_(appId)
    , appName_(name.toUtf8())
{
	if (appId_ == InvalidAppId) appName_.clear();
}

quint64 App::appId() const
{
	return appId_;
}

QString App::appName() const
{
	return appName_;
}

bool App::isValid() const
{
	return appId_ != InvalidAppId;
}

bool App::operator==(const App & rhs) const
{
	return 
	        appId_   == rhs.appId_ &&
	        appName_ == rhs.appName_;
}

QString App::toString() const
{
	return QString::number(appId_) + ":" + qPrintable(appName_);
}

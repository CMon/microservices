#pragma once

#include <cflib/serialize/serialize.h>

/**
 * @brief The App class
 * 
 * This class contains the bare minimum information of each application that is registered on the system. It is used to
 * identify the permissions of a user.
 * 
 * This class is serializable over the network
 */
//FIXME: in doxy make link to permissions and user
class App
{
	SERIALIZE_CLASS
public:
	enum {
		InvalidAppId
	} SpecialAppIds;
	/**
	 * @brief App creates an invalid App object
	 */
	App() : appId_(InvalidAppId) {}
	/**
	 * @brief App creates a valid App object
	 * @param appId The id of the application
	 * @param name  The name of the application
	 */
	App(const quint64 & appId, const QString & name);

	/**
	 * @brief appId returns the application id of this application
	 * @return the application id
	 */
	quint64 appId() const;
	/**
	 * @brief appName returns the application name of this application
	 * @return the application name
	 */
	QString appName() const;
	
	/**
	 * @brief isValid checks if this application is valid
	 * @return true if valid, false if not
	 */
	//FIXME: in doxy how to make link to InvalidAppId?
	//FIXME: in doxy make true and false bold
	bool isValid() const;
	
	bool operator==(const App & rhs) const;
	bool operator!=(const App & rhs) const { return !operator==(rhs); }
	
	/**
	 * @brief toString a non localized string output of this class
	 * @return the string representation of this class
	 */
	QString toString() const;
	
private serialized:
	quint64 appId_;
	QByteArray appName_;
};

inline uint qHash(const App & app, uint seed = 0)
{
	return qHash(app.toString(), seed);
}

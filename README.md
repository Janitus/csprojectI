Admin user info:

username: admin
pw: admin

Information on five issues:

Issue one: Identification and Authentication failures, people can choose whichever password they wish to.
When fixed: You should be required to fulfill some password requirements

Issue two: Broken access control, user is able to update bio of accounts that they aren't the owners of.
When fixed: You should only be able to update your own bio on the account you're logged in.

Issue three: Security misconfiguration, unnecessary feature. When the person logs out, they will be moved into django's default logout page, which contains link to admin login.
When fixed: You should be moved directly into root page

Issue four: Security Logging and Monitoring Failures. We wish to see who logs into our system, from where and when so we can detect suspicious activity.
When fixed: You should be able to see logins per user, IP address and time. The logs are logged into the user_activity.log in the root directory.

Issue five: Insecure design. We're preventing a user account from being accessed after too many failed logins in a short period of time to prevent bruteforces.
When fixed: You should no longer be able to login to an account if you fail to login into it for the first 3 times. The lockout timer is 30 seconds.
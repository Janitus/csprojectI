Admin user info:

username: admin
pw: admin

-------------- Instructions --------------

1. Clone this project to your own directory
2. Navigate there with cmd
3. python manage.py runserver

On the website you can register, login and change the bio in your account.
Note that there is one bug upon registering your account (You will receive erorr IntegrityError at /register/ UNIQUE constraint failed: mysite_profile.user_id), but this does not hinder your ability to log in or test the site otherwise.

I have included some test accounts to try, information on them:

Username - Password

a - 1

b - 1

-------------- Issues below --------------

Information on five issues:

Format:
Issue - Category and details of the problem
How to fix - Instructions are found right under the issue on the links

Issue one: Identification and Authentication failures, people can choose whichever password they wish to.
When fixed: You should be required to fulfill some password requirements
Link: https://github.com/Janitus/csprojectI/blob/33261f141119fbeb0610912df6ed2f5968e2ce8d/mysite/settings.py#L95

Issue two: Broken access control, user is able to update bio of accounts that they aren't the owners of.
When fixed: You should only be able to update your own bio on the account you're logged in.
Link: https://github.com/Janitus/csprojectI/blob/33261f141119fbeb0610912df6ed2f5968e2ce8d/mysite/views.py#L98

Issue three: Security misconfiguration, unnecessary feature. When the person logs out, they will be moved into django's default logout page, which contains link to admin login.
When fixed: You should be moved directly into root page
Link: https://github.com/Janitus/csprojectI/blob/33261f141119fbeb0610912df6ed2f5968e2ce8d/mysite/settings.py#L19

Issue four: Security Logging and Monitoring Failures. We wish to see who logs into our system, from where and when so we can detect suspicious activity.
When fixed: You should be able to see logins per user, IP address and time. The logs are logged into the user_activity.log in the root directory.
Link: https://github.com/Janitus/csprojectI/blob/33261f141119fbeb0610912df6ed2f5968e2ce8d/mysite/views.py#L27

Issue five: Insecure design. We're preventing a user account from being accessed after too many failed logins in a short period of time to prevent bruteforces.
When fixed: You should no longer be able to login to an account if you fail to login into it for the first 3 times. The lockout timer is 30 seconds.
Link: https://github.com/Janitus/csprojectI/blob/33261f141119fbeb0610912df6ed2f5968e2ce8d/mysite/views.py#L31
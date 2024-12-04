#
# Regular cron jobs for the nautilus-uri-bookmark package.
#
0 4	* * *	root	[ -x /usr/bin/nautilus-uri-bookmark_maintenance ] && /usr/bin/nautilus-uri-bookmark_maintenance

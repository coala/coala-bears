from bears.configfiles.NginxBear import NginxBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """
http{
    server {
        listen 80;

        server_name example.com www.example.com;

        root /usr/local/www/example.com;

        access_log /var/log/nginx/example.access.log;
        error_log /var/log/nginx/example.error.log;
    }
}
"""

bad_file = """
http{
    server {
        listen 80;

        server_name example.com www.example.com;

        root /usr/local/www/example.com;

        access_log /var/log/nginx/example.access.log;
        error_log /var/log/nginx/example.error.log;
    }
"""

NginxBearTest = verify_local_bear(NginxBear,
                                  valid_files=(good_file, ),
                                  invalid_files=(bad_file, ))

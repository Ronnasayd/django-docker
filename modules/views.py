#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MIT License

# Copyright (c) 2019 Ronnasayd de Sousa Machado

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

### VERSION: 2.3.3-beta ###

################################################################
                    ## NGIX TEMPLATE ##
################################################################
NGINX_CONFIGURATIN_BASE='''
worker_processes 1;

events {{

    worker_connections 1024;

}}

http {{

    proxy_cache_path {STATIC_ROOT} levels=1:2 keys_zone=my_cache:10m max_size=10g 
        inactive=60m use_temp_path=off;

    default_type  application/octet-stream;
    include       /etc/nginx/mime.types;

    log_format compression '$remote_addr - $remote_user [$time_local] '
                           '"$request" $status $body_bytes_sent '
                           '"$http_referer" "$http_user_agent" "$gzip_ratio"';
   




    sendfile on;

    gzip              on;
    gzip_http_version 1.0;
    gzip_proxied      any;
    gzip_min_length   500;
    gzip_disable      "MSIE [1-6]\\.";
    gzip_types        text/plain text/xml text/css
                      text/comma-separated-values
                      text/javascript
                      application/x-javascript
                      application/atom+xml;

    # Configuration containing list of application servers
    upstream app_servers {{
        ip_hash;
        server {WEB_CONTAINER_NAME}:{WEB_PORT};

    }}

    # Configuration for Nginx
    server {{

        #access_log {LOGS_ROOT}/access.log compression;
        error_log {LOGS_ROOT}/error.log warn;
        

        # Running port
        listen {WEB_PORT};

        # Max_size
        client_max_body_size 20M;

        # Settings to serve static files 
        location /static/  {{

            # Example:
            # root /full/path/to/application/static/file/dir;
            autoindex on;
            alias {STATIC_ROOT}/;

        }}

        location /media/ {{

            autoindex on;
            alias {MEDIA_ROOT}/;
        }}

       

        # Proxy connections to the application servers
        # app_servers
        location / {{


            proxy_cache my_cache;
            proxy_cache_revalidate on;
            proxy_cache_min_uses 3;
            proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
            proxy_cache_background_update on;
            proxy_cache_lock on;

            proxy_pass         http://app_servers;
            proxy_redirect     off;
            proxy_set_header   Host $host;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header   X-Forwarded-Host $server_name;


        }}
    }}
}}

'''
####################################################################
                        ## GULPFILE TEMPLATE ##
####################################################################
GULPFILE_BASE='''
var gulp        = require('gulp');
var browserSync = require('browser-sync').create();
var sass        = require('gulp-sass');
var rename      = require('gulp-rename');
var autoprefixer = require('gulp-autoprefixer');
var uglify = require('gulp-uglify');
var sourcemaps = require('gulp-sourcemaps');
var imagemin = require('gulp-imagemin');

// Static Server + watching scss/html files
gulp.task('serve', ['sass','js'], function() {{

   
    browserSync.init({{
        open: false,
        proxy: {{
          target: "http://{WEB_CONTAINER_NAME}:{WEB_PORT}",
          ws: true,
        }}
    }});

    gulp.watch("**/**/static/{SCSS_FOLDERS}/**/*.scss", ['sass']);
    gulp.watch("**/**/static/{JS_FOLDERS}/**/*.js", ['js-watch']);
    gulp.watch("**/*.html").on('change', browserSync.reload);
    gulp.watch("**/*.css").on('change', browserSync.reload);
    gulp.watch(["**/*.js","!**/**/static/{JS_FOLDERS}/**/*.js","!**/**/static/{JSMIN_FOLDERS}/**/*.js"]).on('change', browserSync.reload);
}});


// create a task that ensures the `js` task is complete before
// reloading browsers
gulp.task('js-watch', ['js'], function (done) {{
    browserSync.reload();
    done();
}});


gulp.task('js',function(){{
    return gulp.src(["**/**/static/{JS_FOLDERS}/**/*.js","!gulpfile.js",'!node_modules/**'])
    .pipe(sourcemaps.init())
    .pipe(uglify()).on('error',function(err){{
            console.log(err.message);
            console.log(err.cause);
            browserSync.notify(err.message, 3000); // Display error in the browser
            this.emit('end'); // Prevent gulp from catching the error and exiting the watch process
     }})
    .pipe(rename(function(file){{
            file.dirname = file.dirname.replace('{JS_FOLDERS}','{JSMIN_FOLDERS}');
            file.extname = ".min.js"
     }}))
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest("."))
}});

gulp.task('imagemin',function(){{
  return gulp.src(["**/**/static/{IMAGE_FOLDERS}/**/*"])
  .pipe(imagemin({{verbose:true}}))
  .pipe(gulp.dest("."))
}});


// Compile sass into CSS & auto-inject into browsers
gulp.task('sass', function() {{
    return gulp.src(["**/**/static/{SCSS_FOLDERS}/**/*.scss",'!node_modules/**'])
        .pipe(sourcemaps.init())
        .pipe(sass({{
            errLogToConsole: true,
            indentedSyntax: false,
            outputStyle: 'compressed'
        }}).on('error',function(err){{
            console.log(err.message);
            browserSync.notify(err.message, 3000); // Display error in the browser
            this.emit('end'); // Prevent gulp from catching the error and exiting the watch process
        }}))
        .pipe(autoprefixer({{
            browsers: ['last 100 versions'],
            cascade: false
        }}))
        .pipe(rename(function(file){{
            file.dirname = file.dirname.replace('{SCSS_FOLDERS}','{CSS_FOLDERS}');
        }}))
        .pipe(sourcemaps.write('./'))
        .pipe(gulp.dest("."))
        .pipe(browserSync.stream());
}});

gulp.task('default', ['serve']);
'''
########################################################################
                        ## GULP SCRIPT ##
########################################################################
GULP_SCRIPT_BEGIN ='''
#!/bin/bash
file="./package.json"
if [ ! -f "$file" ]
then
'''
GULP_ADD='''  yarn add {}
'''

GULP_SCRIPT_END='''  gulp
else
  yarn
  gulp
fi
'''
####################################################################
                    ## MAKE AMBIENT SCRIPT ##
####################################################################
MAKE_AMBIENT_BASE='''
chmod +x {FOLDER_NAME}/wait-for-it.sh
sed -i "s/\\r$//" {FOLDER_NAME}/{RUNSERVER_SCRIPT_NAME}
sed -i "s/\\r$//" {FOLDER_NAME}/wait-for-it.sh
sed -i "s/\\r$//" {FOLDER_NAME}/gulpfile.js
sed -i "s/\\r$//" {FOLDER_NAME}/gulp.sh
cp {FOLDER_NAME}/{RUNSERVER_SCRIPT_NAME} ./{PROJECT_NAME}
cp {FOLDER_NAME}/wait-for-it.sh ./{PROJECT_NAME}
cp {FOLDER_NAME}/gulpfile.js ./{PROJECT_NAME}
cp {FOLDER_NAME}/gulp.sh ./{PROJECT_NAME}
'''

MAKE_AMBIENT_DEVELOPMENT='''docker-compose -f {FOLDER_NAME}/{PROJECT_NAME}_development.yml stop
docker-compose -f {FOLDER_NAME}/{PROJECT_NAME}_production.yml stop
docker-compose -f {FOLDER_NAME}/{PROJECT_NAME}_development.yml down
docker-compose -f {FOLDER_NAME}/{PROJECT_NAME}_production.yml down
docker system prune --force
docker-compose -f {FOLDER_NAME}/{PROJECT_NAME}_development.yml build
COMPOSE_HTTP_TIMEOUT=3600 docker-compose -f {FOLDER_NAME}/{PROJECT_NAME}_development.yml up  --force-recreate'''


MAKE_AMBIENT_PRODUCTION='''docker-compose -f {FOLDER_NAME}/{PROJECT_NAME}_production.yml stop
docker-compose -f {FOLDER_NAME}/{PROJECT_NAME}_development.yml stop
docker-compose -f {FOLDER_NAME}/{PROJECT_NAME}_production.yml down
docker-compose -f {FOLDER_NAME}/{PROJECT_NAME}_development.yml down
docker system prune --force
docker-compose -f {FOLDER_NAME}/{PROJECT_NAME}_production.yml build
docker-compose -f {FOLDER_NAME}/{PROJECT_NAME}_production.yml up  -d  --force-recreate'''

######################################################################
                    ## RUNSERVER SCRIPT ##
######################################################################
RUNSERVER_SCRIPT_BASE='''#!/bin/bash
python manage.py makemigrations
python manage.py migrate'''


RUNSERVER_SCRIPT_DEVELOPMENT='''
python manage.py runserver 0.0.0.0:{WEB_PORT}
'''

RUNSERVER_SCRIPT_PRODUCTION='''
python manage.py collectstatic --noinput
gunicorn --bind=0.0.0.0:{WEB_PORT} --workers=3 {PROJECT_NAME}.wsgi
'''

######################################################################
                    ## WAIT-FOR-IT SCRIPT ##
######################################################################
WAIT_FOR_IT='''#!/usr/bin/env bash
#   Use this script to test if a given TCP host/port are available

WAITFORIT_cmdname=${0##*/}

echoerr() { if [[ $WAITFORIT_QUIET -ne 1 ]]; then echo "$@" 1>&2; fi }

usage()
{
    cat << USAGE >&2
Usage:
    $WAITFORIT_cmdname host:port [-s] [-t timeout] [-- command args]
    -h HOST | --host=HOST       Host or IP under test
    -p PORT | --port=PORT       TCP port under test
                                Alternatively, you specify the host and port as host:port
    -s | --strict               Only execute subcommand if the test succeeds
    -q | --quiet                Don't output any status messages
    -t TIMEOUT | --timeout=TIMEOUT
                                Timeout in seconds, zero for no timeout
    -- COMMAND ARGS             Execute command with args after the test finishes
USAGE
    exit 1
}

wait_for()
{
    if [[ $WAITFORIT_TIMEOUT -gt 0 ]]; then
        echoerr "$WAITFORIT_cmdname: waiting $WAITFORIT_TIMEOUT seconds for $WAITFORIT_HOST:$WAITFORIT_PORT"
    else
        echoerr "$WAITFORIT_cmdname: waiting for $WAITFORIT_HOST:$WAITFORIT_PORT without a timeout"
    fi
    WAITFORIT_start_ts=$(date +%s)
    while :
    do
        if [[ $WAITFORIT_ISBUSY -eq 1 ]]; then
            nc -z $WAITFORIT_HOST $WAITFORIT_PORT
            WAITFORIT_result=$?
        else
            (echo > /dev/tcp/$WAITFORIT_HOST/$WAITFORIT_PORT) >/dev/null 2>&1
            WAITFORIT_result=$?
        fi
        if [[ $WAITFORIT_result -eq 0 ]]; then
            WAITFORIT_end_ts=$(date +%s)
            echoerr "$WAITFORIT_cmdname: $WAITFORIT_HOST:$WAITFORIT_PORT is available after $((WAITFORIT_end_ts - WAITFORIT_start_ts)) seconds"
            break
        fi
        sleep 1
    done
    return $WAITFORIT_result
}

wait_for_wrapper()
{
    # In order to support SIGINT during timeout: http://unix.stackexchange.com/a/57692
    if [[ $WAITFORIT_QUIET -eq 1 ]]; then
        timeout $WAITFORIT_BUSYTIMEFLAG $WAITFORIT_TIMEOUT $0 --quiet --child --host=$WAITFORIT_HOST --port=$WAITFORIT_PORT --timeout=$WAITFORIT_TIMEOUT &
    else
        timeout $WAITFORIT_BUSYTIMEFLAG $WAITFORIT_TIMEOUT $0 --child --host=$WAITFORIT_HOST --port=$WAITFORIT_PORT --timeout=$WAITFORIT_TIMEOUT &
    fi
    WAITFORIT_PID=$!
    trap "kill -INT -$WAITFORIT_PID" INT
    wait $WAITFORIT_PID
    WAITFORIT_RESULT=$?
    if [[ $WAITFORIT_RESULT -ne 0 ]]; then
        echoerr "$WAITFORIT_cmdname: timeout occurred after waiting $WAITFORIT_TIMEOUT seconds for $WAITFORIT_HOST:$WAITFORIT_PORT"
    fi
    return $WAITFORIT_RESULT
}

# process arguments
while [[ $# -gt 0 ]]
do
    case "$1" in
        *:* )
        WAITFORIT_hostport=(${1//:/ })
        WAITFORIT_HOST=${WAITFORIT_hostport[0]}
        WAITFORIT_PORT=${WAITFORIT_hostport[1]}
        shift 1
        ;;
        --child)
        WAITFORIT_CHILD=1
        shift 1
        ;;
        -q | --quiet)
        WAITFORIT_QUIET=1
        shift 1
        ;;
        -s | --strict)
        WAITFORIT_STRICT=1
        shift 1
        ;;
        -h)
        WAITFORIT_HOST="$2"
        if [[ $WAITFORIT_HOST == "" ]]; then break; fi
        shift 2
        ;;
        --host=*)
        WAITFORIT_HOST="${1#*=}"
        shift 1
        ;;
        -p)
        WAITFORIT_PORT="$2"
        if [[ $WAITFORIT_PORT == "" ]]; then break; fi
        shift 2
        ;;
        --port=*)
        WAITFORIT_PORT="${1#*=}"
        shift 1
        ;;
        -t)
        WAITFORIT_TIMEOUT="$2"
        if [[ $WAITFORIT_TIMEOUT == "" ]]; then break; fi
        shift 2
        ;;
        --timeout=*)
        WAITFORIT_TIMEOUT="${1#*=}"
        shift 1
        ;;
        --)
        shift
        WAITFORIT_CLI=("$@")
        break
        ;;
        --help)
        usage
        ;;
        *)
        echoerr "Unknown argument: $1"
        usage
        ;;
    esac
done

if [[ "$WAITFORIT_HOST" == "" || "$WAITFORIT_PORT" == "" ]]; then
    echoerr "Error: you need to provide a host and port to test."
    usage
fi

WAITFORIT_TIMEOUT=${WAITFORIT_TIMEOUT:-15}
WAITFORIT_STRICT=${WAITFORIT_STRICT:-0}
WAITFORIT_CHILD=${WAITFORIT_CHILD:-0}
WAITFORIT_QUIET=${WAITFORIT_QUIET:-0}

# check to see if timeout is from busybox?
WAITFORIT_TIMEOUT_PATH=$(type -p timeout)
WAITFORIT_TIMEOUT_PATH=$(realpath $WAITFORIT_TIMEOUT_PATH 2>/dev/null || readlink -f $WAITFORIT_TIMEOUT_PATH)
if [[ $WAITFORIT_TIMEOUT_PATH =~ "busybox" ]]; then
        WAITFORIT_ISBUSY=1
        WAITFORIT_BUSYTIMEFLAG="-t"

else
        WAITFORIT_ISBUSY=0
        WAITFORIT_BUSYTIMEFLAG=""
fi

if [[ $WAITFORIT_CHILD -gt 0 ]]; then
    wait_for
    WAITFORIT_RESULT=$?
    exit $WAITFORIT_RESULT
else
    if [[ $WAITFORIT_TIMEOUT -gt 0 ]]; then
        wait_for_wrapper
        WAITFORIT_RESULT=$?
    else
        wait_for
        WAITFORIT_RESULT=$?
    fi
fi

if [[ $WAITFORIT_CLI != "" ]]; then
    if [[ $WAITFORIT_RESULT -ne 0 && $WAITFORIT_STRICT -eq 1 ]]; then
        echoerr "$WAITFORIT_cmdname: strict mode, refusing to execute subprocess"
        exit $WAITFORIT_RESULT
    fi
    exec "${WAITFORIT_CLI[@]}"
else
    exit $WAITFORIT_RESULT
fi'''
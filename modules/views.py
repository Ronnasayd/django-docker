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

# VERSION: 4.0.0-beta #

################################################################
                    ## NGIX TEMPLATE ##
################################################################
NGINX_CONFIGURATIN_BASE = '''
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
        {SERVERS}
        

    }}

    # Configuration for Nginx
    server {{
        

        #access_log {LOGS_ROOT}/access.log compression;
        error_log {LOGS_ROOT}/error.log warn;
        

        # Running port
        listen {WEB_PORT};
        listen [::]:{WEB_PORT};

        listen 80;
        listen [::]:80;

        
        {NGINX_SNIPPET_HTTPS}
        

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
                        ## NGINX_SNIPPET TEMPLATE ##
####################################################################
NGINX_SNIPPET_HTTPS='''
        root {WEB_ROOT_PATH};
            index index.html intex.htm index.nginx-debian.html;

        server_name {SERVER_DNS_NAMES};

        location ~ /.well-known/acme-challenge{{
            allow all;
            root {WEB_ROOT_PATH};
        }}'''
####################################################################
                        ## NGINX_SCRIPT TEMPLATE ##
####################################################################
NGINX_CERT_SCRIPT='''certbot certonly  --webroot --webroot-path={WEB_ROOT_PATH} --agree-tos --no-eff-email --force-renewal {SERVER_NAMES} && certbot --nginx'''
####################################################################
                        ## GULPFILE TEMPLATE ##
####################################################################
GULPFILE_BASE = '''
const gulp            = require("gulp");
const browserSync     = require("browser-sync").create();
const sass            = require("gulp-sass");
const rename          = require("gulp-rename");
const autoprefixer    = require("gulp-autoprefixer");
const uglify          = require("gulp-uglify");
const sourcemaps      = require("gulp-sourcemaps");
const imagemin        = require("gulp-imagemin");
const cleanCSS        = require("gulp-clean-css");
const purgecss        = require("gulp-purgecss");
const cache           = require("gulp-cached");
const minimist        = require("minimist");
const concat          = require("gulp-concat");
const sassPartials    = require('gulp-sass-partials-imported');
const jshint          = require('gulp-jshint');



const src_scss        = "static/src/scss/**/*.scss";
const src_css         = "static/src/css/**/*.css";
const src_js          = "static/src/js/**/*.js";

const images_folder   = "static/images/**/*.{{png,jpeg,jpg,svg,ico}}";

const not_node        = "!node_modules/"

const dist_js         = "static/dist/js/"
const dist_css        = "static/dist/css/"


const html_files      = "**/*.html"


const jsHint = ()=>{{
    return gulp.src([src_js,not_node],{{allowEmpty: true}})
    .pipe(cache("jsHint"))
    .pipe(jshint())
    .pipe(jshint.reporter('default'));
}}

const minifyJs = ()=>{{
    return gulp.src([src_js,not_node],{{allowEmpty: true}})
    .pipe(cache("minifyJs"))
    .pipe(sourcemaps.init())
    .pipe(uglify()).on("error",function(err){{
            console.log(err.message);
            console.log(err.cause);
            browserSync.notify(err.message, 3000); // Display error in the browser
            this.emit("end"); // Prevent gulp from catching the error and exiting the watch process
     }})
    .pipe(rename(function(file){{
            file.extname = ".min.js"
     }}))
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest(dist_js))
}}

const sassToCssMin = ()=>{{
    return gulp.src([src_scss,"!_*.scss",not_node],{{allowEmpty: true}})
        .pipe(cache("sassToCssMin"))
        .pipe(sassPartials("static/src/scss"))
        .pipe(sourcemaps.init({{loadMaps: true, largeFile: true}}))
        .pipe(sass({{
            errLogToConsole: true,
            indentedSyntax: false,
        }}).on("error",function(err){{
            console.log(err.message);
            browserSync.notify(err.message, 3000); // Display error in the browser
            this.emit("end"); // Prevent gulp from catching the error and exiting the watch process
        }}))
        .pipe(autoprefixer({{
            browsers: ["last 100 versions"],
            cascade: false
        }}))
        .pipe(purgecss({{content: [html_files,not_node]}}))
        .on("error",function(err){{
            console.log(err.message,err);
            browserSync.notify(err.message, 3000); // Display error in the browser
            this.emit("end"); // Prevent gulp from catching the error and exiting the watch process
        }})
        .pipe(cleanCSS())
        .pipe(rename(function(file){{
            file.extname = ".min.css"
        }}))
        .pipe(sourcemaps.write('./'))
        .pipe(gulp.dest(dist_css))
        .pipe(browserSync.stream())
}}

const minifyCss = ()=>{{
    return gulp.src([src_css,"!_*.css", not_node],{{allowEmpty: true}})
    .pipe(cache("minifyCss"))
    .pipe(sourcemaps.init({{loadMaps: true, largeFile: true}}))
    .pipe(autoprefixer({{
        browsers: ["last 100 versions"],
        cascade: false
    }}))
    .pipe(purgecss({{content: [html_files,not_node]}}))
    .on("error",function(err){{
        console.log(err.message,err);
        browserSync.notify(err.message, 3000); // Display error in the browser
        this.emit("end"); // Prevent gulp from catching the error and exiting the watch process
    }})
    .pipe(cleanCSS())
    .pipe(rename(function(file){{
        file.extname = ".min.css"
    }}))
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest(dist_css))
    .pipe(browserSync.stream())
}}


//  gulp concatfiles --files <list_of_files:file1,file2,file3> --name <name_of_file:all.js> --dist <destination>
const concatFiles = ()=>{{
    let options = minimist(process.argv.slice(2));
    console.log("files: "+options.files);
    console.log("name: "+options.name);
    console.log("dist: "+options.dist);
    return gulp.src(options.files.split(","),{{base: "./", allowEmpty: true}})
    .pipe(cache("concatFiles"))
    .pipe(sourcemaps.init())
    .pipe(concat(options.name))
    .pipe(sourcemaps.write("./"))
    .pipe(gulp.dest(options.dist))
}}



const browserReload = (done)=>{{
    browserSync.reload();
    done();
}}

const minifyImages =()=>{{
    return gulp.src([images_folder,not_node],{{base: "./",allowEmpty: true}})
    .pipe(cache("minifyImages"))
    .pipe(imagemin([
        imagemin.gifsicle({{interlaced: true}}),
        imagemin.jpegtran({{progressive: true}}),
        imagemin.optipng({{optimizationLevel: 5}}),
        imagemin.svgo({{
            plugins: [
                {{removeViewBox: true}},
                {{cleanupIDs: false}}
            ]
        }})
    ]))
    .pipe(gulp.dest("./"))
}}


const js_line = gulp.series(jsHint,minifyJs);
const sass_line = gulp.series(sassToCssMin)
const css_line = gulp.series(minifyCss);
const image_line = gulp.series(minifyImages);


const browserSyncServer = ()=>{{
    browserSync.init({{
        open: false,
        proxy: {{
          target: "http://{WEB_CONTAINER_NAME}:{WEB_PORT}",
          ws: true,
        }}
    }});

    gulp.watch(src_scss, {{interval: 100, usePolling: true}}, sass_line);
    gulp.watch(src_css, {{interval: 100, usePolling: true}}, css_line);
    gulp.watch(src_js, {{interval: 100, usePolling: true}}, gulp.series(js_line,browserReload));
    gulp.watch(images_folder, {{interval: 100, usePolling: true}}, image_line);
    gulp.watch(html_files, {{interval: 100, usePolling: true}}, gulp.series(browserReload));
}}

const server = gulp.series(gulp.parallel(js_line, css_line, sass_line, image_line),browserSyncServer)

exports.concatfiles = concatFiles
exports.default  = server

'''
####################################################################
                    ## MAKE AMBIENT SCRIPT ##
####################################################################
MAKE_AMBIENT_BASE='''
#!/bin/bash

if [ ! -d "{PROJECT_NAME}/static" ]; then
  mkdir {PROJECT_NAME}/static
  mkdir {PROJECT_NAME}/static/src
  mkdir {PROJECT_NAME}/static/src/css
  mkdir {PROJECT_NAME}/static/src/scss
  mkdir {PROJECT_NAME}/static/src/js
fi

if [ ! -f "{PROJECT_NAME}/Pipfile" ]; then
    sed -i "s/\\r$//" {FOLDER_NAME}/Pipfile
    sed -i "s/\\r$//" {FOLDER_NAME}/Pipfile.lock
    cp {FOLDER_NAME}/Pipfile ./{PROJECT_NAME}
    cp {FOLDER_NAME}/Pipfile.lock ./{PROJECT_NAME}
fi

trap cleanup 1 2 3 6
cleanup()
{{
  echo "Caught Signal ... cleaning up."
  rm {PROJECT_NAME}/runserver.sh
  rm {PROJECT_NAME}/gulpfile.js
  rm {PROJECT_NAME}/wait-for-it.sh
  rm {PROJECT_NAME}/package.json
  echo "Done cleanup ... quitting."
  exit 1
}}
chmod +x {FOLDER_NAME}/wait-for-it.sh
sed -i "s/\\r$//" {FOLDER_NAME}/{RUNSERVER_SCRIPT_NAME}
sed -i "s/\\r$//" {FOLDER_NAME}/wait-for-it.sh
sed -i "s/\\r$//" {FOLDER_NAME}/gulpfile.js
sed -i "s/\\r$//" {FOLDER_NAME}/package.json
sed -i "s/\\r$//" {FOLDER_NAME}/ddsettings.py
sed -i "s/\\r$//" {FOLDER_NAME}/ddurls.py
sed -i "s/\\r$//" {FOLDER_NAME}/manage.py
sed -i "s/\\r$//" {FOLDER_NAME}/.dockerignore

cp {FOLDER_NAME}/{RUNSERVER_SCRIPT_NAME} ./{PROJECT_NAME}
cp {FOLDER_NAME}/wait-for-it.sh ./{PROJECT_NAME}
cp {FOLDER_NAME}/gulpfile.js ./{PROJECT_NAME}
cp {FOLDER_NAME}/package.json ./{PROJECT_NAME}
cp {FOLDER_NAME}/manage.py ./{PROJECT_NAME}
cp {FOLDER_NAME}/ddsettings.py ./{PROJECT_NAME}/{PROJECT_NAME}
cp {FOLDER_NAME}/ddurls.py ./{PROJECT_NAME}/{PROJECT_NAME}
cp {FOLDER_NAME}/.dockerignore ./
'''

MAKE_AMBIENT_DEVELOPMENT='''docker-compose -f {FOLDER_NAME}/{PROJECT_NAME}_development.yml stop
docker-compose -p dd -f {FOLDER_NAME}/{PROJECT_NAME}_production.yml stop
docker-compose -p dd -f {FOLDER_NAME}/{PROJECT_NAME}_development.yml down
docker-compose -p dd -f {FOLDER_NAME}/{PROJECT_NAME}_production.yml down
docker system prune --force
docker-compose -p dd -f {FOLDER_NAME}/{PROJECT_NAME}_development.yml build
COMPOSE_HTTP_TIMEOUT=3600 docker-compose -p dd -f {FOLDER_NAME}/{PROJECT_NAME}_development.yml up  --force-recreate'''


MAKE_AMBIENT_PRODUCTION='''docker-compose -p dd -f {FOLDER_NAME}/{PROJECT_NAME}_production.yml stop
docker-compose -p dd -f {FOLDER_NAME}/{PROJECT_NAME}_development.yml stop
docker-compose -p dd -f {FOLDER_NAME}/{PROJECT_NAME}_production.yml down
docker-compose -p dd -f {FOLDER_NAME}/{PROJECT_NAME}_development.yml down
docker system prune --force
docker-compose -p dd -f {FOLDER_NAME}/{PROJECT_NAME}_production.yml build
docker-compose -p dd -f {FOLDER_NAME}/{PROJECT_NAME}_production.yml up  -d {SCALE} --force-recreate'''

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
DJANGO_SETTINGS_MODULE={PROJECT_NAME}.{SETTINGS_FILE_NAME} gunicorn --bind=0.0.0.0:{WEB_PORT} --workers=3 {PROJECT_NAME}.wsgi
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
######################################################################
                    ## SETTINGS FILE ##
######################################################################
SETTINGS='''
from .settings import *
from decouple import config
import os

DEBUG = config('DEBUG', default=False, cast=bool)
STATIC_ROOT = config('STATIC_ROOT')
MEDIA_ROOT = config('MEDIA_ROOT')
STATIC_URL = config('STATIC_URL')
MEDIA_URL = config('MEDIA_URL')

try:
    if "default" not in DATABASES:
        DATBASE_AUX = {{
            "default": {{
                'ENGINE': config('DATABASE_ENGINE'),
                'HOST': config('DATABASE_HOST'),
                'PORT': config('DATABASE_PORT'),
                'NAME': config('DATABASE_NAME'),
                'USER': config('DATABASE_USER'),
                'PASSWORD': config('DATABASE_PASSWORD')
            }}
        }}
        DATABASES.update(DATBASE_AUX)
    else:
        DATABASES["default"] = {{
            'ENGINE': config('DATABASE_ENGINE'),
            'HOST': config('DATABASE_HOST'),
            'PORT': config('DATABASE_PORT'),
            'NAME': config('DATABASE_NAME'),
            'USER': config('DATABASE_USER'),
            'PASSWORD': config('DATABASE_PASSWORD')
        }}

except (KeyError, NameError) as err:
    DATABASES = {{
        'default': {{
            'ENGINE': config('DATABASE_ENGINE'), ## coloque aqui a engine do banco que você vai utilizar ##
            'HOST': config('DATABASE_HOST'),
            'PORT': config('DATABASE_PORT'),
            'NAME': config('DATABASE_NAME'),
            'USER': config('DATABASE_USER'),
            'PASSWORD': config('DATABASE_PASSWORD')
        }}
    }}

## CODE IF YOU WILL USE REDIS TO CACHE
if config('REDIS_URL',default=None) != None:
    CACHES = {{
        "default": {{
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": config('REDIS_URL'),
            "OPTIONS": {{
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }}
        }}
    }}

try:
    STATICFILES_DIRS += [
        os.path.join(BASE_DIR,"static"),
    ]
except NameError as err:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR,"static"),
    ]

if DEBUG:
    def custom_show_toolbar(request):
        return True  # Always show toolbar, for example purposes only.

    INSTALLED_APPS += [
        "debug_toolbar",
        "autofixture",
    ]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    DEBUG_TOOLBAR_CONFIG = {{
        'SHOW_TOOLBAR_CALLBACK': '{PROJECT_NAME}.ddsettings.custom_show_toolbar',
    }}
    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.logging.LoggingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
    ]
    ROOT_URLCONF = "{PROJECT_NAME}.ddurls"
'''
######################################################################
                    ## MANAGE FILE ##
######################################################################
MANAGE='''#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{PROJECT_NAME}.{SETTINGS_FILE_NAME}")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
'''
######################################################################
                    ## PACKAGE.JSON FILE ##
######################################################################
PACKAGEJSON='''{  
  "name": "django-docker",
  "description": "Package.json for development front utilities of django-docker",
  "version": "4.0.0-beta",
  "main": "index.js",
  "author": "Ronnasayd de Sousa Machado",
  "license": "MIT",
  "homepage": "https://github.com/Ronnasayd/django-docker",
  "keywords": [],
  "repository": {
    "type": "git",
    "url": "https://github.com/Ronnasayd/django-docker.git"
  },
  "bugs": {
    "url": "https://github.com/Ronnasayd/django-docker/issues"
  },

  "dependencies": {
    "browser-sync": "latest",
    "gulp": "latest",
    "gulp-autoprefixer": "latest",
    "gulp-cached": "latest",
    "gulp-clean-css": "latest",
    "gulp-concat": "latest",
    "gulp-imagemin": "latest",
    "gulp-purgecss": "latest",
    "gulp-rename": "latest",
    "gulp-sass": "latest",
    "gulp-sourcemaps": "latest",
    "gulp-uglify": "latest",
    "minimist": "latest",
    "node-sass": "latest",
    "gulp-sass-partials-imported":"latest",
    "jshint":"latest",
    "gulp-jshint":"latest"
  }
}
'''
######################################################################
                    ## DOCKERIGNORE FILE ##
######################################################################
DOCKERIGNORE = '''
*/node_modules*
*/gulpfile.js*
*/package.json*
'''
######################################################################
                    ## DDURLS FILE ##
######################################################################
DDURLS = '''
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    path('', include('{PROJECT_NAME}.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]
'''

PIPFILE='''[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[dev-packages]

[packages]
django = "*"
gunicorn = "*"
python-decouple = "*"
psycopg2-binary = "*"
django-debug-toolbar = "*"
pillow = "*"
django-autofixture = "*"

[requires]
python_version = "{PYTHON_VERSION}"
'''

PIPFILELOCK='''{
    "_meta": {
        "hash": {
            "sha256": "074672ef2e0bb2949dfa0511ad69acb3957c13c48d2994741891f6243a5039c0"
        },
        "pipfile-spec": 6,
        "requires": {
            "python_version": "3.6"
        },
        "sources": [
            {
                "name": "pypi",
                "url": "https://pypi.org/simple",
                "verify_ssl": true
            }
        ]
    },
    "default": {
        "django": {
            "hashes": [
                "sha256:6fcc3cbd55b16f9a01f37de8bcbe286e0ea22e87096557f1511051780338eaea",
                "sha256:bb407d0bb46395ca1241f829f5bd03f7e482f97f7d1936e26e98dacb201ed4ec"
            ],
            "index": "pypi",
            "version": "==2.2.1"
        },
        "django-autofixture": {
            "hashes": [
                "sha256:32588b80814cdff3a8aab7cf3859fc9330d38abe37a9cc16e53d24dd1b1fcd86"
            ],
            "index": "pypi",
            "version": "==0.12.1"
        },
        "django-debug-toolbar": {
            "hashes": [
                "sha256:89d75b60c65db363fb24688d977e5fbf0e73386c67acf562d278402a10fc3736",
                "sha256:c2b0134119a624f4ac9398b44f8e28a01c7686ac350a12a74793f3dd57a9eea0"
            ],
            "index": "pypi",
            "version": "==1.11"
        },
        "gunicorn": {
            "hashes": [
                "sha256:aa8e0b40b4157b36a5df5e599f45c9c76d6af43845ba3b3b0efe2c70473c2471",
                "sha256:fa2662097c66f920f53f70621c6c58ca4a3c4d3434205e608e121b5b3b71f4f3"
            ],
            "index": "pypi",
            "version": "==19.9.0"
        },
        "pillow": {
            "hashes": [
                "sha256:15c056bfa284c30a7f265a41ac4cbbc93bdbfc0dfe0613b9cb8a8581b51a9e55",
                "sha256:1a4e06ba4f74494ea0c58c24de2bb752818e9d504474ec95b0aa94f6b0a7e479",
                "sha256:1c3c707c76be43c9e99cb7e3d5f1bee1c8e5be8b8a2a5eeee665efbf8ddde91a",
                "sha256:1fd0b290203e3b0882d9605d807b03c0f47e3440f97824586c173eca0aadd99d",
                "sha256:24114e4a6e1870c5a24b1da8f60d0ba77a0b4027907860188ea82bd3508c80eb",
                "sha256:258d886a49b6b058cd7abb0ab4b2b85ce78669a857398e83e8b8e28b317b5abb",
                "sha256:33c79b6dd6bc7f65079ab9ca5bebffb5f5d1141c689c9c6a7855776d1b09b7e8",
                "sha256:367385fc797b2c31564c427430c7a8630db1a00bd040555dfc1d5c52e39fcd72",
                "sha256:3c1884ff078fb8bf5f63d7d86921838b82ed4a7d0c027add773c2f38b3168754",
                "sha256:44e5240e8f4f8861d748f2a58b3f04daadab5e22bfec896bf5434745f788f33f",
                "sha256:46aa988e15f3ea72dddd81afe3839437b755fffddb5e173886f11460be909dce",
                "sha256:74d90d499c9c736d52dd6d9b7221af5665b9c04f1767e35f5dd8694324bd4601",
                "sha256:809c0a2ce9032cbcd7b5313f71af4bdc5c8c771cb86eb7559afd954cab82ebb5",
                "sha256:85d1ef2cdafd5507c4221d201aaf62fc9276f8b0f71bd3933363e62a33abc734",
                "sha256:8c3889c7681af77ecfa4431cd42a2885d093ecb811e81fbe5e203abc07e0995b",
                "sha256:9218d81b9fca98d2c47d35d688a0cea0c42fd473159dfd5612dcb0483c63e40b",
                "sha256:9aa4f3827992288edd37c9df345783a69ef58bd20cc02e64b36e44bcd157bbf1",
                "sha256:9d80f44137a70b6f84c750d11019a3419f409c944526a95219bea0ac31f4dd91",
                "sha256:b7ebd36128a2fe93991293f997e44be9286503c7530ace6a55b938b20be288d8",
                "sha256:c4c78e2c71c257c136cdd43869fd3d5e34fc2162dc22e4a5406b0ebe86958239",
                "sha256:c6a842537f887be1fe115d8abb5daa9bc8cc124e455ff995830cc785624a97af",
                "sha256:cf0a2e040fdf5a6d95f4c286c6ef1df6b36c218b528c8a9158ec2452a804b9b8",
                "sha256:cfd28aad6fc61f7a5d4ee556a997dc6e5555d9381d1390c00ecaf984d57e4232",
                "sha256:dca5660e25932771460d4688ccbb515677caaf8595f3f3240ec16c117deff89a",
                "sha256:de7aedc85918c2f887886442e50f52c1b93545606317956d65f342bd81cb4fc3",
                "sha256:e6c0bbf8e277b74196e3140c35f9a1ae3eafd818f7f2d3a15819c49135d6c062"
            ],
            "index": "pypi",
            "version": "==6.0.0"
        },
        "psycopg2-binary": {
            "hashes": [
                "sha256:007ca0df127b1862fc010125bc4100b7a630efc6841047bd11afceadb4754611",
                "sha256:03c49e02adf0b4d68f422fdbd98f7a7c547beb27e99a75ed02298f85cb48406a",
                "sha256:0a1232cdd314e08848825edda06600455ad2a7adaa463ebfb12ece2d09f3370e",
                "sha256:131c80d0958c89273d9720b9adf9df1d7600bb3120e16019a7389ab15b079af5",
                "sha256:2de34cc3b775724623f86617d2601308083176a495f5b2efc2bbb0da154f483a",
                "sha256:2eddc31500f73544a2a54123d4c4b249c3c711d31e64deddb0890982ea37397a",
                "sha256:484f6c62bdc166ee0e5be3aa831120423bf399786d1f3b0304526c86180fbc0b",
                "sha256:4c2d9369ed40b4a44a8ccd6bc3a7db6272b8314812d2d1091f95c4c836d92e06",
                "sha256:70f570b5fa44413b9f30dbc053d17ef3ce6a4100147a10822f8662e58d473656",
                "sha256:7a2b5b095f3bd733aab101c89c0e1a3f0dfb4ebdc26f6374805c086ffe29d5b2",
                "sha256:804914a669186e2843c1f7fbe12b55aad1b36d40a28274abe6027deffad9433d",
                "sha256:8520c03172da18345d012949a53617a963e0191ccb3c666f23276d5326af27b5",
                "sha256:90da901fc33ea393fc644607e4a3916b509387e9339ec6ebc7bfded45b7a0ae9",
                "sha256:a582416ad123291a82c300d1d872bdc4136d69ad0b41d57dc5ca3df7ef8e3088",
                "sha256:ac8c5e20309f4989c296d62cac20ee456b69c41fd1bc03829e27de23b6fa9dd0",
                "sha256:b2cf82f55a619879f8557fdaae5cec7a294fac815e0087c4f67026fdf5259844",
                "sha256:b59d6f8cfca2983d8fdbe457bf95d2192f7b7efdb2b483bf5fa4e8981b04e8b2",
                "sha256:be08168197021d669b9964bd87628fa88f910b1be31e7010901070f2540c05fd",
                "sha256:be0f952f1c365061041bad16e27e224e29615d4eb1fb5b7e7760a1d3d12b90b6",
                "sha256:c1c9a33e46d7c12b9c96cf2d4349d783e3127163fd96254dcd44663cf0a1d438",
                "sha256:d18c89957ac57dd2a2724ecfe9a759912d776f96ecabba23acb9ecbf5c731035",
                "sha256:d7e7b0ff21f39433c50397e60bf0995d078802c591ca3b8d99857ea18a7496ee",
                "sha256:da0929b2bf0d1f365345e5eb940d8713c1d516312e010135b14402e2a3d2404d",
                "sha256:de24a4962e361c512d3e528ded6c7480eab24c655b8ca1f0b761d3b3650d2f07",
                "sha256:e45f93ff3f7dae2202248cf413a87aeb330821bf76998b3cf374eda2fc893dd7",
                "sha256:f046aeae1f7a845041b8661bb7a52449202b6c5d3fb59eb4724e7ca088811904",
                "sha256:f1dc2b7b2748084b890f5d05b65a47cd03188824890e9a60818721fd492249fb",
                "sha256:fcbe7cf3a786572b73d2cd5f34ed452a5f5fac47c9c9d1e0642c457a148f9f88"
            ],
            "index": "pypi",
            "version": "==2.8.2"
        },
        "python-decouple": {
            "hashes": [
                "sha256:1317df14b43efee4337a4aa02914bf004f010cd56d6c4bd894e6474ec8c4fe2d"
            ],
            "index": "pypi",
            "version": "==3.1"
        },
        "pytz": {
            "hashes": [
                "sha256:303879e36b721603cc54604edcac9d20401bdbe31e1e4fdee5b9f98d5d31dfda",
                "sha256:d747dd3d23d77ef44c6a3526e274af6efeb0a6f1afd5a69ba4d5be4098c8e141"
            ],
            "version": "==2019.1"
        },
        "sqlparse": {
            "hashes": [
                "sha256:40afe6b8d4b1117e7dff5504d7a8ce07d9a1b15aeeade8a2d10f130a834f8177",
                "sha256:7c3dca29c022744e95b547e867cee89f4fce4373f3549ccd8797d8eb52cdb873"
            ],
            "version": "==0.3.0"
        }
    },
    "develop": {}
}
'''
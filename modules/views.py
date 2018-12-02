#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        server web:{WEB_PORT};

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
          target: "http://web:{WEB_PORT}",
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
    .pipe(rename(function(file){{
            file.dirname = file.dirname.replace('{JS_FOLDERS}','{JSMIN_FOLDERS}');
            file.extname = ".min.js"
    }}))
    .pipe(sourcemaps.init())
    .pipe(uglify()).on('error',function(err){{
            console.log(err.message);
            console.log(err.cause);
            browserSync.notify(err.message, 3000); // Display error in the browser
            this.emit('end'); // Prevent gulp from catching the error and exiting the watch process
     }})
    .pipe(sourcemaps.write())
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
        .pipe(rename(function(file){{
            file.dirname = file.dirname.replace('{SCSS_FOLDERS}','{CSS_FOLDERS}');
        }}))
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
        .pipe(sourcemaps.write())
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
chmod +x modules/wait-for-it.sh
sed -i "s/\\r$//" {FOLDER_NAME}{RUNSERVER_SCRIPT_NAME}
sed -i "s/\\r$//" modules/wait-for-it.sh
sed -i "s/\\r$//" {FOLDER_NAME}gulpfile.js
sed -i "s/\\r$//" {FOLDER_NAME}gulp.sh
cp {FOLDER_NAME}{RUNSERVER_SCRIPT_NAME} ./{PROJECT_NAME}
cp modules/wait-for-it.sh ./{PROJECT_NAME}
cp {FOLDER_NAME}gulpfile.js ./{PROJECT_NAME}
cp {FOLDER_NAME}gulp.sh ./{PROJECT_NAME}
mkdir static/ media/ logs/
'''

MAKE_AMBIENT_DEVELOPMENT='''docker-compose -f {FOLDER_NAME}{PROJECT_NAME}_development.yml stop
docker-compose -f {FOLDER_NAME}{PROJECT_NAME}_production.yml stop
docker-compose -f {FOLDER_NAME}{PROJECT_NAME}_development.yml down
docker-compose -f {FOLDER_NAME}{PROJECT_NAME}_production.yml down
docker system prune --force
docker-compose -f {FOLDER_NAME}{PROJECT_NAME}_development.yml build
COMPOSE_HTTP_TIMEOUT=3600 docker-compose -f {FOLDER_NAME}{PROJECT_NAME}_development.yml up --remove-orphans --force-recreate'''


MAKE_AMBIENT_PRODUCTION='''docker-compose -f {FOLDER_NAME}{PROJECT_NAME}_production.yml stop
docker-compose -f {FOLDER_NAME}{PROJECT_NAME}_development.yml stop
docker-compose -f {FOLDER_NAME}{PROJECT_NAME}_production.yml down
docker-compose -f {FOLDER_NAME}{PROJECT_NAME}_development.yml down
docker system prune --force
docker-compose -f {FOLDER_NAME}{PROJECT_NAME}_production.yml build
docker-compose -f {FOLDER_NAME}{PROJECT_NAME}_production.yml up  -d --remove-orphans --force-recreate'''

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
#########################################################################
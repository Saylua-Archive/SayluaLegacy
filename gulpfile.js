var gulp = require('gulp');
var gutil = require('gulp-util');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var sourcemaps = require('gulp-sourcemaps');
var sass = require('gulp-sass');
var cleanCSS = require('gulp-clean-css');

var glob = require('glob');

var _webpack = require('webpack');
var webpack = require('webpack-stream');
var webpackConfig = require('./webpack.config.js');

var paths = {
  js: 'saylua/static/source/js/*/',
  es6: './saylua/static/source/es6/*/',
  sass: 'saylua/static/source/css/**/*.scss'
};

var dests = {
  scripts: 'saylua/static/js/',
  sass: 'saylua/static/css/'
};

gulp.task('build-sass', function () {
  gulp.src(paths.sass)
    .pipe(sass.sync().on('error', sass.logError))
    .pipe(concat('styles.min.css'))
    .pipe(sourcemaps.init())
    .pipe(cleanCSS())
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(dests.sass));
});

gulp.task('build-js', [], function() {
  // Minify and copy all JavaScript (except vendor scripts)
  // with sourcemaps all the way down
  var jsFolder = glob.sync(paths.js);

  jsFolder.forEach(function(folder) {
    var pkgName = folder.match(/.+\/(.+)\/$/)[1];

    var out = gulp.src([folder + '**/*.js']);

    if (process.env.NODE_ENV === "dev") {
      out.pipe(concat(pkgName + '.min.js'))
        .pipe(gulp.dest(dests.scripts));
    } else {
      out.pipe(sourcemaps.init())
        .pipe(uglify())
        .pipe(concat(pkgName + '.min.js'))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(dests.scripts));
    }
  });
});

gulp.task('build-es6', [], function() {
  // Look for Main.jsx within <FolderName>, compile to <FolderName>.min.js
  var esFolders = glob.sync(paths.es6);

  esFolders.forEach(function(folder) {
    var pkgName = folder.match(/.+\/(.+)\/$/)[1];
    var pkgPath = folder + "Main.jsx";

    // Set additional dev options
    if (process.env.NODE_ENV === "dev") {
      //webpackConfig['devtool'] = 'inline-source-map';
    } else {
      webpackConfig['plugins'] = [
        new _webpack.optimize.DedupePlugin(),
        new _webpack.optimize.UglifyJsPlugin({
          "compress": {
            "warnings": false
          }
        })
      ];
    }

    gulp.src(pkgPath)
      .pipe(webpack(webpackConfig)).on('error', gutil.log)
      .pipe(concat(pkgName + '.min.js'))
      .pipe(gulp.dest(dests.scripts));
  });
});

// Build everything. Check under every stone. Leave no survivors.
gulp.task('build', ['build-js', 'build-es6', 'build-sass']);

// Rerun the task when a file changes
gulp.task('watch', function() {
  process.env.NODE_ENV = "dev";

  gulp.watch(paths.js, ['build-js']);
  gulp.watch(paths.js + "**/*.*", ['build-js']);

  gulp.watch(paths.es6, ['build-es6']);
  gulp.watch(paths.es6 + "**/*.*", ['build-es6']);

  gulp.watch(paths.sass, ['build-sass']);
  gulp.watch(paths.sass + "**/*.*", ['build-sass']);
});

// The default task (called when you run `gulp` from cli)
gulp.task('default', ['watch', 'build']);

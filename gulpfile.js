var gulp = require('gulp');
var sass = require('gulp-sass');
var gutil = require('gulp-util');
var watch = require('gulp-watch');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var cleanCSS = require('gulp-clean-css');
var sourcemaps = require('gulp-sourcemaps');

var glob = require('glob');
var path = require('path');
var stream = require('stream');

var _webpack = require('webpack');
var webpack = require('webpack-stream');
var webpackConfig = require('./webpack.config.js');

var paths = {
  js: 'saylua/**/static-source/js',
  es6: 'saylua/**/static-source/es6',
  sass: 'saylua/**/static-source/scss'
};

var dests = {
  scripts: 'static/js',           // Relative to script location
  sass: 'saylua/static/css/'      // All sass styles compile to style.min.css at the application root.
};

gulp.task('lint', function () {
  console.log("Go away!");
});

gulp.task('build-sass', function () {
  var filesGlob = paths.sass + "/**/*.scss";

  gulp.src(filesGlob)
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
  var pkgGlob = paths.js + "/*";
  var folders = glob.sync(pkgGlob);

  folders.forEach(function(folder) {
    var pkgName = folder.split("/").splice(-1)[0];
    var pkg = gulp.src(folder + '**/*.js', { base: process.cwd() });

    // Filter deprecated / hidden packages
    if (pkgName.startsWith("_")) {
      return;
    }

    // Find our module path
    var modulePath = folder.split('/static-source/')[0]

    // Generate output path
    var pkgPath = path.join(modulePath, dests.scripts);

    if (process.env.NODE_ENV === "dev") {
      pkg.pipe(concat(pkgName + '.min.js'))
        .pipe(gulp.dest(pkgPath));
    } else {
      pkg.pipe(uglify())
        .pipe(concat(pkgName + '.min.js'))
        .pipe(gulp.dest(pkgPath));
    }
  });
});

gulp.task('build-es', ['build-es6']);
gulp.task('build-es6', [], function() {
  // Look for Main.jsx within <FolderName>, compile to <FolderName>.min.js
  var pkgGlob = paths.es6 + "/**/Main.jsx";
  var packages = glob.sync(pkgGlob);

  // Compile hashmap from paths
  var hashmap = {};

  packages.forEach(function(pkg) {
    // First, we grab the name of the package
    var pkgName = pkg.split("/").splice(-2)[0];

    // Then, we separate the module path from the absolute path.
    var modulePath = pkg.split("/static-source/")[0];

    // Then, we combine the two to obtain a static path location.
    var pkgPath = path.join(modulePath, dests.scripts, pkgName);

    // Filter deprecated / hidden packages
    if (pkgName.indexOf("_") == -1) {
      hashmap[pkgPath] = "./" + pkg;
    }
  });

  webpackConfig['entry'] = hashmap;

  // Always display progress.
  webpackConfig['plugins'] = [
    new _webpack.ProgressPlugin(function (percentage, message) {
      var percent = Math.round(percentage * 100);
      var ending = (percent == 100) ? "\n" : "";

      process.stderr.clearLine();
      process.stderr.cursorTo(0);
      process.stderr.write("\033[33m[Building] ... " + percent + '% ' + message + "\033[0m" + ending);
    })
  ];

  // Set additional dev options
  if (process.env.NODE_ENV === "dev") {
    webpackConfig['devtool'] = 'inline-source-map';
  } else {
    webpackConfig['plugins'].push(new _webpack.optimize.DedupePlugin());
    webpackConfig['plugins'].push(
      new _webpack.optimize.UglifyJsPlugin({
        "compress": {
          "warnings": false
        }
      })
    );
  }

  return gulp.src("")
    .pipe(webpack(webpackConfig)).on('error', gutil.log)
    .pipe(gulp.dest("./"));
});

// Build everything. Check under every stone. Leave no survivors.
gulp.task('build', ['build-js', 'build-es6', 'build-sass']);

// Rerun the task when a file changes
gulp.task('watch', function() {
  process.env.NODE_ENV = "dev";

  var reportChange = function(vinyl) {
    var event = vinyl.event;
    event = event[0].toUpperCase() + event.slice(1);

    process.stdout.write("\033[33m[Watching]\033[0m " + event + ": " + vinyl.path + "\n");
  };

  watch([paths.js + "/**/*"], { 'usePolling': true }, function(vinyl) {
    reportChange(vinyl);
    gulp.start('build-js');
  });

  watch([paths.es6 + "/**/*"], { 'usePolling': true }, function(vinyl) {
    reportChange(vinyl);
    gulp.start('build-es6');
  });

  watch([paths.sass + "/**/*"], { 'usePolling': true }, function(vinyl) {
    reportChange(vinyl);
    gulp.start('build-sass');
  });

  var _paths = Object.keys(paths).map(function(key) { return paths[key]; });
  process.stdout.write("\n" + "Watching:" + "\n========================\n" + _paths.join("\n") + "\n\n");

  // Purely for aesthetic reasons.
  // Prevents the "Finished" line from printing.
  return new stream.Stream();
});

// The default task (called when you run `gulp` from cli)
gulp.task('default', ['build']);

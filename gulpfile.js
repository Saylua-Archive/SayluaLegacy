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

var webpack = require('webpack');
var webpackConfig = require('./webpack.config.js');

var tempConfig = require('./temporary.config.js');
var paths = tempConfig.paths;
var dests = tempConfig.dests;

gulp.task('lint', function () {
  console.log("Go away!");
});


gulp.task('build-sass', function () {
  // Compile our initial, root level styles
  var rootGlob = "saylua/static-source/scss/**/*.scss";

  gulp.src(rootGlob)
    .pipe(sass().on('error', sass.logError))
    .pipe(concat('styles.min.css'))
    .pipe(sourcemaps.init())
    .pipe(cleanCSS())
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(dests.sass));

  // Compile our module SCSS into separate payloads.
  var moduleGlob = "saylua/modules/*/"
  var moduleFolders = glob.sync(moduleGlob);

  moduleFolders.forEach(function(folder) {
    var moduleFilesGlob = folder + "/static-source/scss/**/*.scss";
    var moduleFiles = glob.sync(moduleFilesGlob);

    var packageName = folder.split("/").splice(-2)[0];

    var outputName = packageName + '.min.css';
    var outputPath = "saylua/modules/" + packageName + "/static/css/";

    gulp.src(moduleFilesGlob)
      .pipe(sass({
        'includePaths': "saylua/static-source/scss/"
      }).on('error', sass.logError))
      .pipe(concat(outputName))
      .pipe(sourcemaps.init())
      .pipe(cleanCSS())
      .pipe(sourcemaps.write())
      .pipe(gulp.dest(outputPath));
  });
});


gulp.task('build-js', ['build-es']);
gulp.task('build-es6', ['build-es']);
gulp.task('build-es', [], function() {
  // Create a local copy of the config.
  var config = webpackConfig;

  // Set additional dev options
  if (process.env.NODE_ENV === "dev") {
    config['plugins'].push(
      new webpack.DefinePlugin({
        'process.env.NODE_ENV': JSON.stringify('development')
      })
    );
    config['devtool'] = 'inline-source-map';
    config.watch = true;
  } else {
    config['plugins'].push(
      new webpack.DefinePlugin({
        'process.env.NODE_ENV': JSON.stringify('production')
      })
    );

    // Minify output
    config['plugins'].push(
      new webpack.optimize.UglifyJsPlugin({
        "compress": {
          "warnings": false
        }
      })
    );
  }

  // Pre-configure compiler, stream.
  var compiler = webpack(webpackConfig);
  var _stream = new stream.Stream();

  // Build info config
  var statsConfig = {
    "assetsSort": "name",
    "colors": true,
    "chunks": false,
    "chunkModules": false
  };

  // Determine whether or not to 'watch'
  if (process.env.NODE_ENV === "dev") {
    var watch = compiler.watch({}, (err, stats) => {
      gutil.beep();
      gutil.log(stats.toString(statsConfig));
    });
  } else {
    compiler.run((err, stats) => {
      if (err || stats.hasErrors()) {
        gutil.log(err);
      } else {
        gutil.log(stats.toString(statsConfig));
      }
    });

    return _stream;
  }
});


// Build everything. Check under every stone. Leave no survivors.
gulp.task('build', ['build-es6', 'build-sass']);


// Rerun the task when a file changes
gulp.task('watch', function() {
  process.env.NODE_ENV = "dev";

  // Special treatment for sass files.
  var reportChange = function(vinyl) {
    var event = vinyl.event;
    event = event[0].toUpperCase() + event.slice(1);

    process.stdout.write("\x1b[33m[Watching]\x1b[0m " + event + ": " + vinyl.path + "\n");
  };

  watch([paths.sass + "/**/*"], { 'usePolling': true }, function(vinyl) {
    reportChange(vinyl);
    gulp.start('build-sass');
  });


  // Watch is automatically determined by using the node-env in `build-es`, so we can continue as usual.
  var res = gulp.start('build-es');


  // Print the paths we're watching, because we're nice.
  var _paths = Object.keys(paths).map(function(key) { return paths[key]; });
  process.stdout.write("\n" + "Watching:" + "\n========================\n" + _paths.join("\n") + "\n\n");


  // Purely for aesthetic reasons.
  // Prevents the "Finished" line from printing.
  return new stream.Stream();
});


// The default task (called when you run `gulp` from cli)
gulp.task('default', ['build']);


module.exports.dests = dests;
module.exports.paths = paths;

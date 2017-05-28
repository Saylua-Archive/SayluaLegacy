import gulp from 'gulp';
import sass from 'gulp-sass';
import gutil from 'gulp-util';
import watch from 'gulp-watch';
import concat from 'gulp-concat';
import cleanCSS from 'gulp-clean-css';
import sourcemaps from 'gulp-sourcemaps';
import autoprefixer from 'gulp-autoprefixer';

import glob from 'glob';
import stream from 'stream';
import webpack from 'webpack';
import cloneDeep from 'lodash.clonedeep';

import webpackConfig from './webpack.config.js';
import tempConfig from './temporary.config.js';

const paths = tempConfig.paths;
const dests = tempConfig.dests;


gulp.task('build-css', ['build-sass']);
gulp.task('build-sass', () => {
  // Compile our initial, root level styles
  let rootGlob = "saylua/static-source/scss/**/*.scss";

  gulp.src(rootGlob)
    .pipe(sass().on('error', sass.logError))
    .pipe(concat('styles.min.css'))
    .pipe(sourcemaps.init())
    .pipe(autoprefixer())
    .pipe(cleanCSS())
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(dests.sass));

  // Compile our module SCSS into separate payloads.
  let moduleGlob = "saylua/modules/*/";
  let moduleFolders = glob.sync(moduleGlob);

  moduleFolders.map((folder) => {
    let moduleFilesGlob = folder + "/static-source/scss/**/*.scss";
    let moduleFiles = glob.sync(moduleFilesGlob);

    let packageName = folder.split("/").splice(-2)[0];

    let outputName = packageName + '.min.css';
    let outputPath = "saylua/modules/" + packageName + "/static/css/";

    gulp.src(moduleFilesGlob)
      .pipe(sass({
        'includePaths': "saylua/static-source/scss/"
      })
      .on('error', sass.logError))
      .pipe(concat(outputName))
      .pipe(sourcemaps.init())
      .pipe(autoprefixer())
      .pipe(cleanCSS())
      .pipe(sourcemaps.write())
      .pipe(gulp.dest(outputPath));
  });
});


gulp.task('build-js', ['build-es']);
gulp.task('build-es6', ['build-es']);
gulp.task('build-es', (callback) => {
  // Create a local copy of the config.
  let config = cloneDeep(webpackConfig);

  process.env.NODE_ENV = "production";

  // Set our webpack environs
  config['plugins'].push(
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV)
    })
  );

  // Minify output in production.
  config['plugins'].push(
    new webpack.optimize.UglifyJsPlugin({
      "compress": {
        "warnings": false
      }
    })
  );

  // Pre-configure compiler, stream.
  let compiler = webpack(config);
  let _stream = new stream.Stream();

  // Build info config
  let statsConfig = {
    "assetsSort": "name",
    "colors": true,
    "chunks": false,
    "chunkModules": false
  };

  compiler.run((err, stats) => {
    if (err || stats.hasErrors()) {
      gutil.log(err);
      _stream.emit('end');
    } else {
      gutil.log(stats.toString(statsConfig));
      callback();
    }
  });

  return _stream;
});

gulp.task('watch-js', ['watch-es']);
gulp.task('watch-es6', ['watch-es']);
gulp.task('watch-es', (callback) => {
  // Create a local copy of the config.
  let config = cloneDeep(webpackConfig);

  process.env.NODE_ENV = "development";

  // Set our webpack environs
  config['plugins'].push(
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV)
    })
  );

  // Set additional dev options
  config['devtool'] = 'inline-source-map';
  config.watch = true;

  console.log("PLUGINGSINGSINS");
  console.log(config['plugins']);

  // Pre-configure compiler.
  let compiler = webpack(config);

  // Build info config
  let statsConfig = {
    "assetsSort": "name",
    "colors": true,
    "chunks": false,
    "chunkModules": false
  };

  compiler.watch({}, (err, stats) => {
    statsConfig.assets = false;
    gutil.log(stats.toString(statsConfig));
  });
});


// Build everything. Check under every stone. Leave no survivors.
gulp.task('build', ['build-es', 'build-sass']);


// Rerun the task when a file changes
gulp.task('watch', ['build-sass', 'build-es'], () => {
  // Special treatment for sass files.
  const reportChange = (vinyl) => {
    let event = vinyl.event;
    event = event[0].toUpperCase() + event.slice(1);

    process.stdout.write("\x1b[33m[Watching]\x1b[0m " + event + ": " + vinyl.path + "\n");
  };

  watch([paths.sass + "/**/*"], { 'usePolling': true }, (vinyl) => {
    reportChange(vinyl);
    gulp.start('build-sass');
  });

  // We prefer to use Webpack's built in 'watch' for speed reasons, but still want to report
  // file changes.
  watch([paths.es6 + "/**/*"], { 'usePolling': true }, (vinyl) => {
    reportChange(vinyl);
  });
  gulp.start('watch-es');


  // Print the paths we're watching, because we're nice.
  let _paths = Object.keys(paths).map(key => paths[key]);
  process.stdout.write(`\nWatching:`);
  process.stdout.write(`\n========================\n`);
  process.stdout.write(`${ _paths.join('\n') }\n\n`);


  // Purely for aesthetic reasons.
  // Prevents the "Finished" line from printing.
  return new stream.Stream();
});


// The default task (called when you run `gulp` from cli)
gulp.task('default', ['build']);

var gulp = require('gulp');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var sourcemaps = require('gulp-sourcemaps');
var sass = require('gulp-sass');
var cleanCSS = require('gulp-clean-css');
var glob = require('glob');

var paths = {
  scripts: 'saylua/static/source/js/*/',
  sass: 'saylua/static/source/css/**/*.scss'
};

var dests = {
  scripts: 'saylua/static/js/',
  sass: 'saylua/static/css/'
};

gulp.task('sass', function () {
  gulp.src(paths.sass)
    .pipe(sass.sync().on('error', sass.logError))
    .pipe(concat('styles.min.css'))
    .pipe(sourcemaps.init())
    .pipe(cleanCSS())
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(dests.sass));
});

gulp.task('scripts', [], function() {
  // Minify and copy all JavaScript (except vendor scripts)
  // with sourcemaps all the way down
  var jsFolder = glob.sync(paths.scripts);

  jsFolder.forEach(function(folder) {
    var pkgName = folder.match(/.+\/(.+)\/$/)[1];

    gulp.src([folder + '**/*.js'])
            .pipe(sourcemaps.init())
              .pipe(uglify())
              .pipe(concat(pkgName + '.min.js'))
            .pipe(sourcemaps.write())
            .pipe(gulp.dest(dests.scripts));
  });
});

// Rerun the task when a file changes
gulp.task('watch', function() {
  gulp.watch(paths.scripts, ['scripts']);
  gulp.watch(paths.scripts + "**/*.*", ['scripts']);

  gulp.watch(paths.sass, ['sass']);
  gulp.watch(paths.sass + "**/*.*", ['sass']);
});

// The default task (called when you run `gulp` from cli)
gulp.task('default', ['watch', 'scripts', 'sass']);

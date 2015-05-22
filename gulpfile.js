var gulp = require('gulp'),
    source = require('vinyl-source-stream'),
    browserify = require('browserify'),
    reactify = require('reactify'),
    watchify = require('watchify'),
    less = require('gulp-less-sourcemap');

gulp.task('less', function () {
  return gulp.src('./src/less/main.less')
    .pipe(less({
        sourceMap: {sourceMapFileInline: true}
    }))
    .pipe(gulp.dest('./build/css'));
});

gulp.task('lesswatch', function () {
  gulp.watch(['./src/less/**/*.less'], ['less']);
});

gulp.task('browserify', function () {

  var bundler = browserify({
    entries: ['./src/js/main.js'],
    transform: [reactify],
    debug: true
  });

  return bundler.bundle()
    .pipe(source('./bundle.js'))
    .pipe(gulp.dest('./build/js/'));

});

gulp.task('watchify', function () {

    var watcher = watchify(browserify({
        entries: ['./src/js/main.js'], // Only need initial file, browserify finds the deps
        transform: [reactify], // We want to convert JSX to normal javascript
        debug: true,
        cache: {},
        packageCache: {},
        fullPaths: true
    }));

    watcher.on('update', function () {
        watcher.bundle()
            .pipe(source('./bundle.js'))
            .pipe(gulp.dest('./build/js/'));
    });

    watcher.bundle()
        .pipe(source('./bundle.js'))
        .pipe(gulp.dest('./build/js/'));

});

gulp.task('develop', ['watchify', 'lesswatch']);

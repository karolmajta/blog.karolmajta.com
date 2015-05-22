var _ = require('lodash'),
    minimist = require('minimist'),
    gulp = require('gulp'),
    source = require('vinyl-source-stream'),
    browserify = require('browserify'),
    watchify = require('watchify'),
    less = require('gulp-less-sourcemap');
var argv = minimist(process.argv.slice(2));

var REQUIRED_FLAGS = ['js-dir', 'css-dir'];
if (!_.all(_.map(REQUIRED_FLAGS, function (f) { return argv[f]; }))) {
  console.log("USAGE: gulp develop --js-dir=<js dir> --css-dir=<css dir>")
  process.exit(1);
}
var JS_DIR = argv['js-dir']
var CSS_DIR = argv['css-dir']

gulp.task('less', function () {
  return gulp.src('./src/less/main.less')
    .pipe(less({
        sourceMap: {sourceMapFileInline: true}
    }))
    .pipe(gulp.dest(CSS_DIR));
});

gulp.task('lesswatch', function () {
  gulp.watch(['./src/less/**/*.less'], ['less']);
});

gulp.task('browserify', function () {

  var bundler = browserify({
    entries: ['./src/js/main.js'],
    debug: true
  });

  return bundler.bundle()
    .pipe(source('./bundle.js'))
    .pipe(gulp.dest(JS_DIR));

});

gulp.task('watchify', function () {

    var watcher = watchify(browserify({
        entries: ['./src/js/main.js'],
        debug: true,
        cache: {},
        packageCache: {},
        fullPaths: true
    }));

    watcher.on('update', function () {
        watcher.bundle()
            .pipe(source('./bundle.js'))
            .pipe(gulp.dest(JS_DIR));
    });

    watcher.bundle()
        .pipe(source('./bundle.js'))
        .pipe(gulp.dest(JS_DIR));

});

gulp.task('develop', ['watchify', 'lesswatch']);

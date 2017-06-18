var gulp        = require('gulp');
var browserSync = require('browser-sync').create();
var sass        = require('gulp-sass');

// Static Server + watching scss/html files
gulp.task('serve', ['sass'], function() {

    browserSync.init({
        server: "./"
    });

    gulp.watch("public/sass/*.scss", ['sass']);
    gulp.watch("views/*.html").on('change', browserSync.reload);
});

// Compile sass into CSS & auto-inject into browsers
gulp.task('sass', function() {
    return gulp.src("public/sass/*.scss")
        .pipe(sass({outputStyle: 'compressed'}))
        .pipe(gulp.dest("public/css"))
        .pipe(browserSync.stream());
});

gulp.task('default', ['serve']);
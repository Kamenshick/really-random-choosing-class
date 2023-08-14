countStudents = 1;
(function($) {
    var $wrap = $('#stud');
    $wrap.on('blur', 'input', function($e) {
       // console.log($(this).parent(), $e.target);
        countStudents++;
        $(this).after(`<input type="text" value="" class="name-input" name="${'i-'+countStudents}">`);
        $('.count-stud').val(countStudents);
    });
})(jQuery);
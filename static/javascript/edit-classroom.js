(function($) {

    $("#classroom-name").change(function(e) {
        var value = $('#classroom-name').val();
        var students = value.split("|");
        $('#classroom').empty();
        var lenStudents = students.length;
        $('#count-stud').val(`${lenStudents}`);
        $('#class-id').val(`${$('#classroom-name option:selected').data("value")}`)
        students.forEach(function(item, i, arr) {
            $('#classroom').append(`<input type="text" value="${item}" class="name-input" name="${'i-'+i}"></input>`);
          });
          
        $('#classroom').append(`<div id="add-students">Добавить студента</div>`);
    });
    
    var $wrap = $('#classroom');
    $wrap.on('click', '#add-students', function($e) {
        countStudents = $('#count-stud').val()
        $(this).before(`<input type="text" value="" class="name-input" name="${'i-'+countStudents}">`);
        countStudents++;
        $('.count-stud').val(`${countStudents}`);
        });

})(jQuery);


$("#classroom-name").change(function(e) {
    var value = $('#classroom-name').val();
    var students = value.split("|")
    $('#classroom').empty()

    //$('#classroom').attr("data-value", students.length )
    $('#count-stud').val(`${students.length}`)
    //$('.f-input').val('changed Value');

    students.forEach(function(item, i, arr) {
        $('#classroom').append(`<p>${item} <input type="checkbox" name="${'s-'+i}" class="check-box" value="${item}" checked></p>`);
      });
});

$(function () {

    /* Functions */

    var loadForm = function (){
        var btn = $(this);
        $.ajax({
            url: btn.attr('data-url'),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-operation").modal().modal('open');
            },
            success: function (data) {
                $("#modal-operation").html(data.html_form);
                $('select').formSelect();
          }
        });
    };

    var saveForm = function (e) {
        e.preventDefault();
        e.stopImmediatePropagation();

        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#operations-table tbody").html(data.html_operations_list);  // <-- Replace the table body
                    $("#modal-operation").modal('close');  // <-- Close the modal
                }
                else {
                    $("#modal-operation .modal-content").html(data.html_form);
                    $('select').formSelect();
                }
            }
        });
        return false;
    };

    /* Bindings */

    // Create budget
    $(".js-operation-create").click(loadForm);
    $("#modal-operation").on("submit", ".js-operation-create-form", saveForm);

    // Update budget
    $("#operations-table").on("click", ".js-operation-update", loadForm);
    $("#modal-operation").on("submit", ".js-operation-update-form", saveForm);

    //Delete budget
    $("#operations-table").on("click", ".js-operation-delete", loadForm);
    $("#modal-operation").on("submit", ".js-operation-delete-form", saveForm);

});
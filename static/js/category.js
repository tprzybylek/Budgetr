$(function () {

    /* Functions */

    var loadForm = function (){
        var btn = $(this);
        $.ajax({
            url: btn.attr('data-url'),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-category").modal().modal('open');
            },
            success: function (data) {
                $("#modal-category").html(data.html_form);
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
                    $("#categories-list ul").html(data.html_categories_list);  // <-- Replace the table body
                    $("#modal-category").modal('close');  // <-- Close the modal
                }
                else {
                    $("#modal-category .modal-content").html(data.html_form);
                    $('select').formSelect();
                }
            }
        });
        return false;
    };

    /* Bindings */

    // Create budget
    $(".js-category-create").click(loadForm);
    $("#modal-category").on("submit", ".js-category-create-form", saveForm);

    // Update budget
    $("#categories-list").on("click", ".js-category-update", loadForm);
    $("#modal-category").on("submit", ".js-category-update-form", saveForm);

    //Delete budget
    $("#categories-list").on("click", ".js-category-delete", loadForm);
    $("#modal-category").on("submit", ".js-category-delete-form", saveForm);

});
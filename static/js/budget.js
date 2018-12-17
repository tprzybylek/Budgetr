$(function () {

    /* Functions */

    var loadForm = function (){
        var btn = $(this);


        $.ajax({
            url: btn.attr('data-url'),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal_add_budget").modal().modal('open');
            },
            success: function (data) {
                $("#modal_add_budget").html(data.html_form);
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
                    $("#budgets-table tbody").html(data.html_budgets_list);  // <-- Replace the table body
                    $("#modal_add_budget").modal('close');  // <-- Close the modal
                }
                else {
                    $("#modal_add_budget .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };

    /* Bindings */

    // Create budget
    $(".js-add-budget").click(loadForm);
    $("#modal_add_budget").on("submit", ".js-budget-create-form", saveForm);

    // Update budget
    $("#budgets-table").on("click", ".js-update-budget", loadForm);
    $("#modal_add_budget").on("submit", ".js-budget-update-form", saveForm);

    //Delete budget
    $("#budgets-table").on("click", ".js-delete-budget", loadForm);
    $("#modal_add_budget").on("submit", ".js-budget-delete-form", saveForm);

});
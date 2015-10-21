// generate.js
// code for the poetry generation form
console.log('loaded generate.js');
(function () {
    var template_select = document.querySelector('#templates');
    var template_textarea = document.querySelector('textarea');
    var form = document.querySelector('form');
    var preselected_template_option = template_select.selectedOptions[0];

    var template_selected = function (e) {
        var option = e.explicitOriginalTarget;
        template_textarea.innerHTML = option.dataset.content;
    };

    var submit_generation = function (e) {
        e.preventDefault();
        var form_data = new FormData(form);
        var request = new XMLHttpRequest();

        request.open("POST", "/generate");
        request.send(form_data);

        return false;
    };

    template_select.addEventListener('change', template_selected);
    form.addEventListener('submit', submit_generation, true);

    template_textarea.innerHTML = preselected_template_option.dataset.content;
})();

// generate.js
// code for the poetry generation form
console.log('loaded generate.js');

if (!CodeMirror) {
    throw "Missing requirement CodeMirror";
}

(function () {
    // grumph
    var qs = document.querySelector.bind(document);

    // TODO this is a stupid hack.
    JSON.pretty_print = function (json_string) {
        return this.stringify(this.parse(json_string), undefined, 2);
    };

    // events
    var template_selected = function (state, e) {
        var option = e.explicitOriginalTarget;
        state.template_editor.setValue(JSON.pretty_print(option.dataset.content));
    };

    var successful_generation = function (state, e) {
        var lines = JSON.parse(e.target.response).result;

        var poem_container = document.createElement('div');
        poem_container.className = 'poem_container';

        var pre = document.createElement('pre');
        pre.className = 'poem';
        pre.innerHTML = lines.join("\n");

        var poem_controls = document.createElement('div');
        poem_controls.className = 'poem_controls';

        var close_button = document.createElement('button');
        close_button.innerHTML = 'X';
        close_button.addEventListener('click', function(e) {e.target.container.remove();});
        close_button.container = poem_container;
        poem_controls.appendChild(close_button);

        poem_container.appendChild(poem_controls);
        poem_container.appendChild(pre);

        var existing_poems = output.querySelectorAll('.poem_container');

        if (existing_poems.length == 0) {
            output.appendChild(poem_container);
        }
        else {
            output.insertBefore(poem_container, existing_poems[0]);
        }
    };

    var submit_generation = function (state, e) {
        e.preventDefault();

        var form_data = new FormData(state.form);
        var request = new XMLHttpRequest();

        request.open("POST", "/generate");
        request.send(form_data);
        request.addEventListener('load', successful_generation.bind(null, state));
    };

    // init
    var state = {
        template_select: qs('#templates'),
        form: qs('form'),
        output: qs('#output'),
        preselected_template_option: qs('#templates').selectedOptions[0],
        template_editor: CodeMirror.fromTextArea(qs('textarea'), {mode:'javascript'})
    };

    state.template_select.addEventListener('change', template_selected.bind(null, state));
    state.form.addEventListener('submit', submit_generation.bind(null, state), true);
    state.template_editor.setValue(JSON.pretty_print(state.preselected_template_option.dataset.content));
})();

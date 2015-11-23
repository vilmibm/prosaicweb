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
        var poem = JSON.parse(e.target.response);
        var lines = poem.lines;
        var sources = poem.used_sources;

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

        var sources_list = document.createElement('sub');
        sources_list.innerHTML = 'sources: ';
        sources_list.innerHTML += sources.join(', ');

        poem_container.appendChild(poem_controls);
        poem_container.appendChild(pre);
        poem_container.appendChild(sources_list);

        var existing_poems = state.output.querySelectorAll('.poem_container');

        if (existing_poems.length == 0) {
            state.output.appendChild(poem_container);
        }
        else {
            state.output.insertBefore(poem_container, existing_poems[0]);
        }
    };

    var submit_generation = function (state, e) {
        e.preventDefault();

        var form_data = new FormData(state.generate_form);
        var request = new XMLHttpRequest();

        request.open("POST", "/generate");
        request.send(form_data);
        request.addEventListener('load', successful_generation.bind(null, state));
    };

    var upload_file = function (state, e) {
        e.preventDefault();

        var form_data = new FormData(state.upload_form);
        var request = new XMLHttpRequest();

        request.open("POST", "/upload");
        request.send(form_data);
        request.addEventListener('load', successful_upload.bind(null, state));

        state.upload_form.lock();
    };

    var successful_upload = function (state, e) {
        var file_name = JSON.parse(e.target.response).name;
        console.log(file_name);

        var new_source = document.createElement('option');
        new_source.textContent = file_name;
        state.sources.appendChild(new_source);
        state.upload_form.clear();
        state.upload_form.unlock();
    };

    // init
    var state = {
        template_select: qs('#templates'),
        generate_form: qs('#generate'),
        output: qs('#output'),
        preselected_template_option: qs('#templates').selectedOptions[0],
        template_editor: CodeMirror.fromTextArea(qs('textarea'), {mode:'javascript'}),
        upload_form: qs('#upload'),
        sources: qs("#sources")
    };

    NodeList.prototype.forEach = Array.prototype.forEach;
    state.upload_form.lock = function () {
        this.querySelectorAll('input').forEach(function (el) {
            el.setAttribute('disabled', 'true');
        });
    };
    state.upload_form.unlock = function () {
        this.querySelectorAll('input').forEach(function (el) {
            el.removeAttribute('disabled');
        });
    };
    state.upload_form.clear = function () {
        this.querySelector("input[type=text]").value = "";
        this.querySelector("input[type=file]").value = "";
    };

    state.template_select.addEventListener('change', template_selected.bind(null, state));
    state.generate_form.addEventListener('submit', submit_generation.bind(null, state), true);
    state.template_editor.setValue(JSON.pretty_print(state.preselected_template_option.dataset.content));
    state.upload_form.addEventListener('submit', upload_file.bind(null, state));
})();

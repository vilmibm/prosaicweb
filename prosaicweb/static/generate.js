// generate.js
// code for the poetry generation form
console.log('loaded generate.js');

if (!CodeMirror) {
    throw 'Missing requirement CodeMirror';
}

if (!prosaicweb) {
    throw 'Missing requirement prosaicweb';
}

(function () {
    // grumph
    var qs = document.querySelector.bind(document);

    // events
    var template_selected = function (state, e) {
        var option;
        if (e.explicitOriginalTarget) { // mozilla only
            option = e.explicitOriginalTarget;
        }
        else {
            option = qs("option[value=" + e.target.value + "]");
        }
        state.template_editor.setValue(JSON.pretty_print(option.dataset.json));
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

        var corpus_name = document.createElement('span');
        var corpus_link = document.createElement('a');
        corpus_link.href = "/corpora/" + poem.corpus.id;
        corpus_link.innerHTML = poem.corpus.name;
        corpus_name.innerHTML = " from corpus ";
        corpus_name.appendChild(corpus_link);
        poem_controls.appendChild(corpus_name);

        var sources_list = document.createElement('sub');
        sources_list.innerHTML = 'sources: ';
        sources.forEach(function(source) {
            var source_link = document.createElement('a');
            source_link.href = "/sources/" + source.id;
            source_link.innerHTML = source.name;
            sources_list.appendChild(source_link);
            sources_list.innerHTML += ' ';
        });

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

    // init
    var state = {
        template_select: qs('#templates'),
        generate_form: qs('#generate'),
        output: qs('#output'),
        preselected_template_option: qs('#templates').selectedOptions[0],
        template_editor: CodeMirror.fromTextArea(
            qs('textarea'),
            {mode:'javascript'}
        ),
    };

    state.template_select.addEventListener(
        'change',
        template_selected.bind(null, state)
    );
    state.generate_form.addEventListener(
        'submit',
        submit_generation.bind(null, state),
        true
    );
    state.template_editor.setValue(
        JSON.pretty_print(
            state.preselected_template_option.dataset.json
        )
    );
})();

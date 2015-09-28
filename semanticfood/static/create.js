$(document).ready(function () {

    var steps = 1;
    var ingredients = 1;

    $("#add-instruction").on("click", function (e) {
        e.preventDefault();
        $(this).parent()
            .before('<div>' +
            '<textarea id="instruction-step-' + steps + '" placeholder="Describe the next step" name="instruction-step-' + steps + '"></textarea>' +
            '<button tabindex="-1" class="step-remove"">&#9003;         </button>' +
            '</div>');
        steps++;
    });


    $("#submit-button").on("click", function (e) {
        e.preventDefault();
        $("#create-form").submit();
    });

    $("#create-form").on("click", ".step-remove", function (e) {
        e.preventDefault();
        $(this).closest('div').remove();
    });

    $(document).on('keyup keypress', 'form input', function(e) {
        if(e.keyCode == 13) {
            e.preventDefault();
            return false;
        }
    });

    $("#ingredient-0").select2({
        ajax: {
            url: "https://api.github.com/search/repositories",
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    q: params.term, // search term
                    page: params.page
                };
            },
            processResults: function (data, page) {
                // parse the results into the format expected by Select2.
                // since we are using custom formatting functions we do not need to
                // alter the remote JSON data
                return {
                    results: data.items
                };
            },
            cache: true
        },
        escapeMarkup: function (markup) { return markup; },
        minimumInputLength: 1,
        templateResult: formatRepo,
        templateSelection: formatRepoSelection
    });

    function formatRepo (repo) {
        if (repo.loading) return repo.text;

        var markup = '<div class="clearfix">' +
            '<div class="col-sm-1">' +
            '<img src="' + repo.owner.avatar_url + '" style="max-width: 100%" />' +
            '</div>' +
            '<div clas="col-sm-10">' +
            '<div class="clearfix">' +
            '<div class="col-sm-6">' + repo.full_name + '</div>' +
            '<div class="col-sm-3"><i class="fa fa-code-fork"></i> ' + repo.forks_count + '</div>' +
            '<div class="col-sm-2"><i class="fa fa-star"></i> ' + repo.stargazers_count + '</div>' +
            '</div>';

        if (repo.description) {
            markup += '<div>' + repo.description + '</div>';
        }

        markup += '</div></div>';

        return markup;
    }

    function formatRepoSelection (repo) {
        return repo.full_name || repo.text;
    }
});
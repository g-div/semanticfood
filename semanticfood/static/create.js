$(document).ready(function () {

    var steps = 1;
    var ingredients = 1;

    $("#add-instruction").on("click", function (e) {
        e.preventDefault();
        $(this).parent()
            .before('<div>' +
            '<textarea id="instructionStep-' + steps + '" placeholder="Describe the next step" name="instructionStep-' + steps + '"></textarea>' +
            '<button tabindex="-1" class="step-remove"">&#11013;</button>' +
            '</div>');
        steps++;
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
            url: "http://api.nal.usda.gov/ndb/search",
            dataType: 'json',
            delay: 300,
            data: function (params) {
                return {
                    q: params.term,
                    format: "json",
                    api_key: "V5zvO2rQuQAq36ajpuFhTaPLm74RsN9CrcCP3YG1",
                    sort: "r",
                    max: "50",
                    offset: "0"
                };
            },
            processResults: function (data, page) {
                if (data.list.item.length > 0) {

                    var results = [];

                    $.each(data.list.item, function (i, v) {
                        var o = {};
                        o.id = v.ndbno;
                        o.name = v.name;
                        results.push(o);
                    });

                    return {
                        results: results
                    };
                } else {
                    return {
                        results: null
                    };
                }
            },
            cache: true
        },
        escapeMarkup: function (markup) { return markup; },
        minimumInputLength: 3,
        templateResult: formatIngredient,
        templateSelection: formatIngredientSelection,
        placeholder: "Type in an ingredient"
    });

    $('#ingredient-0').on("change", function(e) {
        var ndbno = $(this).val();
        var wip = '			<input id="qty" class="qtyinput" placeholder="QTY" type="number" name="qty">';
        var wip = '<select class="qty-type-select"><option>QTY</option><option>dsfsdf</option></select>';
    });

    function formatIngredient (ingredient) {
        if (ingredient.loading) return ingredient.name;

        var markup = '</div>' + ingredient.name + '</div>';

        return markup;
    }

    function formatIngredientSelection (ingredient) {
        return ingredient.name;
    }
});
$(document).ready(function () {

    var steps = 1;
    var ingredients = 1;

    var API_KEY = "V5zvO2rQuQAq36ajpuFhTaPLm74RsN9CrcCP3YG1";

    $("#add-instruction").on("click", function (e) {
        e.preventDefault();
        $(this).parent()
            .before('<div>' +
            '<textarea required id="instructionStep-' + steps + '" placeholder="Describe the next step" name="instructionStep-' + steps + '"></textarea>' +
            '<button tabindex="-1" class="step-remove remove-button">&#9003;</button>' +
            '</div>');
        steps++;
    });

    $("#create-form").on("click", ".step-remove", function (e) {
        e.preventDefault();
        $(this).closest('div').remove();
    });

    $("#create-form").on("click", ".ingredient-remove", function (e) {
        e.preventDefault();
        $(this).closest('div').remove();
    });

    $(document).on('keyup keypress', 'form input', function(e) {
        if(e.keyCode == 13) {
            e.preventDefault();
            return false;
        }
    });

    $("#add-ingredient").on("click", function (e) {
        e.preventDefault();
        $(this).parent()
            .before('<div><select id="ingredient-' + ingredients + '" name="ingredient-' + ingredients + '"></select>' +
            '<input required id="qty-ingredient-' + ingredients + '" class="qtyinput" placeholder="g / ml" type="number" name="qty">' +
            '<button tabindex="-1" class="ingredient-remove remove-button">&#9003;</button>' +
            '</div>');
        initAjaxSelectorForIngredient(ingredients);
        ingredients++;
    });

    function initAjaxSelectorForIngredient(ingredient) {
        $("#ingredient-"+ingredient).select2({
            ajax: {
                url: "http://api.nal.usda.gov/ndb/search",
                dataType: 'json',
                delay: 300,
                data: function (params) {
                    return {
                        q: params.term,
                        format: "json",
                        api_key: API_KEY,
                        sort: "r",
                        max: "100",
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

                        results.sort(function(a, b){
                            return a.name.length - b.name.length;
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
            escapeMarkup: function (markup) {
                return markup;
            },
            minimumInputLength: 3,
            templateResult: formatIngredient,
            templateSelection: formatIngredientSelection,
            placeholder: "Type in an ingredient"
        });
    }
    initAjaxSelectorForIngredient(0); //Default ingredient

    function formatIngredient (ingredient) {
        if (ingredient.loading) return ingredient.name;

        var markup = '</div>' + ingredient.name + '</div>';

        return markup;
    }

    function formatIngredientSelection (ingredient) {
        return ingredient.name;
    }
});
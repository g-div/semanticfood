$(document).ready(function () {
    var filterCount = 0;
    $("#add-filter").on("click", function (e) {
        e.preventDefault();
        $(this).parent()
            .before('<div>' +
            '<select class="filter-type-selector" data-id="' + filterCount + '" id="filter-' + filterCount + '-type" name="filter-' + filterCount + '-type">' +
            '<option value="0">Nutritional Value</option>' +
            '<option value="1">Ingredient</option>' +
            '<option value="2">Effort</option>' +
            '</select>' +
            '<select class="filter-operator" id="filter-' + filterCount + '-operator" name="filter-' + filterCount + '-operator"></select>' +
            '<input class="filter-value" id="filter-' + filterCount + '-value" name="filter-' + filterCount + '-value">' +
            '<select class="filter-unit" id="filter-' + filterCount + '-unit" name="filter-' + filterCount + '-unit"></select>' +
            '<button tabindex="-1" class="ingredient-remove remove-button">&#9003;</button>' +
            '<hr></div>');
        setNutrionalFilters(filterCount);
        filterCount++;
    });

    function setNutrionalFilters(id) {
        var opElem = $('#filter-' + id + '-operator');
        var valElem = $('#filter-' + id + '-value');
        var unitElem = $('#filter-' + id + '-unit');
        valElem.val("");

        opElem.css("width", "30%");
        valElem.css("width", "30%");
        valElem.css("margin", "0 5%");
        valElem.attr("type", "number");
        valElem.attr("placeholder", "Amount");
        unitElem.css("width", "30%");


        setSelectOptions({lt: 'Fewer than', gt: 'More than'}, opElem);
        setSelectOptions({
                energyPer100g: 'Calories (kcal)',
                carbohydratesPer100g: 'Carbohydrates (g)',
                cholesterolPer100g: 'Cholesterol (mg)',
                fatPer100g: 'Fat (g)',
                unsaturatedFatContent: 'Unsaturated Fat (g)',
                saturatedFatPer100g: 'Saturated Fat (g)',
                transFatPer100g: 'Trans Fat (g)',
                fiberPer100g: 'Fibers (g)',
                proteinsPer100g: 'Protein (g)',
                sodiumPer100g: 'Sodium (mg)',
                sugarsPer100g: 'Sugar (g)'
            },
            unitElem);
        unitElem.show();
    }

    function setIngredientFilters(id) {
        var opElem = $('#filter-' + id + '-operator');
        var valElem = $('#filter-' + id + '-value');
        var unitElem = $('#filter-' + id + '-unit');
        valElem.val("");

        opElem.css("width", "50%");
        valElem.css("width", "45%");
        valElem.css("margin", "0 0 0 5%");
        valElem.attr("type", "text");
        valElem.attr("placeholder", "Ingredient");


        setSelectOptions({eq: 'Must contain', neq: 'Must not contain'}, opElem);
        unitElem.hide();
        unitElem.empty();
    }

    function setEffortFilters(id) {
        var opElem = $('#filter-' + id + '-operator');
        var valElem = $('#filter-' + id + '-value');
        var unitElem = $('#filter-' + id + '-unit');
        valElem.val("");

        opElem.css("width", "30%");
        valElem.css("width", "30%");
        valElem.css("margin", "0 5%");
        valElem.attr("type", "number");
        valElem.attr("placeholder", "Time (Minutes)");
        unitElem.css("width", "30%");


        setSelectOptions({lt: 'Less than', gt: 'More than'}, opElem);
        setSelectOptions({
                totalTime: 'Total Time',
                prepTime: 'Preparation Time',
                cookTime: 'Cooking Time'
            },
            unitElem);
        unitElem.show();
    }

    function setSelectOptions(options, elem) {
        elem.empty();
        $.each(options, function (val, text) {
            elem.append(
                $('<option></option>').val(val).html(text)
            );
        });
    }

    $(".search-box").on("click", ".ingredient-remove", function (e) {
        e.preventDefault();
        $(this).closest('div').remove();
    });

    $(".search-box").on("change", ".filter-type-selector", function (e) {
        var typeId = $(this).val();
        var id = $(this).data("id");
        switch (typeId) {
            case "0":
                setNutrionalFilters(id);
                break;
            case "1":
                setIngredientFilters(id);
                break;
            case "2":
                setEffortFilters(id);
                break;
        }
        e.preventDefault();

    });

    $(document).on('keyup keypress', 'form input', function (e) {
        if (e.keyCode == 13) {
            e.preventDefault();
            return false;
        }
    });

    $("#submit-button").on("click", function (e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: 'search',
            data: $("#search-form").serialize(),
            encode: true
        }).done(function (data) {
            var resultBlock = $(".search-results");
            var results = $.parseJSON(data);

            resultBlock.empty();
            if (results[0] != undefined) {
                $.each(results, function (count, result) {
                    resultBlock.append('<a href="/recipes/' + result.url + '"><div><h3>' + result.title + '</h3><p>' + result.description + '</p></div></a>');
                });
            } else {
                resultBlock.append('<div><h3>No results found.</h3><p>Try some different filter parameters.</p></div>');
            }



        });
    });
});
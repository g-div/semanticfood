$(document).ready(function () {
    var filterCount = 0;
    $("#add-filter").on("click", function (e) {
        e.preventDefault();
        $(this).parent()
            .before('<div>' +
            '<select class="filter-type-selector" data-id="' + filterCount + '" id="filter-type-' + filterCount + '" name="filter-type-' + filterCount + '">' +
            '<option value="0">Nutritional Value</option>' +
            '<option value="1">Ingredient</option>' +
            '<option value="2">Effort</option>' +
            '</select>' +
            '<select class="filter-operator" id="filter-operator-' + filterCount + '" name="filter-operator-' + filterCount + '"></select>' +
            '<input class="filter-value" id="filter-value-' + filterCount + '" name="filter-value-' + filterCount + '">' +
            '<select class="filter-unit" id="filter-unit-' + filterCount + '" name="filter-unit-' + filterCount + '"></select>' +
            '<button tabindex="-1" class="ingredient-remove remove-button">&#9003;</button>' +
            '</div><hr>');
        setNutrionalFilters(filterCount);
        filterCount++;
    });

    function setNutrionalFilters(id) {
        var opElem = $('#filter-operator-' + id);
        var valElem = $('#filter-value-' + id);
        var unitElem = $('#filter-unit-' + id);
        valElem.val("");

        opElem.css("width", "30%");
        valElem.css("width", "30%");
        valElem.css("margin", "0 5%");
        valElem.attr("type", "number");
        valElem.attr("placeholder", "Amount");
        unitElem.css("width", "30%");


        setSelectOptions({lt : 'Fewer than', gt : 'More than'}, opElem);
        setSelectOptions({
            calories : 'Calories (kcal)',
            carbohydrateContent : 'Carbohydrates (g)',
            cholesterolContent : 'Cholesterol (mg)',
            fatContent : 'Fat (g)',
            unsaturatedFatContent: 'Unsaturated Fat (g)',
            saturatedFatContent : 'Saturated Fat (g)',
            fiberContent : 'Fibers (g)',
            proteinContent : 'Protein (g)',
            sodiumContent : 'Sodium (mg)',
            sugarContent : 'Sugar (g)'
            },
            unitElem);
        unitElem.show();
    }

    function setIngredientFilters(id) {
        var opElem = $('#filter-operator-' + id);
        var valElem = $('#filter-value-' + id);
        var unitElem = $('#filter-unit-' + id);
        valElem.val("");

        opElem.css("width", "50%");
        valElem.css("width", "45%");
        valElem.css("margin", "0 0 0 5%");
        valElem.attr("type", "text");
        valElem.attr("placeholder", "Ingredient");


        setSelectOptions({lt : 'Must contain', gt : 'Must not contain'}, opElem);
        unitElem.hide();
        unitElem.empty();
    }

    function setEffortFilters(id) {
        var opElem = $('#filter-operator-' + id);
        var valElem = $('#filter-value-' + id);
        var unitElem = $('#filter-unit-' + id);
        valElem.val("");

        opElem.css("width", "30%");
        valElem.css("width", "30%");
        valElem.css("margin", "0 5%");
        valElem.attr("type", "number");
        valElem.attr("placeholder", "Time (Minutes)");
        unitElem.css("width", "30%");


        setSelectOptions({lt : 'Less than', gt : 'More than'}, opElem);
        setSelectOptions({
                totalTime : 'Total Time',
                prepTime : 'Preparation Time',
                cookTime : 'Cooking Time'
            },
            unitElem);
        unitElem.show();
    }

    function setSelectOptions(options, elem) {
        elem.empty();
        $.each(options, function(val, text) {
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

    $(document).on('keyup keypress', 'form input', function(e) {
        if(e.keyCode == 13) {
            e.preventDefault();
            return false;
        }
    });
});

// ---------------------------------------------------------------- About

//$("body").children().css( "maxWidth", screen.width + "px" );
$("#about .section-content > .chat-bubble").each(function(){
    var $this = $(this);
    var height = $this.parent().find(".section-header").height();
    var x, y;

    y = $this.position().top;

    if (y < 0) {
        console.log($this.css("margin-top"));
        y = $this.css("margin-top");
    }

    y += $this.height();

    x = Math.sqrt(y*height - Math.pow(y, 2));

    $this.css("margin-left", x + 16*4 + "px");
});

// ---------------------------------------------------------------- Availability

$("#availability .integration-code").each(function(){
    var $this = $(this);
    $this.css("width", 3.99 + "em");
    $this.css("padding-left", 0  + "em");
});

$("#availability .integration-slider").mouseenter(function(){
    var integrationCode = $(this).find(".integration-code");
    integrationCode.animate({
        "width": "100%",
        "padding-left": "4.5em"
        }, 400);
});

$("#availability .integration-slider").mouseleave(function(){
    var integrationCode = $(this).find(".integration-code");
    integrationCode.animate({
        "width": "3.99em",
        "padding-left": "0em",
        }, 400);
});

// ---------------------------------------------------------------- Byte Training

// ---------------------------------- Collapsible Tree

$(".collapsible-tree-node .collapsible-tree").hide();

$("#collapse-all-button").click(function(){
    if ($(this).text() === "Expandir todo") {
        $(this).text("Colapsar todo");
        $(".collapse-button").each(function(){
            if ($(this).text() === "+") $(this).text("-");
        });
        $(".collapsible-tree-node .collapsible-tree").slideDown();
    } else {
        $(this).text("Expandir todo");
        $(".collapse-button").each(function(){
            if ($(this).text() === "-") $(this).text("+");
        });
        $(".collapsible-tree-node .collapsible-tree").slideUp();
    }
});

$("span.collapse-button").click(function(){
    if ($(this).text() === "+") $(this).text("-");
    else $(this).text("+");
    $(this).parent().children("div.collapsible-tree").slideToggle();
});

$("#training .collapsible-tree-node li").click(function(){

    var questionCategory = $(this).parent();
    var categoryID = questionCategory.attr("id");
    var questionInputForm = $('#user-question-form');
    var questionInput = questionInputForm.find('#user-question-visible');

    questionInputForm.hide();

    $("#training .section-content div.selected,li.selected,span.selected").removeClass("selected");

    $(this).addClass("selected");
    questionCategory.addClass("selected");
    questionCategory.children("span").addClass("selected");

    categoryID = categoryID.slice(categoryID.indexOf('-')+1);
    questionInputForm.find('input[name="question-cat"]').val(categoryID);
    questionInputForm.find('input[name="question-text"]').val("");

    $(this).after(questionInputForm);
    questionInputForm.find('#question-input-status').hide();
    questionInputForm.fadeIn();

    questionInput.css("margin-bottom", "0em");
    questionInput.animate({
        "margin-bottom": "1.75em",
        }, 400);
    questionInput.find('input[name="question-text"]').prop('autofocus');
    questionInput.find('input[name="question-text"]').focus();

});

// ---------------------------------- Form

$("#user-question-form").hide();

$("#send-button").click(function(){
    $('#user-question-form').triggerHandler('submit');
});

$("#question-input input").change(userQuestionValidation);

$("#user-question-form").submit(function(event){
    event.preventDefault();

    // Validation
    if (!userQuestionValidation()) return false;

    // AJAX
    var url = $(this).attr("action");
    $.ajax({
        url: url,
        type: 'post',
        dataType: 'json',
        data: $(this).serialize(),
        success: function(data) {
                    var inputStatus = $('#question-input-status');
                    var inputStatusMessage = inputStatus.find('.chat-bubble-content');

                    inputStatus.fadeOut();
                    inputStatus.removeClass();
                    if (data['success']) {
                        inputStatus.addClass('success');
                        inputStatusMessage.html('<p>¡Gracias!</p>');
                    } else if (data['error']) {
                        inputStatus.addClass('error');
                        inputStatusMessage.html('<p>' + data['error'] + '</p>');
                    } else if (data['fishy']) {
                        inputStatus.addClass('fishy-error');
                        inputStatusMessage.html('<p>Algo sospechoso ha ocurrido... ¿No sabrás nada al respecto?</p>');
                    }
                    inputStatus.fadeIn();
                 }
    });

    return false;
});

function userQuestionValidation() {
    var questionCategory = $('#user-question-form input[name="question-cat"]');
    var questionText = $('#user-question-form input[name="question-text"]');
    var inputStatus = $('#question-input-status');
    var inputStatusMessage = inputStatus.find('.chat-bubble-content');

    inputStatus.fadeOut();
    inputStatus.removeClass();

    if (questionCategory.val() === undefined || questionCategory.val() === null || questionCategory.val() === ""){
        inputStatus.addClass('fishy-error');
        inputStatusMessage.html('<p>Algo sospechoso ha ocurrido... ¿No sabrás nada al respecto?</p>');
        inputStatus.fadeIn();
        return false;
    }

    if (questionText.val().length < 4) {
        inputStatus.addClass('error');
        inputStatusMessage.html("<p>¡Tu consulta es muy corta!</p>");
        inputStatus.fadeIn();
        return false;
    }

    if (questionText.val().length > 200) {
        inputStatus.addClass('error');
        inputStatusMessage.html("<p>¡Tu consulta es demasiado larga!</p>");
        inputStatus.fadeIn();
        return false;
    }
    return true;
}


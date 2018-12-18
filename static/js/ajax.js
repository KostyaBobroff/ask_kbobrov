$(document).ready(function () {

    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $("div.like").click(function () {
        console.log('yeah');
        $.ajax({
            url : "set_like/", // the endpoint
            type : "POST", // http method
            data : JSON.stringify({ id: parseInt($(this).children()[0].attributes['value'].value),

                    question_or_comment: $(this).children()[0].attributes['name'].value,
                    like: true }), // data sent with the post request

            // handle a successful response
            success : function(json) {

                if (json["question_or_comment"] === true){

                    $("#question_"+json["id"]).text(json["count"]);
                } else{
                    $("#comment_"+json["id"]).text(json["count"]);
                }

            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    });
    $("div.dislike").click(function () {
         $.ajax({
            url : {% url %}, // the endpoint
            type : "POST", // http method
            data : JSON.stringify({ id: parseInt($(this).children()[0].attributes['value'].value),

                    question_or_comment: $(this).children()[0].attributes['name'].value,
                    like: false }), // data sent with the post request

            // handle a successful response
            success : function(json) {

                if (json["question_or_comment"] === true){

                    $("#question_"+json["id"]).text(json["count"]);
                } else{
                    $("#comment_"+json["id"]).text(json["count"]);
                }

            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    });
    
});
$(document).ready(function() {

    $(".favorite").submit(function() {

        $.post("/favorite",
               JSON.stringify({button_id: $(this).children("button").val()}),
               function(data){alert("Added to favorites: " + data.coursename + ", " + data.courseterm);},
               'json');

        return false;
    });

    $(".download").submit(function() {

        $.post("/download",
               JSON.stringify({button_id: $(this).children("button").val()}),
               function(data){alert(data.message);},
               'json');

        return false;
    });

    $(".download-favorites").submit(function() {

        $.post("/download-favorites",
               JSON.stringify({button_id: $(this).children("button").val()}),
               function(data){alert(data.message);},
               'json');

        return false;
    });

});
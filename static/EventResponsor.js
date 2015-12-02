function add_handler() {
    $.ajax({
        url: "/tablemanager",
        type: "POST",
        data: {
            "which": "add_item",
            "table_name": $("#table_name").val(),
            "table_type": $("#table_type").val(),
            "data_level": $("#data_level").val(),
            "proc_name": $("#proc_name").val(),
            "note": $("#note").val(),
            "input_man": $("#input_man").val(),
            "input_date": $("#input_date").val(),
            "update_man": $("#update_man").val(),
            "update_date": $("#update_date").val()
        },
        success: function (json) {
            $("body").fadeTo(500, 1);
            $("#ref_msg").remove();
            console.log(json);
            table_content = json.new_content;
            console.log(table_content);
            var url = "../static/d3table.js";
            $.getScript(url, function(){ console.log("Refreshing table!"); });
        }
    });
    $("body").fadeTo(500, 0.4);
    $("body").append("<div id='ref_msg'>Updating data...</div>");
}

function edit_handler() {
    console.log("Tijiaole!");
    var id = $(this).attr('id').slice(6, 7);
    var item = $(this).attr('id').slice(7, 8);
    var substring = $(this).attr('id').slice(6, 8);
    console.log(id, item, substring);
    var content = $('#editor'+substring).val();
    console.log("Editing content: "+content);
    $.ajax({
        url: "/tablemanager",
        type: "POST",
        data: {
            "which": "edit_item",
            "id_index": id,
            "item_index": item,
            "edit_content": content
        },
        success: function (json) {
            $("body").fadeTo(500, 1);
            $("#ref_msg").remove();
            console.log(json);
            table_content = json.new_content;
            console.log(table_content);
            var url = "../static/d3table.js";
            $.getScript(url, function(){ console.log("Refreshing table!"); });
        }
    });
    $("body").fadeTo(500, 0.4);
    $("body").append("<div id='ref_msg'>Updating data...</div>");
    $(this).css("visibility", "hidden");
    $('#editor'+substring).css("visibility", "hidden");
}

function remove_handler() {
    if (confirm("确定移除这项吗？") == true) {
        var id = $(this).attr('id').slice(6, 7);
        console.log("The ID you choose is " + id);
        $.ajax({
            url: "/tablemanager",
            type: "POST",
            data: {
                "which": "remove_item",
                "id_index": id
            },
            success: function (json) {
                $("body").fadeTo(500, 1);
                $("#ref_msg").remove();
                console.log(json);
                table_content = json.new_content;
                console.log(table_content);
                var url = "../static/d3table.js";
                $.getScript(url, function () {
                    console.log("Refreshing table!");
                });
            }
        });
        $("body").fadeTo(500, 0.4);
        $("body").append("<div id='ref_msg'>Updating data...</div>");
        $(this).css("visibility", "hidden");
        alert("ID为"+id+"的项已被移除");
    }

}

function updatePage(serverResponse) {
    $("tbody").html(serverResponse.table);
    $("#pages").html(serverResponse.page_list);
    $("#page_"+serverResponse.pn).addClass("active");
}

$(document).ready(function(){
    $.ajax({
        url: "search",
        method: "get",
        success: updatePage
    });
    $("#search_form").children().change(function(){
        $.ajax({
            url: $(this).parent().attr("action"),
            method: "get",
            data: $(this).parent().serialize(),
            success: updatePage
        })
    });
    $(document).on("click", ".page-link", function(){
        $.ajax({
            url: $(this).attr("href"),
            method: "get",
            data: $("#search_form").serialize(),
            success: updatePage
        });
        return false;
    });
});
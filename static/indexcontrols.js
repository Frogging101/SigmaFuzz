var ol = "\
<div class=\"overlay\">\
    <table style=\"height:100%;width:100%\">\
        <tr>\
            <td id=\"app_td\" style=\"vertical-align:middle;border-right: 1px solid #000000;\">\
                Approve\
            </td>\
            <td id= \"arc_td\" style=\"vertical-align:middle;\">\
                Archive\
            </td>\
        </tr>\
    </table>\
</div>"

var csrft = $.cookie("csrftoken");

function post(url,data){
    jQuery.ajax(url, {headers: {"X-CSRFToken": csrft},data: data,type: "post",async: false});
}

function arc(id,arcd,arc_td,subbox){
    var archiveURL = "http://"+window.location.hostname+"/s/"+id+"/archival";
    arcd = !arcd;

    post(archiveURL,{"set": String(arcd)});

    subbox.attr("data-arcd",String(arcd));

    if (arcd) {
        arc_td.text("Unarchive");
    }
    else{
        arc_td.text("Archive");
    }
}
function app(id,appd,app_td,subbox){
    var approveURL="http://"+window.location.hostname+"/s/"+id+"/approval";
    appd = !appd;

    post(approveURL,{"set": String(appd)});

    subbox.attr("data-appd",String(appd));

    if (appd) {
        app_td.text("Unapprove");
    }
    else{
        app_td.text("Approve");
    }
}

function noOverlay(){
    $(".overlay").remove();
}

function showOverlay(subbox){
    noOverlay();
    subbox.append(ol);
    var overlay = subbox.find(".overlay");
    overlay.on("mouseout",function(){ $(this).remove();});
    subbox.on("mouseleave",function(){ overlay.remove();});
    var app_td = overlay.find("#app_td");
    var arc_td = overlay.find("#arc_td");
    var appd = (subbox.attr("data-appd") === "true");
    var arcd = (subbox.attr("data-arcd") === "true");

    arc_td.on("click tap", function(){ arc(subbox.attr("data-id"),arcd,arc_td,subbox);});
    app_td.on("click tap", function(){ app(subbox.attr("data-id"),appd,app_td,subbox);});

    if (appd) {
        app_td.text("Unapprove");
    }
    if (arcd) {
        arc_td.text("Unarchive");
    }
}

var hlid = -1;

function kbHandler(e){
    if(e.which <= 40 && e.which >=37)
        e.preventDefault();
    if(e.which == 39)
        hlid++;
    else if(e.which == 37){
        hlid--;
    }
    else if((e.which == 38 || e.which == 40) && hlid > -1){
        var subboxWidth = $(".submissionBox")[0].offsetWidth;
        var mainWidth = $("#main")[0].clientWidth;

        var perRow = parseInt(mainWidth/subboxWidth);
        if(e.which == 38)
            hlid -= perRow;
        else
            hlid += perRow;
    }
    if(hlid < -1)
        hlid = -1;
    if(hlid == -1)
        noOverlay();
    var subbox = $("div.submissionBox:eq("+hlid+")");
    showOverlay(subbox);

    if(hlid == -1)
        return;

    var overlay = subbox.find(".overlay");
    var app_td = overlay.find("#app_td");
    var arc_td = overlay.find("#arc_td");
    var appd = (subbox.attr("data-appd") === "true");
    var arcd = (subbox.attr("data-arcd") === "true");

    if(e.which == 81 || e.which == 113)
        app(subbox.attr("data-id"),appd,app_td,subbox);
    else if(e.which == 87 || e.which == 119)
        arc(subbox.attr("data-id"),arcd,arc_td,subbox);
}

$(document).ready(
    function(){
        $(".submissionBox img").parent("a").on({
            "mouseover tap": function(){
                subbox = $(this).parent(".submissionBox");
                showOverlay(subbox);
            }
        });
        $(document).keydown(kbHandler);
    }
);

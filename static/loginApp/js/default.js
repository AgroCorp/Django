function showEditPopup(url) {
    var win = window.open(url, "Edit",
        'height=500,width=800,resizable=yes,scrollbars=yes');
    return false;
}

function changePaginator(element, url) {
    var selected = element.value
    var forwardUrl = url + "?page=1&count=" +selected;
    console.log(forwardUrl);
    window.location.replace(forwardUrl);
}

function showAddPopup(triggeringLink) {
    var name = triggeringLink.id.replace(/^add_/, '');
    href = triggeringLink.href;
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}
function closePopup(win, newID, newRepr, id) {
    $(id).append('<option value=' + newID + ' selected >' + newRepr + '</option>')
    win.onunload = refreshParent;
    function refreshParent() {
        win.opener.location.reload();
    }
    win.close();
}

function closePopupDel(win, newId, newRepr, id) {
    $(id).remove(id);
    win.onunload = refreshParent;
    function refreshParent() {
        win.opener.location.reload();
    }
    win.close();
}

function nameChanged(select, type) {
    let url = '';
    var selected_id = document.forms[0].name.value;
    var recipe_id = document.forms[0].recipe_id.value;
    var storage_id = document.forms[0].storage_id.value;

    var idTokens = window.location.href.split('/');
    console.log(idTokens);
    var formId = idTokens.at(-2);
    if (window.location.href.includes('new'))
    {
        url = "/recipes/" + type + "/new?selected_name_id=" + selected_id + "&recipe_id=" + recipe_id + "&storage_id=" + storage_id;
    } else {
        url = "/recipes/" + type + '/' + formId + "/edit?selected_name_id=" + selected_id + "&recipe_id=" + recipe_id + "&storage_id=" + storage_id;
    }
    console.log(url);
    window.location.replace(url);
}

jQuery("#backButton").click(function(){
    window.opener.location.reload();
    close();
});

jQuery("a").click(function (event) {
    var type = event.currentTarget.id;
    var name = "";

    if(!type.includes('view') && !type.includes('edit')) {return;}

    var tokens = type.split("_");
    console.log(tokens);

    if(tokens[1] == "ingredient") {
        //console.log(event.currentTarget.name);
        let id = event.currentTarget.name; // 0. ing_id 1. recipe_id

        let url = '/recipes/ingredient/' + id + "/" + tokens[0];
        console.log(id);
        showEditPopup(url);
        event.currentTarget.src = url;
    } else {
        let name = $("#id_"+ tokens[1] + " option:selected").text();
        let data = {"name":name};
        $.ajax({
            type : 'GET',
            url :  '/recipes/' + tokens[1] + '/ajax/get_' + tokens[1] + '_id',
            data : data,
            success : function(data){
                let url = "/recipes/" + tokens[1] + "/" + data[tokens[1] +'_id'] + "/" + tokens[0];
                console.log(url)
                showEditPopup(url);
            },
            error: function(data) {
                alert("Hoppá, valami hiba történt");
            }
        });
    }
})



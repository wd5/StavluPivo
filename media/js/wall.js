var tmp;
function addStiker (ev) {
    tmp=ev;
    if(ev.target.id!='wall')
	return;
    showPopupAdd(ev.pageX,ev.pageY,ev.layerX,ev.layerY);

/*
    var s = jQuery('<div class="stiker"><h1>Тестовое задание</h1><p>Основной текст_</p><div id="to-user">Alex</div></div>');
    $(ev.target).append(s);
    s.append(jQuery('<div class="close">x</div>').click(removeStiter));

    s.css('left',ev.layerX.toString()+'px');
    s.css('top',ev.layerY.toString()+'px');

    addTask();
*/
}

function showPopupAdd(x,y,x1,y1){
    var root=$(document.body);
    jQuery('#exposeMask').css('display','block');
    root.prepend('<div id="body-dialog" class="modal" style="position: absolute; margin: 0 auto; z-index: 9999"></div>');
    var dialog=$('#body-dialog');
    root=dialog;
    root.append('<div class="modal-header"><a href="javascript:closeDialog()" class="close">x</a><h3>Title</h3><input type="text" id="add-kask-title" value="Title"/></div>');
    root.append('<div class="modal-body"><textarea rous="3" id="add-kask-text" value=""/></div>');
    dialog.css('top',y.toString()+'px');
    dialog.css('left',x.toString()+'px');
    dialog.css('width','300px');
    root.append('<div class="modal-footer"><div class="btn success" onclick="addTask('+x1.toString()+','+y1.toString()+');">Add</div><div onclick="closeDialog();" class="btn">Сancel</div></div>');
}

function closeDialog(){
    $('#body-dialog').remove();
    jQuery('#exposeMask').css('display','none');
}


function addTask(x,y){
    var r;
    $.ajax({
	       method : 'GET',
	       url : 'add-task/',
	       data : {'title':$('#add-kask-title')[0].value,
		       'text':$('#add-kask-text')[0].value,
		       'x':x,
		       'y':y},
	       success : function(data){
		   if(data['errors'].length==0){
		       var d=data['data'];
		       var s = jQuery('<div class="stiker"><h1>'+d['title']+'</h1><p>'+d['text']+'</p><div id="to-user">'+d['user']+'</div></div>');
		       $('#wall').append(s);
		       s.append(jQuery('<div class="close" taskId="'+d['id'].toString()+'">x</div>').click(removeStiter));
		       s.css('left',d['x'].toString()+'px');
		       s.css('top',d['y'].toString()+'px');
		       closeDialog();
		   }
	       }
	   });
}

function removeStiter (ev) {
    $.ajax({
	       method : 'GET',
	       url : $(ev.target).attr('taskId')+'/del-task/',
	       data : {},
	       success : function(){}
	   });

    $(ev.target).parent().remove();
}

$(document).ready(
    function () {
	$('.topbar').dropdown();
	$('#wall').click(addStiker);
	$('.close').click(removeStiter);
    });



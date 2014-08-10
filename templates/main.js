function setVal(obj){
	var id = $(obj).attr("id");
	if($(obj).hasClass('selected')){
		$(obj).removeClass('selected');
		$("#"+id+"_input").val('');
	}else{
		$(obj).addClass('selected');
		$("#"+id+"_input").val(id);
	}
};

$(function(){
	$('input').focus(function(){
		$(this).parent().addClass('focus');
	}).blur(function(){
		$(this).parent().removeClass('focus');
	});
	$(document).bind('keydown', 'ctrl+return', function(){
		$('#submit').click();
	});
	$(document).bind('keydown', 'A', function(){
		$('#fumi').click();
	});
	$(document).bind('keydown', 'S', function(){
		$('#other').click();
	});
	$(document).bind('keydown', 'D', function(){
		$('#aikawa').click();
	});
	$(document).bind('keydown', 'F', function(){
		$('#yui').click();
	});
	$(document).bind('keydown', 'H', function(){
		$('#kei').click();
	});
	$(document).bind('keydown', 'J', function(){
		$('#yukari').click();
	});
	$(document).bind('keydown', 'K', function(){
		$('#yuzuko').click();
	});
	$(document).bind('keydown', 'L', function(){
		$('#okasan').click();
	});
});

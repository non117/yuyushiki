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


});

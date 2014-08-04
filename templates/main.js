$(function(){
	$(document).ready(function(){
		setTimeout(function(){
			$('#textbox').focus();
		}, 1);
	});
	$('input').focus(function(){
		$(this).parent().addClass('focus');
	}).blur(function(){
		$(this).parent().removeClass('focus');
	});

});

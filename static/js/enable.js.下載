function rightButtonDisable(e){}

document.body.onkeydown = function(e){
	if (typeof(event) == 'undefined') event = e;
	if ((event.keyCode == 78) && (event.ctrlKey)){
		alert ("No new window")
		event.cancelBubble = true;
		event.returnValue = false;
		event.keyCode = false;
		return false;
	}
};

function newsReadMore(nid)
{
	window.open("/learn/news/news_read.php?node="+nid.substring(1),null,"height=400,width=600, scrollbars=yes, resizable=yes, status=no,toolbar=no,menubar=no,location=no");
}

var result  = null;
document.addEventListener('contextmenu', function(event) {
	var node = event.target;
	while(node && node.nodeName.toLowerCase() != 'a') {
		node = node.parentNode;
	}
	result = node;
}, true);

chrome.runtime.onMessage.addListener(onMessageHandler);

function onMessageHandler(request, sender, sendResponse) {
	if (result && request.command == "Copy") {
		sendResponse({linktext: result.textContent});
	} else if(request.command == "Paste") {
		var element = document.activeElement;
		element.select();
		document.execCommand("paste",false,null);
		// bug? code below should work?
		//var enterEvent = new KeyboardEvent("keypress", {code: "Enter"});
		//document.dispatchEvent(enterEvent);
	}
	return true;
};

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
	if (result && request.command == "Search") {
		sendResponse({linktext: result.textContent});
	}
	return true;
};

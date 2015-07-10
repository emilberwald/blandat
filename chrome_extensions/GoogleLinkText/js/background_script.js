chrome.runtime.onInstalled.addListener(function() {
	chrome.contextMenus.create(
		{
			contexts: ['link'],
			title: 'Google Linktext',
			id: "Google Linktext"
		}
	);
});

chrome.contextMenus.onClicked.addListener(onClickHandler);
function onClickHandler(info, tab){
	if(info.menuItemId == "Google Linktext"){
		chrome.tabs.sendMessage(
			tab.id,
			{command: "Copy"},
			function(response) {
				if(response){
					toClipboard(response.linktext.replace(/\s+/g, " "));
					chrome.tabs.create(
						{url: "http://www.google.se/"}, 
						function (searchtab){
							searchTabID = searchtab.id;
						}
					);
				}
			}
		);
	}
};
var searchTabID = null;

function toClipboard(text){
	var ta = document.getElementById('copy-area');
	ta.value = text;
	ta.select();
	document.execCommand("copy",false,null);	
}

chrome.tabs.onUpdated.addListener(onUpdated);
function onUpdated(tabId, changeInfo, tab) {
	if(searchTabID == tabId && tab.status == "complete"){
		chrome.tabs.sendMessage(
			tabId,
			{command: "Paste"},
			function(response){
				searchTabID = null;
			}
		);
	}
}

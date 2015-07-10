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
			{command: "Search"}, 
			function(response) {
				chrome.tabs.create({url: 
					"http://www.google.se/"
					//find other way of doing this, google thinks you are a bot if you use this.. :(
					//search?q=\""
					//+encodeURIComponent(response.linktext.replace(/\s+/g, " "))
					//+"\""});
			}
		)
	}
};

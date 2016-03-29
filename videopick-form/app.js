function AddVideo(file, video) 
{
	video.src = URL.createObjectURL(file);
	video.loop = true;
	video.controls = true;
	video.autoplay = true;
	video.autostart = true;
	video.play();
}

function HandleFileSelect(evt) {
	var files = evt.currentTarget.files;
	 //while (element.firstChild) {
	 //	 element.removeChild(element.firstChild);
	 //}
	for (var i = 0; i != files.length; i++) {
		var video = document.createElement("video");
		document.getElementById("container").appendChild(video);
		var file = files.item(i);
		if(file)
		{
			AddVideo(file, video);
		}
	}
}
window.onload = function () {
	var container = document.createElement("div");
	container.id = "container";
	document.body.appendChild(container);
	var choose = document.createElement("input");
	choose.multiple = true;
	choose.type="file";
	choose.accept="video/*";
	choose.name="files[]";
	choose.addEventListener("change",HandleFileSelect,false);
	document.body.appendChild(choose);
	var play = document.createElement("button");
	play.addEventListener("click", function() {
		var videos = container.children;
		for(var videoNo = 0; videoNo != videos.length; videoNo++){
			videos[videoNo].play();
		}
	}, false);
	play.appendChild(document.createTextNode("►"));
	document.body.appendChild(play);
	var pause = document.createElement("button");
	pause.addEventListener("click", function() {
		var videos = container.children;
		for(var videoNo = 0; videoNo != videos.length; videoNo++){
			videos[videoNo].pause();
		}
	}, false);
	pause.appendChild(document.createTextNode("❚❚"));
	document.body.appendChild(pause);
};
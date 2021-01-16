URL = window.URL || window.webkitURL;

var gumStream; 						//stream from getUserMedia()
var rec; 							//Recorder.js object
var input; 							//MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record

var button = document.getElementById("send-button");

//add events to button
button.addEventListener("click", recording);


function recording() {
	if (button.value == "off") {
		button.value = "on";
		button.style.background = "#8f2e2e";
		console.log("button clicked - started recording");
		
		var constraints = { audio: true, video:false }
		
		navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
			console.log("getUserMedia() success, stream created, initializing Recorder.js ...");
			
			audioContext = new AudioContext();
			
			console.log("2");
			gumStream = stream;
			
			console.log("3");
			input = audioContext.createMediaStreamSource(stream);
			
			console.log("4");
			rec = new Recorder(input,{numChannels:1})
			
			console.log("5");
			rec.record()
			
			console.log("Recording started");
			
		}).catch(function(err) {
            console.log("Error occured:", err);
			button.disabled = true;
		});
	}
	else {
		button.value = "off";
		button.style.background = "#2ca089";
		console.log("button clicked - stopped recording");
				
		rec.stop();
		console.log("Recording stopped");

		gumStream.getAudioTracks()[0].stop();

		rec.exportWAV(send_audio_to_server);
	}
}

function send_audio_to_server(blob) {
	var url = URL.createObjectURL(blob);

	var xhr = new XMLHttpRequest();
    var fd = new FormData();
	fd.append("audio_data", blob);

	xhr.onreadystatechange = function() {
		if (xhr.readyState === 4) {
			console.log("recognized string: " + xhr.response);

			var form = document.createElement("form");
			form.method = "POST";
			form.action = "/action_handler";
			
			var i = document.createElement("input");
			i.type = "text";
			i.name = "recognized_string";
			i.value = xhr.responseText;

			form.appendChild(i);
			document.body.appendChild(form);

			form.submit();
		}
	  }
	
	xhr.open("POST","/speech_to_text/", true);
	xhr.send(fd);
}
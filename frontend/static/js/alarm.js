function stopAlarm(){
    //TODO - Fix this, cause when there isn't sound, this code returns null
    let alarmSound = document.getElementById("alarm-sound").pause();
}
(function () {
    document.getElementById("send-button").addEventListener("click", stopAlarm);
})();


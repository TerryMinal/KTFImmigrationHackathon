var mainText = document.getElementById("mainText");
var submitBtn = document.getElementById("submitBtn");
var time = document.getElementById("time");


function submitClick() {
  var firebaseRef = firebase.database().ref().child("Post");
  var messageText = mainText.value;

  firebaseRef.set(messageText);

  const preObject = document.getElementById("post");
  const posts = document.getElementById("post");

  firebaseRef.on('value', function(datasnapshot) {
    preObject.innerText = datasnapshot.val();
  });
}

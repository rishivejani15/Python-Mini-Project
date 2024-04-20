importScripts('https://www.gstatic.com/firebasejs/8.10.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.10.0/firebase-messaging.js');

// Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyCKqR9wTb5eFBoQ8hULyaqFjaggDHMe1uM",
authDomain: "quizapp-e74fe.firebaseapp.com",
projectId: "quizapp-e74fe",
storageBucket: "quizapp-e74fe.appspot.com",
messagingSenderId: "1098236969903",
appId: "1:1098236969903:web:814566823b75fe2557a55a",
measurementId: "G-31DZJS4FLZ"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// Retrieve Firebase Messaging instance
const messaging = firebase.messaging();

// Listen for background messages
messaging.onBackgroundMessage((payload) => {
    console.log('Received background message:', payload);
});


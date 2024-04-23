importScripts('https://www.gstatic.com/firebasejs/8.10.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.10.0/firebase-messaging.js');

// Firebase configuration
const firebaseConfig = {
   YOUR_FIREBASE_PROJECT_CONFIGURATION
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// Retrieve Firebase Messaging instance
const messaging = firebase.messaging();

// Listen for background messages
messaging.onBackgroundMessage((payload) => {
    console.log('Received background message:', payload);
});


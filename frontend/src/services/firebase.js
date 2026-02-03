import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyCPvLS3pisPvP5_0V-EvTEPRSOITPzgcQ0",
    authDomain: "mindful-connect-97471.firebaseapp.com",
    projectId: "mindful-connect-97471",
    storageBucket: "mindful-connect-97471.firebasestorage.app",
    messagingSenderId: "122354041409",
    appId: "1:122354041409:web:007959ca06a9fe78ef7cc0",
    measurementId: "G-YDHWTHSJWR"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);
export const googleProvider = new GoogleAuthProvider();

export default app;

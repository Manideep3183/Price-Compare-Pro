import { initializeApp } from "firebase/app";
import {
  getAuth,
  GoogleAuthProvider,
  onAuthStateChanged,
  sendPasswordResetEmail,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signInWithPopup,
  signOut,
  updateProfile,
  User,
} from "firebase/auth";

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();

// Configure Google provider
googleProvider.setCustomParameters({
  prompt: 'select_account'
});

// Auth API helpers
export const AuthAPI = {
  // Listen to auth state changes
  onChange: (callback: (user: User | null) => void) => 
    onAuthStateChanged(auth, callback),

  // Sign up with email and password
  signUpEmail: async (email: string, password: string, displayName?: string) => {
    const { user } = await createUserWithEmailAndPassword(auth, email, password);
    if (displayName) {
      await updateProfile(user, { displayName });
    }
    return user;
  },

  // Login with email and password
  loginEmail: (email: string, password: string) =>
    signInWithEmailAndPassword(auth, email, password),

  // Login with Google
  loginGoogle: () => signInWithPopup(auth, googleProvider),

  // Logout
  logout: () => signOut(auth),

  // Send password reset email
  forgotPassword: (email: string) => sendPasswordResetEmail(auth, email),

  // Get current user's ID token
  getIdToken: () => auth.currentUser?.getIdToken(),

  // Get current user
  getCurrentUser: () => auth.currentUser,
};

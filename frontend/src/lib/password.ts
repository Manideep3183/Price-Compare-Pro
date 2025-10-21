// Password strength checker and generator
export const generateSecurePassword = (): string => {
  const uppercase = "ABCDEFGHJKLMNPQRSTUVWXYZ";
  const lowercase = "abcdefghijkmnpqrstuvwxyz";
  const numbers = "23456789";
  const symbols = "!@#$%^&*()-_=+";
  
  const allChars = uppercase + lowercase + numbers + symbols;
  
  let password = "";
  // Ensure at least one of each type
  password += uppercase[Math.floor(Math.random() * uppercase.length)];
  password += lowercase[Math.floor(Math.random() * lowercase.length)];
  password += numbers[Math.floor(Math.random() * numbers.length)];
  password += symbols[Math.floor(Math.random() * symbols.length)];
  
  // Fill the rest randomly (total 14 characters)
  for (let i = 4; i < 14; i++) {
    password += allChars[Math.floor(Math.random() * allChars.length)];
  }
  
  // Shuffle the password
  return password.split('').sort(() => Math.random() - 0.5).join('');
};

// Password strength checker (0-4 scale)
export const checkPasswordStrength = (password: string): {
  score: number;
  label: string;
  color: string;
} => {
  let score = 0;
  
  if (!password) return { score: 0, label: "None", color: "text-gray-500" };
  
  // Length check
  if (password.length >= 8) score++;
  if (password.length >= 12) score++;
  
  // Character variety checks
  if (/[a-z]/.test(password)) score++;
  if (/[A-Z]/.test(password)) score++;
  if (/[0-9]/.test(password)) score++;
  if (/[^A-Za-z0-9]/.test(password)) score++;
  
  // Normalize to 0-4 scale
  const normalizedScore = Math.min(Math.floor(score / 1.5), 4);
  
  const labels = ["Very Weak", "Weak", "Fair", "Good", "Strong"];
  const colors = [
    "text-red-500",
    "text-orange-500",
    "text-yellow-500",
    "text-blue-500",
    "text-green-500"
  ];
  
  return {
    score: normalizedScore,
    label: labels[normalizedScore],
    color: colors[normalizedScore]
  };
};

// Validate password meets requirements
export const validatePassword = (password: string): {
  isValid: boolean;
  errors: string[];
} => {
  const errors: string[] = [];
  
  if (password.length < 8) {
    errors.push("Password must be at least 8 characters");
  }
  if (!/[a-z]/.test(password)) {
    errors.push("Password must contain a lowercase letter");
  }
  if (!/[A-Z]/.test(password)) {
    errors.push("Password must contain an uppercase letter");
  }
  if (!/[0-9]/.test(password)) {
    errors.push("Password must contain a number");
  }
  if (!/[^A-Za-z0-9]/.test(password)) {
    errors.push("Password must contain a special character");
  }
  
  return {
    isValid: errors.length === 0,
    errors
  };
};

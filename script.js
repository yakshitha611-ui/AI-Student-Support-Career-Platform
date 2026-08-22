const form = document.getElementById('loginForm');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const togglePasswordButton = document.getElementById('togglePassword');
const formError = document.getElementById('formError');

const emailError = document.getElementById('emailError');
const passwordError = document.getElementById('passwordError');
const API_BASE = window.__API_BASE__ || 'https://ai-student-support-career-platform-4.onrender.com';

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function setFieldError(field, message) {
  const errorBox = field === 'email' ? emailError : passwordError;
  errorBox.textContent = message;
  const input = field === 'email' ? emailInput : passwordInput;

  if (message) {
    input.setAttribute('aria-invalid', 'true');
  } else {
    input.setAttribute('aria-invalid', 'false');
  }
}

function clearFormError() {
  formError.textContent = '';
  formError.classList.remove('visible');
}

function validateForm() {
  let isValid = true;

  clearFormError();

  if (!emailInput.value.trim()) {
    setFieldError('email', 'Email is required.');
    isValid = false;
  } else if (!emailPattern.test(emailInput.value.trim())) {
    setFieldError('email', 'Invalid email format.');
    isValid = false;
  } else {
    setFieldError('email', '');
  }

  if (!passwordInput.value.trim()) {
    setFieldError('password', 'Password is required.');
    isValid = false;
  } else {
    setFieldError('password', '');
  }

  return isValid;
}

togglePasswordButton.addEventListener('click', () => {
  const isHidden = passwordInput.type === 'password';
  passwordInput.type = isHidden ? 'text' : 'password';
  togglePasswordButton.textContent = isHidden ? 'Hide' : 'Show';
  togglePasswordButton.setAttribute('aria-label', isHidden ? 'Hide password' : 'Show password');
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  if (!validateForm()) {
    return;
  }

  const payload = {
    email: emailInput.value.trim(),
    password: passwordInput.value,
  };

  try {
    const response = await fetch(`${API_BASE}/api/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    const result = await response.json().catch(() => ({}));

    if (!response.ok) {
      const message = result?.detail || result?.message || 'Incorrect email or password.';
      formError.textContent = String(message).toLowerCase().includes('email') || String(message).toLowerCase().includes('password')
        ? 'Incorrect email or password.'
        : 'We could not log you in right now. Please try again.';
      formError.classList.add('visible');
      return;
    }

    const token = result?.access_token;
    if (!token) {
      formError.textContent = 'We could not log you in right now. Please try again.';
      formError.classList.add('visible');
      return;
    }

    localStorage.setItem('authToken', token);
    localStorage.setItem('access_token', token);
    sessionStorage.setItem('authToken', token);
    sessionStorage.setItem('access_token', token);

    if (result.user) {
      localStorage.setItem('currentUser', JSON.stringify(result.user));
    }

    window.location.href = 'dashboard.html';
  } catch (error) {
    formError.textContent = 'We could not log you in right now. Please try again.';
    formError.classList.add('visible');
  }
});

import { useMemo, useState } from 'react';

const initialForm = {
  email: '',
  password: '',
};

const initialErrors = {
  email: '',
  password: '',
  form: '',
};

const validateEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

function App() {
  const [formData, setFormData] = useState(initialForm);
  const [errors, setErrors] = useState(initialErrors);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const passwordStrengthHint = useMemo(() => {
    if (!formData.password) {
      return 'Use your account password';
    }

    return formData.password.length >= 8 ? 'Password looks good' : 'Use at least 8 characters';
  }, [formData.password]);

  const updateField = (event) => {
    const { name, value } = event.target;

    setFormData((prev) => ({ ...prev, [name]: value }));
    setErrors((prev) => ({ ...prev, [name]: '', form: '' }));
  };

  const validateForm = () => {
    const nextErrors = { ...initialErrors };

    if (!formData.email.trim()) {
      nextErrors.email = 'Email is required.';
    } else if (!validateEmail(formData.email.trim())) {
      nextErrors.email = 'Enter a valid email address.';
    }

    if (!formData.password.trim()) {
      nextErrors.password = 'Password is required.';
    }

    return nextErrors;
  };

  const persistToken = (token) => {
    const storage = window.localStorage;
    const keys = ['authToken', 'token', 'accessToken', 'jwt', 'studentAuthToken'];
    const existingKey = keys.find((key) => storage.getItem(key));

    const savedKey = existingKey || 'authToken';
    storage.setItem(savedKey, token);

    if (token) {
      storage.setItem('authToken', token);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const nextErrors = validateForm();
    if (nextErrors.email || nextErrors.password) {
      setErrors(nextErrors);
      return;
    }

    setIsSubmitting(true);
    setErrors((prev) => ({ ...prev, form: '' }));

    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: formData.email.trim(),
          password: formData.password,
        }),
      });

      const payload = await response.json().catch(() => null);

      if (!response.ok) {
        const message = payload?.message || 'Incorrect email or password.';
        throw new Error(message);
      }

      const token = payload?.token || payload?.accessToken || payload?.data?.token || payload?.authToken;

      if (!token) {
        throw new Error('Unable to sign in right now. Please try again.');
      }

      persistToken(token);

      if (payload?.user) {
        window.localStorage.setItem('currentUser', JSON.stringify(payload.user));
      }

      window.location.href = '/dashboard';
    } catch (error) {
      const displayMessage = error.message.includes('email') || error.message.includes('password')
        ? 'Incorrect email or password.'
        : 'We could not log you in right now. Please try again.';

      setErrors((prev) => ({ ...prev, form: displayMessage }));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="login-page">
      <header className="topbar">
        <div className="topbar__content">
          <div className="brand-wrap">
            <div className="brand-mark">AI</div>
            <div>
              <p className="brand-name">AI-Powered Student Support</p>
              <p className="brand-subtitle">Your personalized learning and career companion</p>
            </div>
          </div>
        </div>
      </header>

      <main className="login-shell">
        <section className="login-card" aria-labelledby="login-title">
          <div className="card-header">
            <span className="eyebrow">Welcome</span>
            <h1 id="login-title">Welcome Back</h1>
            <p>Login to continue your journey</p>
          </div>

          <form onSubmit={handleSubmit} noValidate>
            <div className="form-field">
              <label htmlFor="email">Email</label>
              <input
                id="email"
                name="email"
                type="email"
                value={formData.email}
                onChange={updateField}
                placeholder="Enter your email"
                aria-invalid={Boolean(errors.email)}
                aria-describedby={errors.email ? 'email-error' : undefined}
                autoComplete="email"
              />
              {errors.email ? <span id="email-error" className="field-error">{errors.email}</span> : null}
            </div>

            <div className="form-field">
              <label htmlFor="password">Password</label>
              <div className="password-wrap">
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  value={formData.password}
                  onChange={updateField}
                  placeholder="Enter your password"
                  aria-invalid={Boolean(errors.password)}
                  aria-describedby={errors.password ? 'password-error' : undefined}
                  autoComplete="current-password"
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowPassword((prev) => !prev)}
                  aria-label={showPassword ? 'Hide password' : 'Show password'}
                >
                  {showPassword ? 'Hide' : 'Show'}
                </button>
              </div>
              {errors.password ? <span id="password-error" className="field-error">{errors.password}</span> : null}
              {!errors.password ? <span className="password-hint">{passwordStrengthHint}</span> : null}
            </div>

            {errors.form ? <div className="form-alert" role="alert">{errors.form}</div> : null}

            <button type="submit" className="login-button" disabled={isSubmitting}>
              {isSubmitting ? 'Logging in...' : 'Login'}
            </button>
          </form>

          <p className="register-link">
            Don&apos;t have an account? <a href="register.html">Register</a>
          </p>
        </section>
      </main>
    </div>
  );
}

export default App;

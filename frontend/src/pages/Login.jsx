import { useState } from 'react';
import api from '../utils/api';

function Login({ setIsAuthenticated }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const response = await api.post('/auth/login', { email, password });
            localStorage.setItem('token', response.data.access_token);
            setIsAuthenticated(true);
        } catch (err) {
            setError(err.response?.data?.detail || 'Login failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            {/* Animated Background */}
            <div className="login-bg-pulse"></div>

            <div className="card-glass animate-slide-in login-card">
                <div className="text-center mb-4">
                    <h1 className="gradient-text text-3xl font-bold mb-2">LeadPilot AI</h1>
                    <p style={{ color: 'var(--gray-400)' }}>Autonomous Lead Qualification System</p>
                </div>

                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label className="input-label">
                            Email Address
                        </label>
                        <input
                            type="email"
                            className="input"
                            placeholder="your@email.com"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>

                    <div className="mb-3">
                        <label className="input-label">
                            Password
                        </label>
                        <input
                            type="password"
                            className="input"
                            placeholder="••••••••"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>

                    {error && (
                        <div className="alert-error">
                            {error}
                        </div>
                    )}

                    <button
                        type="submit"
                        className="btn btn-primary w-full"
                        disabled={loading}
                    >
                        {loading ? 'Signing in...' : 'Sign In'}
                    </button>
                </form>

                <div className="text-center mt-4" style={{ fontSize: '0.875rem', color: 'var(--gray-400)' }}>
                    <p>
                        Don't have an account?{' '}
                        <a
                            href="/register"
                            style={{
                                color: 'var(--primary)',
                                textDecoration: 'none',
                                fontWeight: 600
                            }}
                        >
                            Create one now
                        </a>
                    </p>
                </div>
            </div>
        </div>
    );
}

export default Login;

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../utils/api';

function Register() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        full_name: '',
        tenant_name: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            // Create payload matching backend expectations
            const payload = {
                email: formData.email,
                password: formData.password,
                full_name: formData.full_name,
                tenant_id: 'default-tenant', // Use default tenant
                role: 'admin'
            };

            const response = await api.post('/auth/register', payload);
            localStorage.setItem('token', response.data.access_token);
            navigate('/dashboard');
        } catch (err) {
            setError(err.response?.data?.detail || 'Registration failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{
            minHeight: '100vh',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            padding: '2rem'
        }}>
            <div style={{
                maxWidth: '480px',
                width: '100%',
                background: 'white',
                borderRadius: '20px',
                padding: '3rem',
                boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)'
            }}>
                {/* Header */}
                <div style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
                    <div style={{
                        fontSize: '3rem',
                        marginBottom: '0.5rem',
                        filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.1))'
                    }}>
                        🚀
                    </div>
                    <h1 style={{
                        fontSize: '1.75rem',
                        fontWeight: 'bold',
                        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                        WebkitBackgroundClip: 'text',
                        WebkitTextFillColor: 'transparent',
                        marginBottom: '0.5rem'
                    }}>
                        Welcome to LeadPilot AI
                    </h1>
                    <p style={{ color: '#6b7280', fontSize: '0.95rem' }}>
                        Create your account to get started
                    </p>
                </div>

                {/* Error Alert */}
                {error && (
                    <div style={{
                        padding: '1rem',
                        background: '#fee2e2',
                        border: '1px solid #fca5a5',
                        borderRadius: '12px',
                        color: '#dc2626',
                        marginBottom: '1.5rem',
                        fontSize: '0.875rem'
                    }}>
                        ⚠️ {error}
                    </div>
                )}

                {/* Form */}
                <form onSubmit={handleSubmit}>
                    {/* Full Name */}
                    <div style={{ marginBottom: '1.5rem' }}>
                        <label style={{
                            display: 'block',
                            marginBottom: '0.5rem',
                            fontSize: '0.875rem',
                            fontWeight: 600,
                            color: '#374151'
                        }}>
                            Full Name
                        </label>
                        <input
                            type="text"
                            placeholder="John Doe"
                            value={formData.full_name}
                            onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                            required
                            style={{
                                width: '100%',
                                padding: '0.75rem 1rem',
                                fontSize: '0.95rem',
                                border: '2px solid #e5e7eb',
                                borderRadius: '12px',
                                outline: 'none',
                                transition: 'all 0.2s',
                                background: '#f9fafb'
                            }}
                            onFocus={(e) => e.target.style.borderColor = '#667eea'}
                            onBlur={(e) => e.target.style.borderColor = '#e5e7eb'}
                        />
                    </div>

                    {/* Company Name */}
                    <div style={{ marginBottom: '1.5rem' }}>
                        <label style={{
                            display: 'block',
                            marginBottom: '0.5rem',
                            fontSize: '0.875rem',
                            fontWeight: 600,
                            color: '#374151'
                        }}>
                            Company Name
                        </label>
                        <input
                            type="text"
                            placeholder="Acme Inc."
                            value={formData.tenant_name}
                            onChange={(e) => setFormData({ ...formData, tenant_name: e.target.value })}
                            required
                            style={{
                                width: '100%',
                                padding: '0.75rem 1rem',
                                fontSize: '0.95rem',
                                border: '2px solid #e5e7eb',
                                borderRadius: '12px',
                                outline: 'none',
                                transition: 'all 0.2s',
                                background: '#f9fafb'
                            }}
                            onFocus={(e) => e.target.style.borderColor = '#667eea'}
                            onBlur={(e) => e.target.style.borderColor = '#e5e7eb'}
                        />
                    </div>

                    {/* Email */}
                    <div style={{ marginBottom: '1.5rem' }}>
                        <label style={{
                            display: 'block',
                            marginBottom: '0.5rem',
                            fontSize: '0.875rem',
                            fontWeight: 600,
                            color: '#374151'
                        }}>
                            Email Address
                        </label>
                        <input
                            type="email"
                            placeholder="you@company.com"
                            value={formData.email}
                            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                            required
                            style={{
                                width: '100%',
                                padding: '0.75rem 1rem',
                                fontSize: '0.95rem',
                                border: '2px solid #e5e7eb',
                                borderRadius: '12px',
                                outline: 'none',
                                transition: 'all 0.2s',
                                background: '#f9fafb'
                            }}
                            onFocus={(e) => e.target.style.borderColor = '#667eea'}
                            onBlur={(e) => e.target.style.borderColor = '#e5e7eb'}
                        />
                    </div>

                    {/* Password */}
                    <div style={{ marginBottom: '2rem' }}>
                        <label style={{
                            display: 'block',
                            marginBottom: '0.5rem',
                            fontSize: '0.875rem',
                            fontWeight: 600,
                            color: '#374151'
                        }}>
                            Password
                        </label>
                        <input
                            type="password"
                            placeholder="••••••••"
                            value={formData.password}
                            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                            required
                            minLength={6}
                            style={{
                                width: '100%',
                                padding: '0.75rem 1rem',
                                fontSize: '0.95rem',
                                border: '2px solid #e5e7eb',
                                borderRadius: '12px',
                                outline: 'none',
                                transition: 'all 0.2s',
                                background: '#f9fafb'
                            }}
                            onFocus={(e) => e.target.style.borderColor = '#667eea'}
                            onBlur={(e) => e.target.style.borderColor = '#e5e7eb'}
                        />
                        <p style={{ fontSize: '0.75rem', color: '#9ca3af', marginTop: '0.5rem' }}>
                            Minimum 6 characters
                        </p>
                    </div>

                    {/* Submit Button */}
                    <button
                        type="submit"
                        disabled={loading}
                        style={{
                            width: '100%',
                            padding: '0.875rem',
                            fontSize: '1rem',
                            fontWeight: 600,
                            color: 'var(--gray-900)',
                            background: loading ? '#9ca3af' : 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                            border: 'none',
                            borderRadius: '12px',
                            cursor: loading ? 'not-allowed' : 'pointer',
                            transition: 'all 0.3s',
                            boxShadow: '0 4px 12px rgba(102, 126, 234, 0.4)'
                        }}
                        onMouseEnter={(e) => !loading && (e.target.style.transform = 'translateY(-2px)')}
                        onMouseLeave={(e) => e.target.style.transform = 'translateY(0)'}
                    >
                        {loading ? '⏳ Creating Account...' : '🚀 Create Account'}
                    </button>

                    {/* Footer */}
                    <div style={{ textAlign: 'center', marginTop: '1.5rem' }}>
                        <p style={{ color: '#6b7280', fontSize: '0.875rem' }}>
                            Already have an account?{' '}
                            <a
                                href="/login"
                                style={{
                                    color: '#667eea',
                                    textDecoration: 'none',
                                    fontWeight: 600
                                }}
                                onClick={(e) => {
                                    e.preventDefault();
                                    navigate('/login');
                                }}
                            >
                                Sign in
                            </a>
                        </p>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default Register;

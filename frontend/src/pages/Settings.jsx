import { useState } from 'react';
import Sidebar from '../components/Sidebar';

function Settings() {
    const [copied, setCopied] = useState(false);

    const widgetCode = `<!-- LeadPilot AI Chat Widget -->
<script>
  window.leadpilotConfig = {
    tenantKey: 'demo-key-12345',
    apiUrl: 'http://localhost:8000'
  };
</script>
<script src="http://localhost:5173/widget/leadpilot-widget.js"></script>
<link rel="stylesheet" href="http://localhost:5173/widget/widget.css">`;

    const copyToClipboard = () => {
        navigator.clipboard.writeText(widgetCode);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div style={{ display: 'flex' }}>
            <Sidebar />
            <div style={{ marginLeft: '260px', flex: 1, padding: '2rem', minHeight: '100vh' }}>
                <div className="animate-slide-in">
                    <h1 className="text-3xl font-bold mb-2">Settings</h1>
                    <p style={{ color: 'var(--gray-400)', marginBottom: '2rem' }}>
                        Configure your LeadPilot AI system
                    </p>

                    {/* Widget Integration */}
                    <div className="card" style={{ marginBottom: '2rem' }}>
                        <h2 className="text-xl font-bold mb-3">🔌 Widget Integration</h2>
                        <p style={{ color: 'var(--gray-700)', marginBottom: '1rem' }}>
                            Copy and paste this code before the closing &lt;/body&gt; tag on your website:
                        </p>

                        <div style={{
                            position: 'relative',
                            background: 'rgba(0, 0, 0, 0.3)',
                            padding: '1rem',
                            borderRadius: 'var(--radius-md)',
                            fontFamily: 'monospace',
                            fontSize: '0.875rem',
                            overflow: 'auto'
                        }}>
                            <pre style={{ margin: 0, color: 'var(--gray-900)' }}>
                                {widgetCode}
                            </pre>
                            <button
                                onClick={copyToClipboard}
                                className="btn btn-primary"
                                style={{
                                    position: 'absolute',
                                    top: '1rem',
                                    right: '1rem',
                                    fontSize: '0.75rem',
                                    padding: '0.5rem 1rem'
                                }}
                            >
                                {copied ? '✓ Copied!' : '📋 Copy Code'}
                            </button>
                        </div>
                    </div>

                    {/* Tenant Information */}
                    <div className="card" style={{ marginBottom: '2rem' }}>
                        <h2 className="text-xl font-bold mb-3">🏢 Tenant Information</h2>

                        <div style={{ marginBottom: '1rem' }}>
                            <label style={{
                                display: 'block',
                                marginBottom: '0.5rem',
                                fontSize: '0.875rem',
                                fontWeight: 600,
                                color: 'var(--gray-700)'
                            }}>
                                Tenant Key
                            </label>
                            <input
                                type="text"
                                className="input"
                                value="demo-key-12345"
                                readOnly
                                style={{ background: 'rgba(0, 0, 0, 0.2)' }}
                            />
                        </div>

                        <div style={{ marginBottom: '1rem' }}>
                            <label style={{
                                display: 'block',
                                marginBottom: '0.5rem',
                                fontSize: '0.875rem',
                                fontWeight: 600,
                                color: 'var(--gray-700)'
                            }}>
                                Business Name
                            </label>
                            <input
                                type="text"
                                className="input"
                                value="Demo Business"
                                readOnly
                                style={{ background: 'rgba(0, 0, 0, 0.2)' }}
                            />
                        </div>
                    </div>

                    {/* Lead Scoring Thresholds */}
                    <div className="card" style={{ marginBottom: '2rem' }}>
                        <h2 className="text-xl font-bold mb-3">🎯 Lead Scoring Thresholds</h2>

                        <div style={{ marginBottom: '1rem' }}>
                            <label style={{
                                display: 'block',
                                marginBottom: '0.5rem',
                                fontSize: '0.875rem',
                                fontWeight: 600,
                                color: 'var(--gray-700)'
                            }}>
                                Hot Lead Threshold (Score ≥)
                            </label>
                            <input
                                type="number"
                                className="input"
                                value="70"
                                readOnly
                                style={{ background: 'rgba(0, 0, 0, 0.2)' }}
                            />
                        </div>

                        <div style={{ marginBottom: '1rem' }}>
                            <label style={{
                                display: 'block',
                                marginBottom: '0.5rem',
                                fontSize: '0.875rem',
                                fontWeight: 600,
                                color: 'var(--gray-700)'
                            }}>
                                Warm Lead Threshold (Score ≥)
                            </label>
                            <input
                                type="number"
                                className="input"
                                value="40"
                                readOnly
                                style={{ background: 'rgba(0, 0, 0, 0.2)' }}
                            />
                        </div>

                        <p style={{ fontSize: '0.875rem', color: 'var(--gray-400)', marginTop: '1rem' }}>
                            💡 Tip: Leads are automatically scored based on contact completeness, budget, timeline urgency, and engagement.
                        </p>
                    </div>

                    {/* Email Notifications */}
                    <div className="card">
                        <h2 className="text-xl font-bold mb-3">📧 Email Notifications</h2>

                        <div style={{ marginBottom: '1rem' }}>
                            <label style={{
                                display: 'block',
                                marginBottom: '0.5rem',
                                fontSize: '0.875rem',
                                fontWeight: 600,
                                color: 'var(--gray-700)'
                            }}>
                                Notification Email
                            </label>
                            <input
                                type="email"
                                className="input"
                                value="turjoyewu@gmail.com"
                                readOnly
                                style={{ background: 'rgba(0, 0, 0, 0.2)' }}
                            />
                        </div>

                        <p style={{ fontSize: '0.875rem', color: 'var(--gray-400)' }}>
                            ✉️ You'll receive instant email alerts when hot leads are captured (score ≥ 70)
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Settings;

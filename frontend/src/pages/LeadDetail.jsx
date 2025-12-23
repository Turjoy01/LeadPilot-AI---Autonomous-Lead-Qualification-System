import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import api from '../utils/api';
import { format } from 'date-fns';

function LeadDetail() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [updating, setUpdating] = useState(false);

    useEffect(() => {
        fetchLead();
    }, [id]);

    const fetchLead = async () => {
        try {
            const response = await api.get(`/leads/${id}`);
            setData(response.data);
        } catch (error) {
            console.error('Error fetching lead:', error);
        } finally {
            setLoading(false);
        }
    };

    const updateStatus = async (newStatus) => {
        setUpdating(true);
        try {
            await api.patch(`/leads/${id}`, { status: newStatus });
            await fetchLead();
        } catch (error) {
            console.error('Error updating lead:', error);
        } finally {
            setUpdating(false);
        }
    };

    const getBadgeClass = (grade) => {
        const classes = {
            'HOT': 'badge-hot',
            'WARM': 'badge-warm',
            'COLD': 'badge-cold'
        };
        return `badge ${classes[grade] || ''}`;
    };

    if (loading) {
        return (
            <div style={{ display: 'flex' }}>
                <Sidebar />
                <div style={{ marginLeft: '260px', flex: 1, padding: '2rem' }}>
                    <div className="gradient-text text-center">Loading lead details...</div>
                </div>
            </div>
        );
    }

    if (!data) {
        return (
            <div style={{ display: 'flex' }}>
                <Sidebar />
                <div style={{ marginLeft: '260px', flex: 1, padding: '2rem' }}>
                    <div className="card text-center">
                        <h3 className="text-xl font-bold mb-2">Lead not found</h3>
                        <button onClick={() => navigate('/leads')} className="btn btn-primary mt-3">
                            Back to Leads
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    const { lead, conversation } = data;

    return (
        <div style={{ display: 'flex' }}>
            <Sidebar />
            <div style={{ marginLeft: '260px', flex: 1, padding: '2rem', minHeight: '100vh' }}>
                <div className="animate-slide-in">
                    <button
                        onClick={() => navigate('/leads')}
                        className="btn btn-secondary mb-3"
                        style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }}
                    >
                        ← Back to Leads
                    </button>

                    <div className="flex justify-between items-center mb-4">
                        <div>
                            <h1 className="text-3xl font-bold mb-2">
                                {lead.fields.name || 'Anonymous Lead'}
                            </h1>
                            <div className={getBadgeClass(lead.grade)}>
                                {lead.grade} - Score: {lead.score}/100
                            </div>
                        </div>
                    </div>

                    <div className="grid grid-2" style={{ gap: '1.5rem' }}>
                        {/* Lead Information */}
                        <div className="card">
                            <h2 className="text-xl font-bold mb-3">Contact Information</h2>

                            <div style={{ marginBottom: '1rem' }}>
                                <div style={{ fontSize: '0.875rem', color: 'var(--gray-400)', marginBottom: '0.25rem' }}>
                                    Name
                                </div>
                                <div style={{ fontWeight: 600 }}>
                                    {lead.fields.name || 'Not provided'}
                                </div>
                            </div>

                            <div style={{ marginBottom: '1rem' }}>
                                <div style={{ fontSize: '0.875rem', color: 'var(--gray-400)', marginBottom: '0.25rem' }}>
                                    Email
                                </div>
                                <div style={{ fontWeight: 600 }}>
                                    {lead.fields.email || 'Not provided'}
                                </div>
                            </div>

                            <div style={{ marginBottom: '1rem' }}>
                                <div style={{ fontSize: '0.875rem', color: 'var(--gray-400)', marginBottom: '0.25rem' }}>
                                    Phone
                                </div>
                                <div style={{ fontWeight: 600 }}>
                                    {lead.fields.phone || 'Not provided'}
                                </div>
                            </div>

                            <div style={{ marginBottom: '1rem' }}>
                                <div style={{ fontSize: '0.875rem', color: 'var(--gray-400)', marginBottom: '0.25rem' }}>
                                    Service Interest
                                </div>
                                <div style={{ fontWeight: 600 }}>
                                    {lead.fields.service_interest || 'Not specified'}
                                </div>
                            </div>

                            <div style={{ marginBottom: '1rem' }}>
                                <div style={{ fontSize: '0.875rem', color: 'var(--gray-400)', marginBottom: '0.25rem' }}>
                                    Budget
                                </div>
                                <div style={{ fontWeight: 600 }}>
                                    {lead.fields.budget || 'Not specified'}
                                </div>
                            </div>

                            <div style={{ marginBottom: '1rem' }}>
                                <div style={{ fontSize: '0.875rem', color: 'var(--gray-400)', marginBottom: '0.25rem' }}>
                                    Timeline
                                </div>
                                <div style={{ fontWeight: 600 }}>
                                    {lead.fields.timeline || 'Not specified'}
                                </div>
                            </div>

                            <div style={{ marginBottom: '1rem' }}>
                                <div style={{ fontSize: '0.875rem', color: 'var(--gray-400)', marginBottom: '0.25rem' }}>
                                    Created
                                </div>
                                <div style={{ fontWeight: 600 }}>
                                    {format(new Date(lead.created_at), 'PPpp')}
                                </div>
                            </div>
                        </div>

                        {/* Status Management */}
                        <div className="card">
                            <h2 className="text-xl font-bold mb-3">Lead Status</h2>

                            <div style={{ marginBottom: '1.5rem' }}>
                                <div style={{ fontSize: '0.875rem', color: 'var(--gray-400)', marginBottom: '0.5rem' }}>
                                    Current Status
                                </div>
                                <div className="badge badge-new" style={{ fontSize: '0.875rem' }}>
                                    {lead.status.toUpperCase()}
                                </div>
                            </div>

                            <div>
                                <div style={{ fontSize: '0.875rem', color: 'var(--gray-400)', marginBottom: '0.5rem' }}>
                                    Update Status
                                </div>
                                <div className="grid grid-2" style={{ gap: '0.5rem' }}>
                                    <button
                                        onClick={() => updateStatus('contacted')}
                                        className="btn btn-secondary"
                                        disabled={updating}
                                        style={{ fontSize: '0.75rem', padding: '0.5rem' }}
                                    >
                                        Contacted
                                    </button>
                                    <button
                                        onClick={() => updateStatus('qualified')}
                                        className="btn btn-secondary"
                                        disabled={updating}
                                        style={{ fontSize: '0.75rem', padding: '0.5rem' }}
                                    >
                                        Qualified
                                    </button>
                                    <button
                                        onClick={() => updateStatus('won')}
                                        className="btn btn-primary"
                                        disabled={updating}
                                        style={{ fontSize: '0.75rem', padding: '0.5rem' }}
                                    >
                                        Won
                                    </button>
                                    <button
                                        onClick={() => updateStatus('lost')}
                                        className="btn btn-secondary"
                                        disabled={updating}
                                        style={{ fontSize: '0.75rem', padding: '0.5rem' }}
                                    >
                                        Lost
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Conversation Transcript */}
                    {conversation && conversation.messages && conversation.messages.length > 0 && (
                        <div className="card mt-3">
                            <h2 className="text-xl font-bold mb-3">Conversation Transcript</h2>
                            <div style={{
                                maxHeight: '500px',
                                overflowY: 'auto',
                                padding: '1rem',
                                background: 'rgba(0, 0, 0, 0.2)',
                                borderRadius: 'var(--radius-md)'
                            }}>
                                {conversation.messages.map((msg, idx) => (
                                    <div
                                        key={idx}
                                        style={{
                                            marginBottom: '1rem',
                                            padding: '0.75rem',
                                            background: msg.role === 'user'
                                                ? 'rgba(99, 102, 241, 0.1)'
                                                : 'rgba(139, 92, 246, 0.1)',
                                            borderLeft: `3px solid ${msg.role === 'user' ? 'var(--primary)' : 'var(--secondary)'}`,
                                            borderRadius: 'var(--radius-sm)'
                                        }}
                                    >
                                        <div style={{
                                            fontSize: '0.75rem',
                                            color: 'var(--gray-400)',
                                            marginBottom: '0.25rem',
                                            fontWeight: 600
                                        }}>
                                            {msg.role === 'user' ? '👤 Customer' : '🤖 AI Assistant'}
                                            {msg.timestamp && (
                                                <span style={{ marginLeft: '0.5rem' }}>
                                                    • {format(new Date(msg.timestamp), 'HH:mm:ss')}
                                                </span>
                                            )}
                                        </div>
                                        <div style={{ fontSize: '0.875rem', lineHeight: 1.6 }}>
                                            {msg.content}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default LeadDetail;

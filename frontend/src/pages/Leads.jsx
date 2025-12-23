import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import api from '../utils/api';
import { format } from 'date-fns';

function Leads() {
    const [leads, setLeads] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState({ status: '', grade: '' });

    useEffect(() => {
        fetchLeads();
    }, [filter]);

    const fetchLeads = async () => {
        try {
            const params = {};
            if (filter.status) params.status = filter.status;
            if (filter.grade) params.grade = filter.grade;

            const response = await api.get('/leads', { params });
            setLeads(response.data);
        } catch (error) {
            console.error('Error fetching leads:', error);
        } finally {
            setLoading(false);
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

    return (
        <div style={{ display: 'flex' }}>
            <Sidebar />
            <div style={{ marginLeft: '260px', flex: 1, padding: '2rem', minHeight: '100vh' }}>
                <div className="animate-slide-in">
                    <div className="flex justify-between items-center mb-4">
                        <div>
                            <h1 className="text-3xl font-bold mb-2">Leads</h1>
                            <p style={{ color: 'var(--gray-400)' }}>
                                Manage and track your qualified leads
                            </p>
                        </div>
                    </div>

                    {/* Filters */}
                    <div className="card" style={{ marginBottom: '2rem' }}>
                        <div className="flex gap-md">
                            <div style={{ flex: 1 }}>
                                <label style={{
                                    display: 'block',
                                    marginBottom: '0.5rem',
                                    fontSize: '0.875rem',
                                    fontWeight: 600,
                                    color: '#374151'
                                }}>
                                    Filter by Grade
                                </label>
                                <select
                                    className="input"
                                    value={filter.grade}
                                    onChange={(e) => setFilter({ ...filter, grade: e.target.value })}
                                >
                                    <option value="">All Grades</option>
                                    <option value="HOT">🔥 Hot</option>
                                    <option value="WARM">⚡ Warm</option>
                                    <option value="COLD">❄️ Cold</option>
                                </select>
                            </div>

                            <div style={{ flex: 1 }}>
                                <label style={{
                                    display: 'block',
                                    marginBottom: '0.5rem',
                                    fontSize: '0.875rem',
                                    fontWeight: 600,
                                    color: '#374151'
                                }}>
                                    Filter by Status
                                </label>
                                <select
                                    className="input"
                                    value={filter.status}
                                    onChange={(e) => setFilter({ ...filter, status: e.target.value })}
                                >
                                    <option value="">All Statuses</option>
                                    <option value="new">New</option>
                                    <option value="contacted">Contacted</option>
                                    <option value="qualified">Qualified</option>
                                    <option value="won">Won</option>
                                    <option value="lost">Lost</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    {/* Leads List */}
                    {loading ? (
                        <div className="text-center mt-4">
                            <div className="gradient-text">Loading leads...</div>
                        </div>
                    ) : leads.length === 0 ? (
                        <div className="card text-center">
                            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>👥</div>
                            <h3 className="text-xl font-bold mb-2">No leads yet</h3>
                            <p style={{ color: 'var(--gray-400)' }}>
                                Leads will appear here once visitors interact with your chat widget
                            </p>
                        </div>
                    ) : (
                        <div className="grid" style={{ gap: '1rem' }}>
                            {leads.map((lead) => (
                                <Link
                                    key={lead.id}
                                    to={`/leads/${lead.id}`}
                                    style={{ textDecoration: 'none' }}
                                >
                                    <div className="card">
                                        <div className="flex justify-between items-center mb-3">
                                            <div>
                                                <h3 className="text-lg font-bold" style={{ color: '#1f2937' }}>
                                                    {lead.fields.name || 'Anonymous'}
                                                </h3>
                                                <p style={{ fontSize: '0.875rem', color: '#3b82f6' }}>
                                                    {lead.fields.email || 'No email provided'}
                                                </p>
                                            </div>
                                            <div className={getBadgeClass(lead.grade)}>
                                                {lead.grade} ({lead.score})
                                            </div>
                                        </div>

                                        <div className="grid grid-2" style={{ gap: '0.5rem', marginBottom: '1rem' }}>
                                            {lead.fields.phone && (
                                                <div style={{ fontSize: '0.875rem' }}>
                                                    <span style={{ color: 'var(--gray-400)' }}>📞 </span>
                                                    {lead.fields.phone}
                                                </div>
                                            )}
                                            {lead.fields.service_interest && (
                                                <div style={{ fontSize: '0.875rem' }}>
                                                    <span style={{ color: 'var(--gray-400)' }}>💼 </span>
                                                    {lead.fields.service_interest}
                                                </div>
                                            )}
                                            {lead.fields.budget && (
                                                <div style={{ fontSize: '0.875rem' }}>
                                                    <span style={{ color: 'var(--gray-400)' }}>💰 </span>
                                                    {lead.fields.budget}
                                                </div>
                                            )}
                                            {lead.fields.timeline && (
                                                <div style={{ fontSize: '0.875rem' }}>
                                                    <span style={{ color: 'var(--gray-400)' }}>⏰ </span>
                                                    {lead.fields.timeline}
                                                </div>
                                            )}
                                        </div>

                                        <div className="flex justify-between items-center" style={{
                                            paddingTop: '1rem',
                                            borderTop: '1px solid var(--gray-200)',
                                            fontSize: '0.75rem',
                                            color: 'var(--gray-500)'
                                        }}>
                                            <span>Status: {lead.status}</span>
                                            <span>{format(new Date(lead.created_at), 'MMM d, yyyy')}</span>
                                        </div>
                                    </div>
                                </Link>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Leads;

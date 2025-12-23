import { useState, useEffect } from 'react';
import Sidebar from '../components/Sidebar';
import api from '../utils/api';

function Dashboard() {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchStats();
    }, []);

    const fetchStats = async () => {
        try {
            const response = await api.get('/leads/stats/summary');
            setStats(response.data);
        } catch (error) {
            console.error('Error fetching stats:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex">
            <Sidebar />
            <div className="main-content">
                <div className="animate-slide-in">
                    <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
                    <p className="mb-4" style={{ color: 'var(--gray-400)' }}>
                        Welcome to LeadPilot AI - Your autonomous lead qualification system
                    </p>

                    {loading ? (
                        <div className="text-center mt-4">
                            <div className="gradient-text">Loading stats...</div>
                        </div>
                    ) : (
                        <>
                            {/* Stats Grid */}
                            <div className="grid grid-4 mb-4">
                                <div className="card">
                                    <div className="text-sm mb-2" style={{ color: 'var(--gray-400)' }}>
                                        Total Leads
                                    </div>
                                    <div className="text-3xl font-bold gradient-text">
                                        {stats?.total_leads || 0}
                                    </div>
                                </div>

                                <div className="card">
                                    <div className="text-sm mb-2" style={{ color: 'var(--gray-400)' }}>
                                        🔥 Hot Leads
                                    </div>
                                    <div className="text-3xl font-bold" style={{ color: 'var(--error)' }}>
                                        {stats?.hot_leads || 0}
                                    </div>
                                </div>

                                <div className="card">
                                    <div className="text-sm mb-2" style={{ color: 'var(--gray-400)' }}>
                                        ⚡ Warm Leads
                                    </div>
                                    <div className="text-3xl font-bold" style={{ color: 'var(--warning)' }}>
                                        {stats?.warm_leads || 0}
                                    </div>
                                </div>

                                <div className="card">
                                    <div className="text-sm mb-2" style={{ color: 'var(--gray-400)' }}>
                                        ❄️ Cold Leads
                                    </div>
                                    <div className="text-3xl font-bold" style={{ color: 'var(--info)' }}>
                                        {stats?.cold_leads || 0}
                                    </div>
                                </div>
                            </div>

                            {/* Quick Actions */}
                            <div className="card mb-4">
                                <h2 className="text-xl font-bold mb-3">Quick Actions</h2>
                                <div className="grid grid-3">
                                    <a href="/leads" className="btn btn-primary">
                                        👥 View All Leads
                                    </a>
                                    <a href="/knowledge-base" className="btn btn-secondary">
                                        📚 Manage Knowledge Base
                                    </a>
                                    <a href="/settings" className="btn btn-secondary">
                                        ⚙️ Configure Settings
                                    </a>
                                </div>
                            </div>

                            {/* Getting Started */}
                            <div className="card">
                                <h2 className="text-xl font-bold mb-3">Getting Started</h2>
                                <div style={{ color: 'var(--gray-700)', lineHeight: 1.8 }}>
                                    <p className="mb-2">
                                        <strong>1. Upload Knowledge Base:</strong> Add your business information, FAQs, and product details to the Knowledge Base.
                                    </p>
                                    <p className="mb-2">
                                        <strong>2. Configure Settings:</strong> Set up your lead qualification thresholds and notification preferences.
                                    </p>
                                    <p className="mb-2">
                                        <strong>3. Embed Widget:</strong> Copy the widget code from Settings and add it to your website.
                                    </p>
                                    <p>
                                        <strong>4. Monitor Leads:</strong> Watch as LeadPilot AI automatically qualifies and scores your leads!
                                    </p>
                                </div>
                            </div>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Dashboard;

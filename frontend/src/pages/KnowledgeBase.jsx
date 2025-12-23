import { useState, useEffect } from 'react';
import Sidebar from '../components/Sidebar';
import api from '../utils/api';

function KnowledgeBase() {
    const [documents, setDocuments] = useState([]);
    const [stats, setStats] = useState({ total_documents: 0, total_chunks: 0 });
    const [loading, setLoading] = useState(true);
    const [uploading, setUploading] = useState(false);
    const [formData, setFormData] = useState({ name: '', content: '' });

    useEffect(() => {
        fetchDocuments();
        fetchStats();
    }, []);

    const fetchDocuments = async () => {
        try {
            const response = await api.get('/knowledge-base/documents');
            setDocuments(response.data);
        } catch (error) {
            console.error('Error fetching documents:', error);
        } finally {
            setLoading(false);
        }
    };

    const fetchStats = async () => {
        try {
            const response = await api.get('/knowledge-base/stats');
            setStats(response.data);
        } catch (error) {
            console.error('Error fetching stats:', error);
        }
    };

    const handleUpload = async (e) => {
        e.preventDefault();
        setUploading(true);

        try {
            await api.post('/knowledge-base/upload', formData);
            setFormData({ name: '', content: '' });
            await fetchDocuments();
            await fetchStats();
            alert('Document uploaded successfully!');
        } catch (error) {
            console.error('Error uploading document:', error);
            alert('Failed to upload document');
        } finally {
            setUploading(false);
        }
    };

    const handleDelete = async (documentId) => {
        if (!confirm('Are you sure you want to delete this document?')) return;

        try {
            await api.delete(`/knowledge-base/documents/${documentId}`);
            await fetchDocuments();
        } catch (error) {
            console.error('Error deleting document:', error);
            alert('Failed to delete document');
        }
    };

    return (
        <div style={{ display: 'flex' }}>
            <Sidebar />
            <div style={{ marginLeft: '260px', flex: 1, padding: '2rem', minHeight: '100vh' }}>
                <div className="animate-slide-in">
                    <h1 className="text-3xl font-bold mb-2">Knowledge Base</h1>
                    <p style={{ color: 'var(--gray-400)', marginBottom: '2rem' }}>
                        Upload business information, FAQs, and product details for AI-powered responses
                    </p>

                    {/* Statistics Cards */}
                    <div className="grid" style={{ gap: '1rem', marginBottom: '2rem', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))' }}>
                        <div className="card" style={{ textAlign: 'center' }}>
                            <div style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>📚</div>
                            <div className="gradient-text" style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '0.25rem' }}>
                                {stats.total_documents}
                            </div>
                            <div style={{ color: 'var(--gray-400)', fontSize: '0.875rem' }}>
                                Total Documents
                            </div>
                        </div>
                        <div className="card" style={{ textAlign: 'center' }}>
                            <div style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>🧩</div>
                            <div className="gradient-text" style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '0.25rem' }}>
                                {stats.total_chunks}
                            </div>
                            <div style={{ color: 'var(--gray-400)', fontSize: '0.875rem' }}>
                                Knowledge Chunks
                            </div>
                        </div>
                    </div>

                    {/* Upload Form */}
                    <div className="card" style={{ marginBottom: '2rem' }}>
                        <h2 className="text-xl font-bold mb-3">Upload New Document</h2>
                        <form onSubmit={handleUpload}>
                            <div style={{ marginBottom: '1rem' }}>
                                <label style={{
                                    display: 'block',
                                    marginBottom: '0.5rem',
                                    fontSize: '0.875rem',
                                    fontWeight: 600,
                                    color: 'var(--gray-700)'
                                }}>
                                    Document Name
                                </label>
                                <input
                                    type="text"
                                    className="input"
                                    placeholder="e.g., Product FAQ, Pricing Information"
                                    value={formData.name}
                                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                    required
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
                                    Content
                                </label>
                                <textarea
                                    className="input"
                                    placeholder="Paste your document content here..."
                                    value={formData.content}
                                    onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                                    required
                                    rows={10}
                                    style={{ resize: 'vertical' }}
                                />
                            </div>

                            <button
                                type="submit"
                                className="btn btn-primary"
                                disabled={uploading}
                            >
                                {uploading ? '📤 Uploading...' : '📤 Upload Document'}
                            </button>
                        </form>
                    </div>

                    {/* Documents List */}
                    <div className="card">
                        <h2 className="text-xl font-bold mb-3">Uploaded Documents</h2>

                        {loading ? (
                            <div className="text-center">
                                <div className="gradient-text">Loading documents...</div>
                            </div>
                        ) : documents.length === 0 ? (
                            <div className="text-center" style={{ padding: '2rem', color: 'var(--gray-400)' }}>
                                <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📚</div>
                                <p>No documents uploaded yet</p>
                            </div>
                        ) : (
                            <div className="grid" style={{ gap: '1rem' }}>
                                {documents.map((doc) => (
                                    <div
                                        key={doc.document_id}
                                        style={{
                                            padding: '1rem',
                                            background: 'rgba(99, 102, 241, 0.1)',
                                            border: '1px solid rgba(99, 102, 241, 0.2)',
                                            borderRadius: 'var(--radius-md)',
                                            display: 'flex',
                                            justifyContent: 'space-between',
                                            alignItems: 'center'
                                        }}
                                    >
                                        <div>
                                            <h3 style={{ fontWeight: 600, marginBottom: '0.25rem' }}>
                                                📄 {doc.name}
                                            </h3>
                                            <p style={{ fontSize: '0.875rem', color: 'var(--gray-400)' }}>
                                                {doc.chunks_count} chunks • Uploaded {new Date(doc.created_at).toLocaleDateString()}
                                            </p>
                                        </div>
                                        <button
                                            onClick={() => handleDelete(doc.document_id)}
                                            style={{
                                                padding: '0.5rem 1rem',
                                                background: 'rgba(239, 68, 68, 0.1)',
                                                border: '1px solid var(--error)',
                                                borderRadius: 'var(--radius-md)',
                                                color: 'var(--error)',
                                                cursor: 'pointer',
                                                fontSize: '0.875rem',
                                                fontWeight: 600
                                            }}
                                        >
                                            🗑️ Delete
                                        </button>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default KnowledgeBase;

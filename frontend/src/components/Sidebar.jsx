import { Link, useLocation } from 'react-router-dom';

function Sidebar() {
    const location = useLocation();

    const menuItems = [
        { path: '/dashboard', icon: '📊', label: 'Dashboard' },
        { path: '/leads', icon: '👥', label: 'Leads' },
        { path: '/knowledge-base', icon: '📚', label: 'Knowledge Base' },
        { path: '/chat-test', icon: '💬', label: 'Chat Test' },
        { path: '/settings', icon: '⚙️', label: 'Settings' },
    ];

    const handleLogout = () => {
        localStorage.removeItem('token');
        window.location.href = '/login';
    };

    return (
        <div className="sidebar">
            {/* Logo */}
            <div className="p-4 mt-2">
                <h1 className="gradient-text text-xl font-bold">LeadPilot AI</h1>
                <p className="text-xs text-gray-400 mt-1" style={{ color: 'var(--gray-400)' }}>
                    Lead Qualification
                </p>
            </div>

            {/* Menu Items */}
            <nav className="flex-1 px-4" style={{ padding: '0 1rem' }}>
                {menuItems.map((item) => {
                    const isActive = location.pathname === item.path ||
                        (item.path === '/leads' && location.pathname.startsWith('/leads'));

                    return (
                        <Link
                            key={item.path}
                            to={item.path}
                            className={`sidebar-link ${isActive ? 'active' : ''}`}
                        >
                            <span className="text-xl">{item.icon}</span>
                            <span>{item.label}</span>
                        </Link>
                    );
                })}
            </nav>

            {/* Logout Button */}
            <div className="p-4">
                <button
                    onClick={handleLogout}
                    className="w-full p-3 rounded-md font-semibold transition-all duration-300 flex items-center justify-center gap-2"
                    style={{
                        background: 'rgba(239, 68, 68, 0.1)',
                        border: '1px solid var(--error)',
                        color: 'var(--error)',
                        cursor: 'pointer'
                    }}
                    onMouseEnter={(e) => {
                        e.currentTarget.style.background = 'var(--error)';
                        e.currentTarget.style.color = 'var(--gray-900)';
                    }}
                    onMouseLeave={(e) => {
                        e.currentTarget.style.background = 'rgba(239, 68, 68, 0.1)';
                        e.currentTarget.style.color = 'var(--error)';
                    }}
                >
                    🚪 Logout
                </button>
            </div>
        </div>
    );
}

export default Sidebar;

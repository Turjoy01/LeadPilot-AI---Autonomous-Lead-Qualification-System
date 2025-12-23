import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Leads from './pages/Leads';
import LeadDetail from './pages/LeadDetail';
import KnowledgeBase from './pages/KnowledgeBase';
import ChatTest from './pages/ChatTest';
import Settings from './pages/Settings';

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const token = localStorage.getItem('token');
        setIsAuthenticated(!!token);
        setLoading(false);
    }, []);

    if (loading) {
        return (
            <div style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                height: '100vh'
            }}>
                <div className="gradient-text text-2xl font-bold">Loading...</div>
            </div>
        );
    }

    return (
        <Router>
            <Routes>
                <Route
                    path="/login"
                    element={
                        isAuthenticated ? <Navigate to="/dashboard" /> : <Login setIsAuthenticated={setIsAuthenticated} />
                    }
                />
                <Route
                    path="/register"
                    element={
                        isAuthenticated ? <Navigate to="/dashboard" /> : <Register setIsAuthenticated={setIsAuthenticated} />
                    }
                />
                <Route
                    path="/dashboard"
                    element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />}
                />
                <Route
                    path="/leads"
                    element={isAuthenticated ? <Leads /> : <Navigate to="/login" />}
                />
                <Route
                    path="/leads/:id"
                    element={isAuthenticated ? <LeadDetail /> : <Navigate to="/login" />}
                />
                <Route
                    path="/knowledge-base"
                    element={isAuthenticated ? <KnowledgeBase /> : <Navigate to="/login" />}
                />
                <Route
                    path="/chat-test"
                    element={isAuthenticated ? <ChatTest /> : <Navigate to="/login" />}
                />
                <Route
                    path="/settings"
                    element={isAuthenticated ? <Settings /> : <Navigate to="/login" />}
                />
                <Route path="/" element={<Navigate to="/dashboard" />} />
            </Routes>
        </Router>
    );
}

export default App;

import { useCallback, useEffect, useMemo, useState } from 'react';
import LoginForm from './components/LoginForm.jsx';
import RegisterForm from './components/RegisterForm.jsx';
import UserArea from './components/UserArea.jsx';

const STORAGE_KEY = 'pbe_auth_state';

const createEmptyAuth = () => ({
  access: null,
  refresh: null,
  user: null,
  profile: null,
  groups: []
});

function loadStoredAuth() {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      return createEmptyAuth();
    }
    const parsed = JSON.parse(raw);
    if (!parsed?.access || !parsed?.user) {
      return createEmptyAuth();
    }
    return {
      ...createEmptyAuth(),
      ...parsed,
      access: parsed.access ?? null,
      refresh: parsed.refresh ?? null,
      user: parsed.user ?? null,
      profile: parsed.profile ?? null,
      groups: parsed.groups ?? []
    };
  } catch (_error) {
    return createEmptyAuth();
  }
}

export default function App() {
  const [auth, setAuth] = useState(() => loadStoredAuth());
  const [view, setView] = useState('login');

  const isAuthenticated = useMemo(() => Boolean(auth.access && auth.user), [auth.access, auth.user]);

  useEffect(() => {
    if (auth.access) {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(auth));
    } else {
      window.localStorage.removeItem(STORAGE_KEY);
    }
  }, [auth]);

  useEffect(() => {
    if (!isAuthenticated) {
      setView('login');
    }
  }, [isAuthenticated]);

  const handleAuthSuccess = useCallback((payload) => {
    setAuth({
      access: payload.access ?? null,
      refresh: payload.refresh ?? null,
      user: payload.user ?? null,
      profile: payload.profile ?? null,
      groups: payload.groups ?? []
    });
  }, []);

  const handleProfileUpdate = useCallback((profile) => {
    setAuth((prev) => ({
      ...prev,
      profile
    }));
  }, []);

  const handleLogout = useCallback(() => {
    setAuth(createEmptyAuth());
  }, []);

  return (
    <div className="app-shell">
      <div className="card">
        {isAuthenticated ? (
          <UserArea auth={auth} onProfileUpdate={handleProfileUpdate} onLogout={handleLogout} />
        ) : view === 'login' ? (
          <LoginForm onSuccess={handleAuthSuccess} onSwitchToRegister={() => setView('register')} />
        ) : (
          <RegisterForm onSuccess={handleAuthSuccess} onSwitchToLogin={() => setView('login')} />
        )}
      </div>
      <footer className="app-footer">
        <p>
          Portal desenvolvido com Django (API) e React (UI). Utilize o servidor Django em <code>localhost:8000</code> e
          rode <code>npm run dev</code> na pasta <code>Streaming/frontend</code> para iniciar a interface.
        </p>
      </footer>
    </div>
  );
}

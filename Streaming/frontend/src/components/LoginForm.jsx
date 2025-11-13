import { useState } from 'react';
import { login } from '../api/auth.js';

const initialForm = {
  username: '',
  password: ''
};

export default function LoginForm({ onSuccess, onSwitchToRegister }) {
  const [form, setForm] = useState(initialForm);
  const [status, setStatus] = useState({ loading: false, error: '' });

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setStatus({ loading: true, error: '' });

    try {
      const payload = await login(form);
      onSuccess(payload);
      setForm(initialForm);
    } catch (error) {
      setStatus({ loading: false, error: error.message });
      return;
    }

    setStatus({ loading: false, error: '' });
  };

  return (
    <div className="card-body">
      <h2 className="card-title">Entrar</h2>
      <p className="card-subtitle">Use seu usuário e senha cadastrados.</p>
      <form onSubmit={handleSubmit} className="form">
        <label className="form-label" htmlFor="username">Usuário</label>
        <input
          id="username"
          name="username"
          type="text"
          autoComplete="username"
          required
          value={form.username}
          onChange={handleChange}
          className="form-input"
        />

        <label className="form-label" htmlFor="password">Senha</label>
        <input
          id="password"
          name="password"
          type="password"
          autoComplete="current-password"
          required
          value={form.password}
          onChange={handleChange}
          className="form-input"
        />

        {status.error && <p className="form-error">{status.error}</p>}

        <button disabled={status.loading} type="submit" className="form-button">
          {status.loading ? 'Entrando...' : 'Entrar'}
        </button>

        <button
          type="button"
          className="secondary-button full-width"
          onClick={onSwitchToRegister}
        >
          Quero me cadastrar
        </button>
      </form>
      <p className="form-footer">Ainda não tem conta? Clique em “Quero me cadastrar”.</p>
    </div>
  );
}

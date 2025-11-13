import { useState } from 'react';
import { registerUser } from '../api/auth.js';

const initialForm = {
  username: '',
  email: '',
  password: '',
  first_name: ''
};

export default function RegisterForm({ onSuccess, onSwitchToLogin }) {
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
      const payload = await registerUser(form);
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
      <h2 className="card-title">Criar conta</h2>
      <p className="card-subtitle">Cadastre-se para acessar vagas e atualizar seu perfil.</p>
      <form onSubmit={handleSubmit} className="form">
        <label className="form-label" htmlFor="first_name">Nome</label>
        <input
          id="first_name"
          name="first_name"
          type="text"
          value={form.first_name}
          onChange={handleChange}
          className="form-input"
          placeholder="Como devemos te chamar"
        />

        <label className="form-label" htmlFor="username">Usuário</label>
        <input
          id="username"
          name="username"
          type="text"
          required
          value={form.username}
          onChange={handleChange}
          className="form-input"
          autoComplete="username"
        />

        <label className="form-label" htmlFor="email">E-mail</label>
        <input
          id="email"
          name="email"
          type="email"
          required
          value={form.email}
          onChange={handleChange}
          className="form-input"
          autoComplete="email"
        />

        <label className="form-label" htmlFor="password">Senha</label>
        <input
          id="password"
          name="password"
          type="password"
          required
          value={form.password}
          onChange={handleChange}
          className="form-input"
          autoComplete="new-password"
        />

        {status.error && <p className="form-error">{status.error}</p>}

        <button disabled={status.loading} type="submit" className="form-button">
          {status.loading ? 'Criando...' : 'Criar conta'}
        </button>
      </form>
      <p className="form-footer">
        Já tem cadastro?{' '}
        <button type="button" className="link-button" onClick={onSwitchToLogin}>
          Fazer login
        </button>
      </p>
    </div>
  );
}

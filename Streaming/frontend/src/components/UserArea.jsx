import { useEffect, useMemo, useState } from 'react';
import { fetchProfile, updateProfile } from '../api/auth.js';

const initialStatus = { loading: false, error: '', success: '' };

export default function UserArea({ auth, onProfileUpdate, onLogout }) {
  const [profile, setProfile] = useState(auth.profile);
  const [form, setForm] = useState({ nome: auth.profile?.nome || '', curriculo: null });
  const [status, setStatus] = useState(initialStatus);

  const firstName = useMemo(() => {
    return profile?.nome || auth.user?.first_name || auth.user?.username;
  }, [profile, auth.user]);

  useEffect(() => {
    setProfile(auth.profile);
    setForm((prev) => ({ ...prev, nome: auth.profile?.nome || '' }));
  }, [auth.profile]);

  useEffect(() => {
    let active = true;
    if (!auth.access || auth.profile) {
      return () => {
        active = false;
      };
    }

    async function loadProfile() {
      setStatus(initialStatus);
      try {
        const data = await fetchProfile(auth.access);
        if (!active) {
          return;
        }
        setProfile(data);
        setForm((prev) => ({ ...prev, nome: data?.nome || '' }));
        onProfileUpdate(data);
      } catch (error) {
        if (!active) {
          return;
        }
        setStatus({ loading: false, error: error.message, success: '' });
      }
    }

    loadProfile();
    return () => {
      active = false;
    };
  }, [auth.access, auth.profile, onProfileUpdate]);

  const handleChange = (event) => {
    const { name, value, files } = event.target;
    if (name === 'curriculo' && files) {
      const [file] = files;
      if (file && file.type !== 'application/pdf') {
        setStatus({ loading: false, error: 'Envie apenas arquivos PDF.', success: '' });
        return;
      }
      setForm((prev) => ({ ...prev, curriculo: file || null }));
      return;
    }
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setStatus({ loading: true, error: '', success: '' });

    try {
      const updatedProfile = await updateProfile(auth.access, {
        nome: form.nome,
        curriculo: form.curriculo
      });
      setProfile(updatedProfile);
      onProfileUpdate(updatedProfile);
      setForm((prev) => ({ ...prev, curriculo: null }));
      setStatus({ loading: false, error: '', success: 'Perfil atualizado com sucesso.' });
    } catch (error) {
      setStatus({ loading: false, error: error.message, success: '' });
    }
  };

  return (
    <div className="card-body">
      <div className="card-header">
        <div>
          <h2 className="card-title">Olá, {firstName}!</h2>
          <p className="card-subtitle">Mantenha seus dados atualizados para participar das seleções.</p>
        </div>
        <button type="button" className="secondary-button" onClick={onLogout}>
          Sair
        </button>
      </div>

      <section className="profile-section">
        <h3>Dados básicos</h3>
        <form onSubmit={handleSubmit} className="form profile-form">
          <label className="form-label" htmlFor="nome">Nome preferido</label>
          <input
            id="nome"
            name="nome"
            type="text"
            value={form.nome}
            onChange={handleChange}
            className="form-input"
            placeholder="Como devemos te chamar"
          />

          <label className="form-label" htmlFor="curriculo">Currículo (PDF)</label>
          <input
            id="curriculo"
            name="curriculo"
            type="file"
            accept="application/pdf"
            onChange={handleChange}
            className="form-input"
          />
          <p className="hint">O arquivo deve estar em formato PDF e pode ter até 5 MB.</p>

          {profile?.curriculo_pdf && (
            <p className="form-info">
              Currículo enviado:{' '}
              <a href={profile.curriculo_pdf} target="_blank" rel="noreferrer">
                Abrir arquivo
              </a>
            </p>
          )}

          {status.error && <p className="form-error">{status.error}</p>}
          {status.success && <p className="form-success">{status.success}</p>}

          <button disabled={status.loading} type="submit" className="form-button">
            {status.loading ? 'Salvando...' : 'Salvar alterações'}
          </button>
        </form>
      </section>
    </div>
  );
}

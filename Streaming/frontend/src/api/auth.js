const API_BASE = '/api';

async function handleResponse(response) {
  const contentType = response.headers.get('content-type') || '';
  const isJson = contentType.includes('application/json');
  const payload = isJson ? await response.json() : null;

  if (!response.ok) {
    const detail = payload?.detail || payload?.error;
    const nonField = Array.isArray(payload?.non_field_errors) ? payload.non_field_errors.join(' ') : null;
    const message = detail || nonField || 'Não foi possível completar a solicitação.';
    throw new Error(message);
  }

  return payload;
}

export async function login(credentials) {
  const response = await fetch(`${API_BASE}/auth/login/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(credentials)
  });
  return handleResponse(response);
}

export async function registerUser(payload) {
  const response = await fetch(`${API_BASE}/auth/register/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });
  return handleResponse(response);
}

export async function fetchProfile(token) {
  const response = await fetch(`${API_BASE}/me/profile/`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  return handleResponse(response);
}

export async function updateProfile(token, data) {
  const formData = new FormData();
  if (data.nome !== undefined) {
    formData.append('nome', data.nome);
  }
  if (data.curriculo instanceof File) {
    formData.append('curriculo_pdf', data.curriculo);
  }
  const response = await fetch(`${API_BASE}/me/profile/`, {
    method: 'PATCH',
    headers: {
      Authorization: `Bearer ${token}`
    },
    body: formData
  });
  return handleResponse(response);
}

<template>
  <div class="profile-container animate-fade-in">
    <div class="profile-card">
      <div class="profile-header">
        <div class="avatar-container">
          <User :size="48" class="avatar-icon" />
        </div>
        <h1>Mi Perfil</h1>
        <p>Gestiona tus datos biométricos y preferencias de entrenamiento</p>
      </div>

      <form @submit.prevent="handleUpdate" class="profile-form">
        <!-- Datos Personales -->
        <h3 class="section-title">Datos Personales</h3>
        <div class="form-grid">
          <div class="input-group">
            <label>Nombre Completo</label>
            <input v-model="profile.name" type="text" placeholder="Tu nombre" />
          </div>
          <div class="input-group">
            <label>Nickname</label>
            <input v-model="profile.nickname" type="text" placeholder="Tu apodo" />
          </div>
          <div class="input-group full-width">
            <label>Correo Electrónico</label>
            <input v-model="profile.email" type="email" placeholder="email@ejemplo.com" />
          </div>
        </div>

        <!-- Datos Fitness -->
        <h3 class="section-title">Datos Fitness</h3>
        <div class="form-grid">
          <div class="input-group">
            <label>Peso (kg)</label>
            <input v-model="profile.weight" type="number" step="0.1" required />
          </div>
          <div class="input-group">
            <label>Altura (cm)</label>
            <input v-model="profile.height" type="number" required />
          </div>
          <div class="input-group">
            <label>Días por semana</label>
            <select v-model="profile.days_per_week">
              <option v-for="n in 7" :key="n" :value="n">{{ n }} días</option>
            </select>
          </div>
          <div class="input-group">
            <label>Minutos por sesión</label>
            <input v-model="profile.time_per_session" type="number" />
          </div>
          <div class="input-group full-width">
            <label>Objetivo Fitness</label>
            <select v-model="profile.fitness_goal">
              <option value="Hypertrophy">Hipertrofia (Ganar músculo)</option>
              <option value="Weight Loss">Pérdida de peso</option>
              <option value="Strength">Fuerza</option>
              <option value="Endurance">Resistencia / Cardio</option>
            </select>
          </div>
          <div class="input-group full-width">
            <label>Nivel de experiencia</label>
            <select v-model="profile.experience_level">
              <option value="Beginner">Principiante</option>
              <option value="Intermediate">Intermedio</option>
              <option value="Advanced">Avanzado</option>
            </select>
          </div>
        </div>

        <!-- Adicional -->
        <h3 class="section-title">Información Adicional</h3>
        <div class="form-grid">
          <div class="input-group">
            <label>País</label>
            <input v-model="profile.country" type="text" />
          </div>
          <div class="input-group">
            <label>Teléfono</label>
            <input v-model="profile.phone" type="text" />
          </div>
          <div class="input-group full-width">
            <label>Biografía</label>
            <textarea v-model="profile.bio" placeholder="Cuéntanos sobre tus metas..."></textarea>
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-primary" :disabled="loading">
            <Save :size="20" v-if="!loading" />
            <span>{{ loading ? 'Actualizando...' : 'Guardar Cambios' }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { User, Save } from 'lucide-vue-next';

import api from '../services/api';
import { useAuthStore } from '../stores/auth';
import { useNotificationStore } from '../stores/notification';


const authStore = useAuthStore();
const notificationStore = useNotificationStore();
const router = useRouter();

const loading = ref(false);


const profile = ref({
  name: '',
  nickname: '',
  email: '',
  weight: 0,
  height: 0,
  days_per_week: 3,
  time_per_session: 60,
  fitness_goal: 'Hypertrophy',
  experience_level: 'Beginner',
  country: '',
  phone: '',
  bio: '',
  address: ''
});

onMounted(async () => {
  try {
    const res = await api.get('/profile/');
    Object.assign(profile.value, res.data);
  } catch (err) {
    console.error("Error loading profile", err);
  }
});

const handleUpdate = async () => {
  loading.value = true;
  try {
    await api.put('/profile/', profile.value);
    authStore.user = { ...authStore.user, ...profile.value };
    notificationStore.addToast("¡Perfil actualizado con éxito!", "success");
    router.push('/');
  } catch (err) {
    notificationStore.addToast("Error al actualizar el perfil. Revisa los datos.", "error");
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.profile-container {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.profile-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 24px;
  padding: 2.5rem;
  box-shadow: 0 20px 50px rgba(0,0,0,0.2);
}

.profile-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.avatar-container {
  width: 80px;
  height: 80px;
  background: var(--glass);
  border: 2px solid var(--primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
}

.avatar-icon {
  color: var(--primary);
}

.profile-header h1 {
  font-size: 2.2rem;
  margin-bottom: 0.5rem;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--primary);
  margin-top: 2rem;
  margin-bottom: 1.2rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--glass);
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.2rem;
}

.full-width {
  grid-column: span 2;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.input-group label {
  font-size: 0.85rem;
  color: var(--text-muted);
  font-weight: 500;
}

input, select, textarea {
  background: rgba(15, 23, 42, 0.4);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 0.7rem 1rem;
  color: white;
  transition: all 0.2s;
}

textarea {
  min-height: 80px;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.form-actions {
  margin-top: 3rem;
  display: flex;
  justify-content: center;
}

.btn-primary {
  background: var(--primary);
  color: white;
  border: none;
  padding: 1rem 2.5rem;
  border-radius: 12px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background: var(--primary-hover);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 640px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  .full-width {
    grid-column: span 1;
  }
}
</style>

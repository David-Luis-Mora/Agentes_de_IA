<template>
  <div class="setup-container animate-fade-in">
    <div class="setup-card">
      <div class="setup-header">
        <h1>{{ step === 1 ? 'Tu Perfil Fitness' : 'Información Opcional' }}</h1>
        <p>{{ step === 1 ? 'Cuéntanos sobre ti para que el Coach pueda personalizar tu entrenamiento.' : 'Completa tu perfil para una mejor experiencia (puedes saltar esto).' }}</p>
        
        <div class="progress-bar">
          <div class="progress" :style="{ width: step === 1 ? '50%' : '100%' }"></div>
        </div>
      </div>

      <form @submit.prevent="handleSubmit">
        <!-- Step 1: Fitness Data -->
        <div v-if="step === 1" class="form-grid">
          <div class="input-group">
            <label>Peso (kg)</label>
            <input v-model="profile.weight" type="number" step="0.1" required placeholder="Ej: 75.5" />
          </div>
          <div class="input-group">
            <label>Altura (cm)</label>
            <input v-model="profile.height" type="number" required placeholder="Ej: 180" />
          </div>
          <div class="input-group">
            <label>Días por semana</label>
            <select v-model="profile.days_per_week">
              <option v-for="n in 7" :key="n" :value="n">{{ n }} días</option>
            </select>
          </div>
          <div class="input-group">
            <label>Minutos por sesión</label>
            <input v-model="profile.time_per_session" type="number" placeholder="Ej: 60" />
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

        <!-- Step 2: Extra Data -->
        <div v-if="step === 2" class="form-grid">
          <div class="input-group">
            <label>País</label>
            <input v-model="profile.country" type="text" placeholder="Ej: España" />
          </div>
          <div class="input-group">
            <label>Teléfono</label>
            <input v-model="profile.phone" type="text" placeholder="Ej: +34..." />
          </div>
          <div class="input-group full-width">
            <label>Biografía</label>
            <textarea v-model="profile.bio" placeholder="Cuéntanos un poco sobre ti..."></textarea>
          </div>
          <div class="input-group full-width">
            <label>Dirección</label>
            <input v-model="profile.address" type="text" placeholder="Tu dirección" />
          </div>
        </div>

        <div class="setup-actions">
          <button v-if="step === 2" type="button" class="btn-secondary" @click="step = 1">
            Atrás
          </button>
          <button type="submit" class="btn-primary" :disabled="loading">
            {{ loading ? 'Guardando...' : (step === 1 ? 'Siguiente' : 'Finalizar') }}
          </button>
          <button v-if="step === 2" type="button" class="btn-skip" @click="finish">
            Saltar y finalizar
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import api from '../services/api';

const router = useRouter();
const authStore = useAuthStore();
const step = ref(1);
const loading = ref(false);

const profile = ref({
  weight: null,
  height: null,
  days_per_week: 3,
  time_per_session: 60,
  fitness_goal: 'Hypertrophy',
  experience_level: 'Beginner',
  country: '',
  phone: '',
  bio: '',
  address: '',
  balance: 0
});

onMounted(async () => {
  try {
    const res = await api.get('/profile/');
    // Fill current data if exists
    Object.assign(profile.value, res.data);
  } catch (err) {
    console.error("Error fetching profile:", err);
  }
});

const handleSubmit = async () => {
  if (step.value === 1) {
    step.value = 2;
    window.scrollTo(0, 0);
  } else {
    await finish();
  }
};

const finish = async () => {
  loading.value = true;
  try {
    const res = await api.put('/profile/', profile.value);
    // Update the store so the router knows the profile is no longer "new"
    authStore.user = { ...authStore.user, ...profile.value };
    router.push('/');
  } catch (err) {
    alert("Error al guardar el perfil");
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.setup-container {
  min-height: calc(100vh - 70px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.setup-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 24px;
  padding: 3rem;
  width: 100%;
  max-width: 600px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
}

.setup-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.setup-header h1 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.setup-header p {
  color: var(--text-muted);
}

.progress-bar {
  height: 6px;
  background: var(--glass);
  border-radius: 3px;
  margin-top: 1.5rem;
  overflow: hidden;
}

.progress {
  height: 100%;
  background: var(--primary);
  transition: width 0.3s ease;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

.full-width {
  grid-column: span 2;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.input-group label {
  font-size: 0.9rem;
  color: var(--text-main);
  font-weight: 500;
}

input, select, textarea {
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 0.75rem 1rem;
  color: white;
  font-size: 1rem;
  transition: all 0.2s;
}

textarea {
  min-height: 100px;
  resize: vertical;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
}

.setup-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  align-items: center;
}

.btn-primary {
  background: var(--primary);
  color: white;
  border: none;
  padding: 0.85rem 2rem;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text-main);
  padding: 0.85rem 2rem;
  border-radius: 12px;
  cursor: pointer;
}

.btn-skip {
  background: transparent;
  border: none;
  color: var(--text-muted);
  text-decoration: underline;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-primary:hover {
  background: var(--primary-hover);
  transform: translateY(-2px);
}
</style>

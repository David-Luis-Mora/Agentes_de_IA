<template>
  <div class="routine-page animate-fade-in">
    <div class="header">
      <h1>Mi Calendario de <span class="highlight">Entrenamiento</span></h1>
      <p>Selecciona un día para ver tu rutina programada.</p>
    </div>

    <!-- Weekly Calendar Selector -->
    <div class="calendar-wrapper">
      <div class="calendar-container">
        <div 
          v-for="(day, index) in days" 
          :key="index"
          class="day-card"
          :class="{ active: selectedDay === index, 'has-routine': routines[index] }"
          @click="selectedDay = index"
        >
          <span class="day-name">{{ day.short }}</span>
          <div class="day-indicator">
            <div v-if="routines[index]" class="routine-dot"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Routine Details Content -->
    <Transition name="slide-up" mode="out-in">
      <div :key="selectedDay" class="routine-content">
        <div v-if="currentRoutine" class="routine-details">
          <div class="routine-header">
            <div class="title-group">
              <span class="day-badge">{{ days[selectedDay].label }}</span>
              <h2>{{ currentRoutine.name || 'Rutina Programada' }}</h2>
            </div>
            <div class="stats-badge">
              {{ currentRoutine.exercises.length }} Ejercicios
            </div>
          </div>

          <div class="exercises-grid">
            <div 
              v-for="(ex, idx) in currentRoutine.exercises" 
              :key="idx" 
              class="exercise-summary-card"
              @click="goToExercise(ex.id)"
            >
              <div class="card-left">
                <div class="image-box">
                  <img v-if="ex.image_url" :src="ex.image_url" :alt="ex.name" class="fit-image" />
                  <div v-else class="img-placeholder"><Dumbbell :size="24" /></div>
                </div>
              </div>
              <div class="card-center">
                <h3>{{ ex.name }}</h3>
                <div class="card-meta">
                  <span class="series-count">{{ ex.sets?.length || 0 }} Series</span>
                  <span v-if="ex.primary_muscle" class="muscle-tag">{{ ex.primary_muscle }}</span>
                </div>
              </div>
              <div class="card-right">
                <ChevronRight :size="20" />
              </div>
            </div>
          </div>
        </div>

        <div v-else class="no-routine">
          <div class="empty-state">
            <div class="icon-circle">
              <CalendarX :size="40" />
            </div>
            <h3>Día de Descanso</h3>
            <p>No tienes una rutina guardada para este día.</p>
            <router-link to="/" class="btn-chat">
              Hablar con GymAI
            </router-link>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { Dumbbell, CalendarX, ChevronRight } from 'lucide-vue-next';
import api from '../services/api';

const router = useRouter();
const days = [
  { short: 'LUN', label: 'Lunes' },
  { short: 'MAR', label: 'Martes' },
  { short: 'MIE', label: 'Miércoles' },
  { short: 'JUE', label: 'Jueves' },
  { short: 'VIE', label: 'Viernes' },
  { short: 'SAB', label: 'Sábado' },
  { short: 'DOM', label: 'Domingo' }
];

const today = new Date().getDay();
const selectedDay = ref(today === 0 ? 6 : today - 1);
const routines = ref({});

const currentRoutine = computed(() => routines.value[selectedDay.value]);

const goToExercise = (id) => {
  router.push(`/exercise/${id}`);
};

onMounted(async () => {
  try {
    const response = await api.get('/routines/');
    routines.value = response.data;
  } catch (error) {
    console.error('Error fetching routines:', error);
  }
});
</script>

<style scoped>
.routine-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
}

.header { text-align: center; margin-bottom: 2.5rem; }
.header h1 { font-size: 2.5rem; font-weight: 800; }
.highlight { color: var(--primary); }

.calendar-wrapper {
  background: var(--glass);
  padding: 1rem;
  border-radius: 20px;
  border: 1px solid var(--border);
  margin-bottom: 2.5rem;
}

.calendar-container {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0.5rem;
}

.day-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem 0.5rem;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.day-card.active {
  background: var(--primary);
  color: white;
}

.day-name { font-size: 0.8rem; font-weight: 700; }

.routine-dot {
  width: 6px;
  height: 6px;
  background: var(--primary);
  border-radius: 50%;
  margin-top: 4px;
}
.day-card.active .routine-dot { background: white; }

.routine-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 2rem;
  border-bottom: 1px solid var(--border);
  padding-bottom: 1rem;
}

.day-badge {
  background: rgba(99, 102, 241, 0.1);
  color: var(--primary);
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.exercises-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.exercise-summary-card {
  display: flex;
  align-items: center;
  background: var(--glass);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.exercise-summary-card:hover {
  border-color: var(--primary);
  transform: translateX(5px);
  background: rgba(255,255,255,0.03);
}

.card-left {
  margin-right: 1.25rem;
}

.image-box {
  width: 70px;
  height: 70px;
  border-radius: 12px;
  overflow: hidden;
  background: #000;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--border);
}

.fit-image {
  width: 100%;
  height: 100%;
  object-fit: cover; /* can be 'contain' if the user prefers, let's try cover with aspect ratio */
}

.card-center {
  flex: 1;
}

.card-center h3 {
  font-size: 1.1rem;
  margin-bottom: 0.3rem;
}

.card-meta {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.series-count {
  font-size: 0.85rem;
  color: var(--primary);
  font-weight: 600;
}

.muscle-tag {
  font-size: 0.75rem;
  background: rgba(255,255,255,0.05);
  padding: 0.1rem 0.5rem;
  border-radius: 4px;
  color: var(--text-muted);
}

.card-right {
  color: var(--text-muted);
}

.no-routine { text-align: center; padding: 3rem; }
.btn-chat {
  display: inline-block;
  margin-top: 1rem;
  background: var(--primary);
  color: white;
  padding: 0.6rem 1.5rem;
  border-radius: 8px;
  text-decoration: none;
}
</style>

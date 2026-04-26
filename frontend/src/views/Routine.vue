<template>
  <div class="routine-page animate-fade-in">
    <div class="header">
      <h1>Mi Calendario de <span class="highlight">Entrenamiento</span></h1>
      <p>Selecciona un día para ver tu rutina programada y los ejercicios correspondientes.</p>
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
            <div v-for="(ex, idx) in currentRoutine.exercises" :key="idx" class="exercise-card">
              <div class="exercise-number">{{ idx + 1 }}</div>
              <div class="exercise-body">
                <div class="exercise-text">
                  <h3>{{ ex.name }}</h3>
                  <p v-if="ex.description" class="description" v-html="ex.description"></p>
                </div>
                
                <div v-if="ex.video_url" class="exercise-media">
                  <div class="video-container">
                    <video 
                      v-if="isVideo(ex.video_url)" 
                      controls 
                      class="exercise-video"
                      preload="metadata"
                    >
                      <source :src="ex.video_url" type="video/mp4">
                      Tu navegador no soporta videos.
                    </video>
                    <a v-else :href="ex.video_url" target="_blank" class="external-video-btn">
                      <Play :size="18" />
                      <span>Ver Video Demostrativo</span>
                    </a>
                  </div>
                </div>
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
            <p>No tienes una rutina guardada para este día. ¡Aprovecha para recuperar energías!</p>
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
import { Play, CalendarX } from 'lucide-vue-next';
import api from '../services/api';

const days = [
  { short: 'LUN', label: 'Lunes' },
  { short: 'MAR', label: 'Martes' },
  { short: 'MIE', label: 'Miércoles' },
  { short: 'JUE', label: 'Jueves' },
  { short: 'VIE', label: 'Viernes' },
  { short: 'SAB', label: 'Sábado' },
  { short: 'DOM', label: 'Domingo' }
];

// Default to current day (0=Monday in our array, getDay() 0=Sunday)
const today = new Date().getDay();
const selectedDay = ref(today === 0 ? 6 : today - 1);
const routines = ref({});

const currentRoutine = computed(() => routines.value[selectedDay.value]);

const isVideo = (url) => {
  if (!url) return false;
  return url.toLowerCase().endsWith('.mp4') || url.includes('wger-static');
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
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
  min-height: calc(100vh - 70px);
}

.header {
  text-align: center;
  margin-bottom: 3rem;
}

.header h1 {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
  letter-spacing: -1px;
}

.highlight {
  color: var(--primary);
  background: linear-gradient(120deg, var(--primary), #818cf8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.header p {
  color: var(--text-muted);
  font-size: 1.1rem;
}

/* Calendar Selector */
.calendar-wrapper {
  background: var(--glass);
  padding: 1rem;
  border-radius: 20px;
  border: 1px solid var(--border);
  margin-bottom: 3rem;
  box-shadow: var(--shadow-sm);
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
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.day-card:hover {
  background: rgba(255, 255, 255, 0.05);
  transform: translateY(-2px);
}

.day-card.active {
  background: var(--primary);
  color: white;
  box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3);
}

.day-name {
  font-size: 0.8rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  opacity: 0.8;
}

.day-indicator {
  height: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.routine-dot {
  width: 6px;
  height: 6px;
  background: var(--primary);
  border-radius: 50%;
}

.day-card.active .routine-dot {
  background: white;
}

/* Routine Content */
.routine-content {
  min-height: 400px;
}

.routine-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--border);
}

.day-badge {
  background: rgba(99, 102, 241, 0.1);
  color: var(--primary);
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  display: inline-block;
}

.routine-header h2 {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
}

.stats-badge {
  background: var(--surface);
  padding: 0.5rem 1rem;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-muted);
  border: 1px solid var(--border);
}

/* Exercises */
.exercises-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.exercise-card {
  background: var(--glass);
  border-radius: 20px;
  border: 1px solid var(--border);
  overflow: hidden;
  display: flex;
  transition: transform 0.2s;
}

.exercise-card:hover {
  transform: scale(1.01);
}

.exercise-number {
  background: var(--primary);
  color: white;
  width: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 1.2rem;
}

.exercise-body {
  flex: 1;
  padding: 1.5rem;
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 2rem;
}

.exercise-text h3 {
  font-size: 1.3rem;
  margin-bottom: 0.75rem;
  color: var(--text-main);
}

.description {
  color: var(--text-muted);
  line-height: 1.6;
  font-size: 0.95rem;
}

.video-container {
  width: 100%;
  aspect-ratio: 16/9;
  background: #000;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.exercise-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.external-video-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  color: white;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9rem;
  transition: opacity 0.2s;
}

.external-video-btn:hover {
  opacity: 0.8;
}

/* Empty State */
.no-routine {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 4rem 0;
}

.empty-state {
  text-align: center;
  max-width: 400px;
}

.icon-circle {
  width: 80px;
  height: 80px;
  background: var(--surface);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  color: var(--text-muted);
  border: 1px solid var(--border);
}

.empty-state h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.empty-state p {
  color: var(--text-muted);
  margin-bottom: 2rem;
}

.btn-chat {
  display: inline-block;
  background: var(--primary);
  color: white;
  padding: 0.8rem 2rem;
  border-radius: 12px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-chat:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(99, 102, 241, 0.4);
}

@media (max-width: 768px) {
  .exercise-body {
    grid-template-columns: 1fr;
  }
  .calendar-container {
    gap: 0.25rem;
  }
  .day-name {
    font-size: 0.7rem;
  }
}

/* Animations */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease-out;
}

.slide-up-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.slide-up-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>

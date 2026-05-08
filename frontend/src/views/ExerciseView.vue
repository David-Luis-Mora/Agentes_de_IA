<template>
  <div class="exercise-detail-page animate-fade-in" v-if="exercise">
    <div class="top-nav">
      <button @click="router.back()" class="back-btn">
        <ArrowLeft :size="20" />
        <span>Volver a la rutina</span>
      </button>
    </div>

    <div class="exercise-card-container">
      <!-- Main Collapsible Section -->
      <div class="exercise-expandable-card">
        <div class="card-header-row">
          <div class="header-left">
            <div class="image-container">
              <img v-if="exercise.image_url" :src="exercise.image_url" :alt="exercise.name" class="main-img" />
              <div v-else class="img-placeholder"><Dumbbell :size="32" /></div>
            </div>
            <div class="title-section">
              <h1 @click="showModal = true" class="clickable-title">{{ exercise.name }}</h1>
              <p class="subtitle">{{ exercise.category || 'Ejercicio' }} • {{ exercise.sets?.length || 0 }} Series</p>
            </div>
          </div>
          <button class="toggle-btn" @click="isExpanded = !isExpanded">
            <component :is="isExpanded ? ChevronUp : ChevronDown" :size="28" />
          </button>
        </div>

        <Transition name="expand">
          <div v-if="isExpanded" class="sets-content">
            <div class="sets-table">
              <div class="table-header">
                <span>#</span>
                <span>Peso (kg)</span>
                <span>Reps</span>
                <span>Completado</span>
              </div>
              <div v-for="(set, index) in exercise.sets" :key="index" class="set-row">
                <span class="set-index">{{ index + 1 }}</span>
                <span class="set-weight">{{ set.weight }} kg</span>
                <span class="set-reps">{{ set.reps }}</span>
                <div class="check-box">
                  <input type="checkbox" />
                </div>
              </div>
              <div v-if="!exercise.sets || !exercise.sets.length" class="empty-sets">
                No hay series especificadas para este ejercicio.
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </div>

    <!-- Details Modal -->
    <Transition name="fade">
      <div v-if="showModal" class="modal-overlay" @click="showModal = false">
        <div class="modal-content animate-pop" @click.stop>
          <button class="close-modal" @click="showModal = false"><X :size="24" /></button>
          
          <div class="modal-header">
            <h2>{{ exercise.name }}</h2>
            <div class="muscle-tags">
              <div class="m-tag"><small>Primario:</small> {{ exercise.primary_muscle || 'N/A' }}</div>
              <div class="m-tag"><small>Secundario:</small> {{ exercise.secondary_muscle || 'N/A' }}</div>
              <div class="m-tag"><small>Categoría:</small> {{ exercise.category || 'N/A' }}</div>
            </div>
          </div>

          <div class="modal-body">
            <div v-if="exercise.video_url" class="video-section">
              <h3>Guía de ejecución</h3>
              <div class="video-wrapper">
                <video controls preload="metadata" class="detail-video">
                  <source :src="exercise.video_url" type="video/mp4">
                  Tu navegador no soporta video.
                </video>
              </div>
            </div>

            <div class="instructions-section">
              <h3>Instrucciones paso a paso</h3>
              <div class="instructions-box" v-html="formattedInstructions"></div>
            </div>
          </div>

          <div class="modal-footer">
            <button class="ok-btn" @click="showModal = false">¡Entendido!</button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
  <div v-else-if="loading" class="loading-state">
    <div class="spinner"></div>
    <p>Cargando detalles del ejercicio...</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { 
  ArrowLeft, 
  Dumbbell, 
  ChevronDown, 
  ChevronUp, 
  X 
} from 'lucide-vue-next';
import api from '../services/api';

const route = useRoute();
const router = useRouter();

const exercise = ref(null);
const loading = ref(true);
const isExpanded = ref(true);
const showModal = ref(false);

const formattedInstructions = computed(() => {
  const text = exercise.value?.instructions || exercise.value?.description;
  if (!text) return 'Sin instrucciones disponibles.';
  return text.replace(/\n/g, '<br>');
});

onMounted(async () => {
  try {
    const res = await api.get(`/exercise/${route.params.id}/`);
    exercise.value = res.data;
  } catch (err) {
    console.error("Error fetching exercise details:", err);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.exercise-detail-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.top-nav {
  margin-bottom: 2rem;
}

.back-btn {
  background: none;
  border: none;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-weight: 500;
  transition: color 0.2s;
}

.back-btn:hover {
  color: var(--primary);
}

.exercise-expandable-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 15px 35px rgba(0,0,0,0.3);
}

.card-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  background: rgba(255,255,255,0.02);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex: 1;
}

.image-container {
  width: 80px;
  height: 80px;
  border-radius: 16px;
  overflow: hidden;
  background: #000;
  border: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.title-section h1 {
  font-size: 1.5rem;
  margin-bottom: 0.25rem;
  cursor: pointer;
  transition: color 0.2s;
}

.clickable-title:hover {
  color: var(--primary);
  text-decoration: underline;
}

.subtitle {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.toggle-btn {
  background: var(--glass);
  border: 1px solid var(--border);
  color: var(--primary);
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.toggle-btn:hover {
  background: var(--primary);
  color: white;
}

.sets-content {
  padding: 2rem;
  border-top: 1px solid var(--border);
  background: rgba(0,0,0,0.2);
}

.sets-table {
  width: 100%;
}

.table-header {
  display: grid;
  grid-template-columns: 50px 1fr 1fr 80px;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border);
  color: var(--text-muted);
  font-weight: 700;
  font-size: 0.85rem;
  text-transform: uppercase;
}

.set-row {
  display: grid;
  grid-template-columns: 50px 1fr 1fr 80px;
  padding: 1.25rem 0;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  align-items: center;
  font-size: 1.1rem;
}

.set-index {
  color: var(--primary);
  font-weight: 800;
}

.check-box input {
  width: 24px;
  height: 24px;
  accent-color: var(--primary);
  cursor: pointer;
}

.empty-sets {
  padding: 2rem;
  text-align: center;
  color: var(--text-muted);
  font-style: italic;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0,0,0,0.9);
  backdrop-filter: blur(10px);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.modal-content {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 32px;
  width: 100%;
  max-width: 900px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 3rem;
  position: relative;
  box-shadow: 0 30px 60px rgba(0,0,0,0.6);
}

.close-modal {
  position: absolute;
  top: 1.5rem; right: 1.5rem;
  background: var(--glass);
  border: 1px solid var(--border);
  color: white;
  width: 44px; height: 44px;
  border-radius: 50%;
  cursor: pointer;
}

.modal-header h2 { font-size: 2.5rem; margin-bottom: 1.5rem; }

.muscle-tags {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

.m-tag {
  background: var(--glass);
  padding: 0.6rem 1.2rem;
  border-radius: 12px;
  border: 1px solid var(--border);
  font-size: 1rem;
}

.m-tag small {
  color: var(--primary);
  display: block;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 0.25rem;
}

.video-wrapper {
  aspect-ratio: 16/9;
  background: #000;
  border-radius: 20px;
  overflow: hidden;
  margin-top: 1rem;
}

.detail-video { width: 100%; height: 100%; }

.instructions-section h3, .video-section h3 {
  color: var(--primary);
  margin-bottom: 1.25rem;
  font-size: 1.4rem;
}

.instructions-box {
  background: rgba(255,255,255,0.03);
  padding: 2rem;
  border-radius: 20px;
  border: 1px solid var(--border);
  line-height: 1.7;
  font-size: 1.1rem;
}

.ok-btn {
  background: var(--primary);
  color: white;
  border: none;
  width: 100%;
  padding: 1.25rem;
  border-radius: 16px;
  font-weight: 800;
  font-size: 1.2rem;
  cursor: pointer;
  margin-top: 2rem;
  transition: all 0.2s;
}

.ok-btn:hover { background: var(--primary-hover); transform: translateY(-2px); }

/* Transitions */
.expand-enter-active, .expand-leave-active { transition: all 0.3s ease; max-height: 500px; }
.expand-enter-from, .expand-leave-to { max-height: 0; opacity: 0; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.animate-pop { animation: pop 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
@keyframes pop {
  from { transform: scale(0.8); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 60vh;
  color: var(--text-muted);
}

.spinner {
  width: 40px; height: 40px;
  border: 4px solid var(--glass);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>

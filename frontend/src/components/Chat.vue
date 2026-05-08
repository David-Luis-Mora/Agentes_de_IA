<template>
  <div class="chat-container animate-fade-in">
    <div class="chat-messages" ref="messageContainer">
      <div v-if="messages.length === 0" class="empty-state">
        <MessageSquare :size="48" class="placeholder-icon" />
        <h2>Coach Chat</h2>
        <p>Hola! Soy tu entrenador personal IA. ¿En qué puedo ayudarte hoy? Podemos planificar una rutina, revisar tu progreso o hablar sobre nutrición.</p>
      </div>
      
      <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.role]">
        <div class="message-content">
          <div class="avatar">
            <User v-if="msg.role === 'user'" :size="20" />
            <Dumbbell v-else :size="20" />
          </div>
          <div class="text">
            <p>{{ msg.text }}</p>
          </div>
        </div>
      </div>

      <div v-if="loading" class="message bot thinking">
        <div class="message-content">
          <div class="avatar">
            <Dumbbell :size="20" />
          </div>
          <div class="text">
            <div class="typing-dots">
              <span></span><span></span><span></span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="chat-input-area">
      <form @submit.prevent="sendMessage" class="input-wrapper">
        <input 
          v-model="newMessage" 
          type="text" 
          placeholder="Escribe tu mensaje aquí..." 
          :disabled="loading"
        />
        <button type="submit" :disabled="loading || !newMessage.trim()">
          <Send :size="20" />
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue';
import { useAuthStore } from '../stores/auth';
import api from '../services/api';
import { Send, User, Dumbbell, MessageSquare } from 'lucide-vue-next';

const authStore = useAuthStore();
const messages = ref([]);
const newMessage = ref('');
const loading = ref(false);
const messageContainer = ref(null);

const scrollToBottom = async () => {
  await nextTick();
  if (messageContainer.value) {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
  }
};

onMounted(async () => {
  try {
    const res = await api.get('/chat-history/');
    if (res.data.history) {
      messages.value = res.data.history;
      scrollToBottom();
    }
  } catch (err) {
    console.error("Error loading chat history:", err);
  }
});

const sendMessage = async () => {
  if (!newMessage.value.trim() || loading.value) return;

  const text = newMessage.value;
  messages.value.push({ role: 'user', text });
  newMessage.value = '';
  loading.value = true;
  
  scrollToBottom();

  try {
    const res = await api.post('/chat/', { message: text });
    messages.value.push({ role: 'bot', text: res.data.response });
  } catch (err) {
    console.error("Error sending message:", err);
    messages.value.push({ 
      role: 'bot', 
      text: "Lo siento, ha ocurrido un error al conectar con el entrenador. Asegúrate de que el servidor esté funcionando." 
    });
  } finally {
    loading.value = false;
    scrollToBottom();
  }
};


watch(messages, () => {
  scrollToBottom();
}, { deep: true });
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 120px);
  max-width: 900px;
  margin: 0 auto;
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  color: var(--text-muted);
  padding: 2rem;
}

.placeholder-icon {
  margin-bottom: 1.5rem;
  color: var(--primary);
  opacity: 0.5;
}

.empty-state h2 {
  color: var(--text-main);
  margin-bottom: 1rem;
}

.message {
  display: flex;
  max-width: 80%;
  animation: fadeIn 0.3s ease-out;
}

.message.user {
  align-self: flex-end;
}

.message.bot {
  align-self: flex-start;
}

.message-content {
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
}

.message.user .message-content {
  flex-direction: row-reverse;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.message.user .avatar {
  background: var(--primary);
  color: white;
}

.message.bot .avatar {
  background: var(--glass);
  border: 1px solid var(--border);
  color: var(--primary);
}

.text {
  padding: 0.85rem 1.25rem;
  border-radius: 16px;
  font-size: 0.95rem;
  line-height: 1.5;
  white-space: pre-wrap;
}

.message.user .text {
  background: var(--primary);
  color: white;
  border-bottom-right-radius: 4px;
}

.message.bot .text {
  background: var(--glass);
  border: 1px solid var(--border);
  color: var(--text-main);
  border-bottom-left-radius: 4px;
}

.chat-input-area {
  padding: 1.5rem 2rem;
  background: rgba(15, 23, 42, 0.4);
  border-top: 1px solid var(--border);
}

.input-wrapper {
  display: flex;
  gap: 1rem;
}

.input-wrapper input {
  flex: 1;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 0.85rem 1.25rem;
  color: white;
  font-size: 1rem;
  transition: all 0.2s;
}

.input-wrapper input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
}

.input-wrapper button {
  background: var(--primary);
  color: white;
  border: none;
  border-radius: 12px;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.input-wrapper button:hover:not(:disabled) {
  background: var(--primary-hover);
  transform: translateY(-2px);
}

.input-wrapper button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Typing animation */
.typing-dots {
  display: flex;
  gap: 4px;
  padding: 4px 0;
}

.typing-dots span {
  width: 6px;
  height: 6px;
  background: var(--text-muted);
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.typing-dots span:nth-child(1) { animation-delay: -0.32s; }
.typing-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1.0); }
}
</style>

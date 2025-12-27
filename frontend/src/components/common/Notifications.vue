<script setup lang="ts">
import { computed } from 'vue'
import { useUiStore } from '../../stores/uiStore'

const uiStore = useUiStore()

const notifications = computed(() => uiStore.notifications)

const getNotificationClass = (type: string) => {
  return `notification notification-${type}`
}

const getIcon = (type: string) => {
  const icons: Record<string, string> = {
    success: '✓',
    error: '✕',
    info: 'ℹ',
    warning: '⚠',
  }
  return icons[type] || '•'
}
</script>

<template>
  <div class="notifications-container">
    <transition-group name="notification" tag="div">
      <div
        v-for="notification in notifications"
        :key="(notification as any).id"
        :class="getNotificationClass(notification.type)"
      >
        <span class="notification-icon">{{ getIcon(notification.type) }}</span>
        <span class="notification-message">{{ notification.message }}</span>
        <button
          class="notification-close"
          @click="uiStore.dismissNotification((notification as any).id)"
        >
          ×
        </button>
      </div>
    </transition-group>
  </div>
</template>

<style scoped>
.notifications-container {
  position: fixed;
  top: var(--spacing-lg);
  right: var(--spacing-lg);
  z-index: 1000;
  max-width: 400px;
}

.notification {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-md);
  border-radius: var(--radius-lg);
  background-color: white;
  box-shadow: var(--shadow-lg);
  animation: slideIn 0.3s ease-out;
}

.notification-success {
  border-left: 4px solid var(--color-success);
}

.notification-error {
  border-left: 4px solid var(--color-error);
}

.notification-info {
  border-left: 4px solid var(--color-info);
}

.notification-warning {
  border-left: 4px solid var(--color-warning);
}

.notification-icon {
  font-weight: bold;
  font-size: var(--font-size-lg);
}

.notification-success .notification-icon {
  color: var(--color-success);
}

.notification-error .notification-icon {
  color: var(--color-error);
}

.notification-info .notification-icon {
  color: var(--color-info);
}

.notification-warning .notification-icon {
  color: var(--color-warning);
}

.notification-message {
  flex: 1;
  color: var(--color-text-primary);
  font-size: var(--font-size-sm);
}

.notification-close {
  background: none;
  border: none;
  color: var(--color-text-secondary);
  font-size: var(--font-size-lg);
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color var(--transition-base);
}

.notification-close:hover {
  color: var(--color-text-primary);
}

@keyframes slideIn {
  from {
    transform: translateX(400px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  transform: translateX(400px);
  opacity: 0;
}

.notification-leave-to {
  transform: translateX(400px);
  opacity: 0;
}

@media (max-width: 768px) {
  .notifications-container {
    left: var(--spacing-md);
    right: var(--spacing-md);
    max-width: none;
  }
}
</style>


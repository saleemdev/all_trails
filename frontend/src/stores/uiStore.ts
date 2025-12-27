import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { ModalState, NotificationState } from '../types/index';

export const useUiStore = defineStore('ui', () => {
  const modals = ref<Record<string, ModalState>>({
    booking: { isOpen: false },
    confirmation: { isOpen: false },
    error: { isOpen: false },
  });

  const notifications = ref<NotificationState[]>([]);

  const openModal = (modalName: string, data?: any) => {
    if (!modals.value[modalName]) {
      modals.value[modalName] = { isOpen: false };
    }
    modals.value[modalName].isOpen = true;
    modals.value[modalName].data = data;
  };

  const closeModal = (modalName: string) => {
    if (modals.value[modalName]) {
      modals.value[modalName].isOpen = false;
      modals.value[modalName].data = undefined;
    }
  };

  const toggleModal = (modalName: string, data?: any) => {
    if (modals.value[modalName]?.isOpen) {
      closeModal(modalName);
    } else {
      openModal(modalName, data);
    }
  };

  const showNotification = (notification: NotificationState) => {
    const id = Date.now();
    const notif = { ...notification, id };
    notifications.value.push(notif as any);

    if (notification.duration !== 0) {
      setTimeout(() => {
        notifications.value = notifications.value.filter(n => (n as any).id !== id);
      }, notification.duration || 3000);
    }

    return id;
  };

  const showSuccess = (message: string, duration?: number) => {
    return showNotification({ type: 'success', message, duration });
  };

  const showError = (message: string, duration?: number) => {
    return showNotification({ type: 'error', message, duration });
  };

  const showInfo = (message: string, duration?: number) => {
    return showNotification({ type: 'info', message, duration });
  };

  const showWarning = (message: string, duration?: number) => {
    return showNotification({ type: 'warning', message, duration });
  };

  const dismissNotification = (id: number) => {
    notifications.value = notifications.value.filter(n => (n as any).id !== id);
  };

  const clearAllNotifications = () => {
    notifications.value = [];
  };

  return {
    modals,
    notifications,
    openModal,
    closeModal,
    toggleModal,
    showNotification,
    showSuccess,
    showError,
    showInfo,
    showWarning,
    dismissNotification,
    clearAllNotifications,
  };
});


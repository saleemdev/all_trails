<script setup lang="ts">
import { computed, watch } from 'vue'
import { useUiStore } from '../../stores/uiStore'
import { toast } from 'frappe-ui'

const uiStore = useUiStore()

const notifications = computed(() => uiStore.notifications)

// Watch for new notifications and show them using frappe-ui toast
watch(notifications, (newNotifications) => {
  newNotifications.forEach((notification: any) => {
    if (!notification._shown) {
      notification._shown = true
      
      const duration = notification.duration || 3000
      
      switch (notification.type) {
        case 'success':
          toast.success(notification.message, { duration })
          break
        case 'error':
          toast.error(notification.message, { duration })
          break
        case 'warning':
          toast.warning(notification.message, { duration })
          break
        case 'info':
        default:
          toast.info(notification.message, { duration })
          break
      }
      
      // Auto-dismiss after duration
      if (duration > 0) {
        setTimeout(() => {
          uiStore.dismissNotification(notification.id)
        }, duration)
      }
    }
  })
}, { deep: true, immediate: true })
</script>

<template>
  <!-- frappe-ui toast is handled globally, no template needed -->
  <div></div>
</template>

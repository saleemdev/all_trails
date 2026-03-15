<script setup lang="ts">
interface InputOption {
  label: string
  value: string
}

const props = withDefaults(
  defineProps<{
    modelValue: string | number
    label?: string
    placeholder?: string
    type?: string
    help?: string
    error?: string
    textarea?: boolean
    options?: InputOption[]
    required?: boolean
    disabled?: boolean
    min?: number
    max?: number
  }>(),
  {
    label: '',
    placeholder: '',
    type: 'text',
    help: '',
    error: '',
    textarea: false,
    options: () => [],
    required: false,
    disabled: false,
    min: undefined,
    max: undefined,
  }
)

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const updateValue = (event: Event) => {
  emit('update:modelValue', (event.target as HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement).value)
}
</script>

<template>
  <label class="flex flex-col gap-1.5 text-[13px]">
    <span v-if="props.label" class="font-medium tone-heading">
      {{ props.label }}
      <span v-if="props.required" class="text-red-600">*</span>
    </span>

    <textarea
      v-if="props.textarea"
      :value="props.modelValue"
      :placeholder="props.placeholder"
      :required="props.required"
      :disabled="props.disabled"
      rows="3"
      class="soft-input min-h-24 resize-y rounded-[0.9rem]"
      @input="updateValue"
    />

    <select
      v-else-if="props.options.length"
      :value="props.modelValue"
      :required="props.required"
      :disabled="props.disabled"
      class="soft-input rounded-[0.9rem]"
      @change="updateValue"
    >
      <option v-for="option in props.options" :key="option.value" :value="option.value">
        {{ option.label }}
      </option>
    </select>

    <input
      v-else
      :value="props.modelValue"
      :type="props.type"
      :placeholder="props.placeholder"
      :required="props.required"
      :disabled="props.disabled"
      :min="props.min"
      :max="props.max"
      class="soft-input rounded-[0.9rem]"
      @input="updateValue"
    />

    <span v-if="props.error" class="text-xs text-red-600">{{ props.error }}</span>
    <span v-else-if="props.help" class="text-xs tone-muted">{{ props.help }}</span>
  </label>
</template>

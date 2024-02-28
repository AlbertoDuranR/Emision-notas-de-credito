<script setup>

const emit = defineEmits(['search'])

const search = (e) => {
  // console.log(e.target.value)
  emit('search', e.target.value);
}
</script>

<template>
  <form class="py-3 flex items-center">
    <label class="text-sm mr-2">Buscar: </label>
    <div class="relative w-full">
      <input type="text" @input="search" placeholder="Fecha" class="bg-gray-50 border border-gray-300 text-gray-900 px-2 py-1 rounded-lg">
    </div>
  </form>
</template>

<style scoped>
</style>
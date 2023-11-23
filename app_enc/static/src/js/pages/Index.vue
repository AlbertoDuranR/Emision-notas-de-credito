<template>
    <Header />
    <div class="container mx-auto px-6 pt-60">
        <div class="flex items-center justify-center"><span class="text-lg font-bold text-gray-500">Bienvenido a la página de Gestion de Notas
                de Crédito</span></div>
        <div class="flex items-center justify-center"><span class="text-sm text-gray-500">Proceda a seleccionar alguna opción del menú superior</span></div>
        <!-- <a @click="navigateTo('/login2')">Bienvenido a la pagina</a> -->
    </div>
</template>
<script setup>
// Importando layouts
import Header from '../layouts/Header.vue'

</script>
<script>
export default {
    name: "Index",
    props: {
        array: Array,
        errors: Object
    },
    methods: {
        navigateTo(route) {
            this.$inertia.visit(route);
        }
    }
}
</script>
<style scope></style>
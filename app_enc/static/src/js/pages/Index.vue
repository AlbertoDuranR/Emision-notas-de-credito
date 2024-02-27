<template>
    <Header :selectMarket="selectMarket?.mar_descripcion"/>
    <div class="container mx-auto px-30 pt-30">
        <div class="flex items-center justify-center pt-10"><span class="text-2xl font-bold text-gray-500">Bienvenido a la página de Gestion de Notas
                de Crédito</span></div>
        <div class="space-y-1 px-60 py-2 pt-10 text-center">
              <label class="text-gray-500 text-lg">Seleccionar Establecimiento</label>
              <multiselect
                v-model="selectMarket"
                id="multiselect"
                :options="establecimiento.options"
                :preserve-search="true"
                placeholder="Seleccionar local..."
                label="mar_descripcion"
                track-by="mar_descripcion"
              >
              </multiselect>
        </div>

        <!-- <div class="flex items-center justify-center"><span class="text-sm text-gray-500">Proceda a seleccionar alguna opción del menú superior</span></div> -->
        <!-- <a @click="navigateTo('/login2')">Bienvenido a la pagina</a> -->
    </div>
</template>
<script setup>
// Importando layouts
import Header from '../layouts/Header.vue'
import Multiselect from "vue-multiselect";
</script>
<script>
export default {
    name: "Index",
    props: {
        array: Array,
        errors: Object,
        lista_markets: Array,
    },
    data() {
        return {
        showUser: false,
        selectMarket: null,
        establecimiento: {
          options: this.lista_markets,
          // options: ['a', 'b'],
        },
        };
    },
    methods: {
        navigateTo(route) {
            this.$inertia.visit(route);
        }
    }
}
</script>
<style scope>
@import "https://unpkg.com/vue-multiselect@2.1.6/dist/vue-multiselect.min.css";
</style>
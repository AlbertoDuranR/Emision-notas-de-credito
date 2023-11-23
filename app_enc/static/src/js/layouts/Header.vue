<template>
    <div class="block">
        <div class="bg-white">
            <nav class="
          container
          px-6
          py-4
          mx-auto
          md:flex md:justify-between md:items-center
        ">
                <div class="flex items-center justify-between">
                    <router-link to="/" class="
              text-xl
              font-bold
              text-gray-800
              md:text-2xl
              hover:text-amber-400
            ">
                        <img :src="image" class="h-10" />
                    </router-link>
                    <div @click="showMenu = !showMenu" class="flex md:hidden">
                        <button type="button" class="
                text-gray-800
                hover:text-gray-400
                focus:outline-none focus:text-gray-400
              ">
                            <svg viewBox="0 0 24 24" class="w-6 h-6 fill-current">
                                <path fill-rule="evenodd"
                                    d="M4 5h16a1 1 0 0 1 0 2H4a1 1 0 1 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2z">
                                </path>
                            </svg>
                        </button>
                    </div>
                </div>
                <div class="flex items-center space-x-2">
                    <svg class="h-9 w-9 p-2 text-white rounded-full bg-red-600" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                        <circle cx="12" cy="7" r="4" />
                    </svg>
                    <div>
                        <div class="dropdown inline-block relative">
                            <button class="text-gray-700 text-sm font-semibold rounded inline-flex items-center">
                                <span class="mr-1">Wilfredo Cáceres</span>
                                <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                                    <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
                                </svg>
                            </button>
                            <ul class="dropdown-menu absolute hidden text-gray-500 font-semibold text-sm pt-2 h-auto drop-shadow-lg">
                                <li class=""><a
                                        class="rounded bg-white hover:bg-gray-200 py-2 px-4 block whitespace-no-wrap"
                                        href="#">Cerrar Sesión</a></li>
                            </ul>
                        </div>

                    </div>
                </div>
            </nav>
        </div>
        <hr>
        <div class="bg-white">
            <nav class="container
          px-6
          py-4
          mx-auto
          md:flex md:justify-center md:items-center">
                <ul :class="showMenu ? 'flex' : 'hidden'" class="
            flex-col
            mt-2
            space-y-4
            md:flex
            md:space-y-0
            md:flex-row
            md:items-center
            md:space-x-10
            md:mt-0
          ">
                    <li class="text-sm font-bold text-gray-500 hover:text-amber-400 flex items-center space-x-1">
                        <svg class="h-8 w-8 text-gray-500 hover:text-amber-400 " fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2h-2M8 7H6a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-2" />
                        </svg> <div class="dropdown inline-block relative">
                            <button class="text-gray-500 text-sm font-semibold rounded inline-flex items-center">
                                <span class="mr-1 font-bold">Solicitar Notas de Crédito</span>
                                <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                                    <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
                                </svg>
                            </button>
                            <ul class="dropdown-menu absolute hidden text-gray-500 font-semibold text-sm pt-3 h-auto drop-shadow-md">
                                <li class=""><a
                                        class="rounded bg-white hover:bg-gray-100 py-2 px-4 block whitespace-no-wrap"
                                        @click="navigateTo('/solicitud_nota_credito/punto_venta')">Punto de Venta</a></li>
                                <li class=""><a class="rounded bg-white hover:bg-gray-100 py-2 px-4 block whitespace-no-wrap"
                                    @click="navigateTo('/solicitud_nota_credito/financieros')">Financiero</a></li>
                                <li class=""><a
                                        class="rounded bg-white hover:bg-gray-100 py-2 px-4 block whitespace-no-wrap"
                                        @click="navigateTo('/solicitud_nota_credito/servicios')">Servicios</a></li>
                            </ul>
                        </div>
                    </li>
                    <li class="text-sm font-bold text-gray-500 hover:text-amber-400 flex items-center space-x-1">
                        <svg class="h-8 w-8 text-gray-500 hover:text-amber-400 "  width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">  <path stroke="none" d="M0 0h24v24H0z"/>  <polyline points="12 4 4 8 12 12 20 8 12 4" />  <polyline points="4 12 12 16 20 12" />  <polyline points="4 16 12 20 20 16" /></svg><div class="dropdown inline-block relative">
                            <button class="text-gray-500 text-sm font-semibold rounded inline-flex items-center">
                                <span class="mr-1 font-bold">Consolidación</span>
                                <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                                    <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
                                </svg>
                            </button>
                            <ul class="dropdown-menu absolute hidden text-gray-500 font-semibold text-sm pt-3 h-auto drop-shadow-md">
                                <li class=""><a
                                        class="rounded bg-white hover:bg-gray-100 py-2 px-4 block whitespace-no-wrap"
                                        @click="navigateTo('/consolidacion_nota_credito/punto_venta')">Punto de Venta</a></li>
                                <li class=""><a class="rounded bg-white hover:bg-gray-100 py-2 px-4 block whitespace-no-wrap"
                                    @click="navigateTo('/consolidacion_nota_credito/financieros')">Financiero</a></li>
                                <li class=""><a
                                        class="rounded bg-white hover:bg-gray-100 py-2 px-4 block whitespace-no-wrap"
                                        @click="navigateTo('/consolidacion_nota_credito/servicios')">Servicios</a></li>
                            </ul>
                        </div>
                    </li>
                    <li class="text-sm font-bold text-gray-500 hover:text-amber-400 flex items-center space-x-1">
                        <svg class="h-8 w-8 text-gray-500 hover:text-amber-400 "  width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">  <path stroke="none" d="M0 0h24v24H0z"/>  <path d="M9 4h3l2 2h5a2 2 0 0 1 2 2v7a2 2 0 0 1 -2 2h-10a2 2 0 0 1 -2 -2v-9a2 2 0 0 1 2 -2" />  <path d="M17 17v2a2 2 0 0 1 -2 2h-10a2 2 0 0 1 -2 -2v-9a2 2 0 0 1 2 -2h2" /></svg>
                        <div class="dropdown inline-block relative">
                            <button class="text-gray-500 text-sm font-semibold rounded inline-flex items-center">
                                <span class="mr-1 font-bold">Bandeja de Solicitudes</span>
                                <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                                    <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
                                </svg>
                            </button>
                            <ul class="dropdown-menu absolute hidden text-gray-500 font-semibold text-sm pt-3 h-auto drop-shadow-md">
                                <li class=""><a
                                        class="rounded bg-white hover:bg-gray-100 py-2 px-4 block whitespace-no-wrap"
                                        @click="navigateTo('/bandeja_nota_credito/punto_venta')">Punto de Venta</a></li>
                                <li class=""><a class="rounded bg-white hover:bg-gray-100 py-2 px-4 block whitespace-no-wrap"
                                    @click="navigateTo('/bandeja_nota_credito/financieros')">Financiero</a></li>
                                <li class=""><a
                                        class="rounded bg-white hover:bg-gray-100 py-2 px-4 block whitespace-no-wrap"
                                        @click="navigateTo('/bandeja_nota_credito/servicios')">Servicios</a></li>
                            </ul>
                        </div>
                    </li>
                    <li class="text-sm font-bold text-gray-500 hover:text-amber-400 flex items-center space-x-1">
                        <svg class="h-8 w-8 text-gray-500 hover:text-amber-400 "  width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">  <path stroke="none" d="M0 0h24v24H0z"/>  <path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 0 0 2.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 0 0 1.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 0 0 -1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 0 0 -2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 0 0 -2.573 -1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 0 0 -1.065 -2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 0 0 1.066 -2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />  <circle cx="12" cy="12" r="3" /></svg>
                        <span>Configuración</span>
                    </li>
                </ul>
            </nav>
        </div>
    </div>
</template>
<script setup>
</script>
<script>
import image from "../../../dist/Logo3.png"
export default {
    name: "Header",
    data: function () {
        return {
            image: image,
            showMenu: false
        }
    },
    methods: {
        toggleNav: function () {
            this.showMenu = !this.showMenu;
        },
        navigateTo(route) {
            this.$inertia.visit(route);
        }
    }
}
</script>
<style scoped>
.dropdown:hover .dropdown-menu {
    display: block;
}
</style>
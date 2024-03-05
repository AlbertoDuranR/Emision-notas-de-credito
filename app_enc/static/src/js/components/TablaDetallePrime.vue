<template>
    <ThemeSwitcher />
    <div class="card">
        <DataTable v-model:filters="filters" :value="solicitudes" paginator
            :rows="15" dataKey="id" filterDisplay="menu"
            :globalFilterFields="['ID_NC', 'SOLICITANTE', 'ESTABLECIMIENTO', 'TIPO', 'NRO_COMPROBANTE']"
            sortField="ID_NC"
            :sortOrder="-1"
            >
            <template #header>
                <div class="flex justify-between">
                    <Button type="button" icon="pi pi-filter-slash" label="Limpiar" outlined @click="clearFilter()" />
                    <span class="relative">
                        <!-- <i class="pi pi-search absolute top-2/4 -mt-2 left-3 text-surface-400 dark:text-surface-600" /> -->
                        <svg xmlns="http://www.w3.org/2000/svg" height="18" width="18" viewBox="0 0 512 512"
                            class="pi absolute top-2/4 -mt-2 left-3 text-surface-400 dark:text-surface-600">
                            <path
                                d="M416 208c0 45.9-14.9 88.3-40 122.7L502.6 457.4c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L330.7 376c-34.4 25.2-76.8 40-122.7 40C93.1 416 0 322.9 0 208S93.1 0 208 0S416 93.1 416 208zM208 352a144 144 0 1 0 0-288 144 144 0 1 0 0 288z" />
                        </svg>
                        <InputText v-model="filters['global'].value" placeholder="Buscar" class="pl-10 font-normal" />
                    </span>
                </div>
            </template>

            <template #empty> No se encontraron Solicitudes. </template>
            <Column field="ID_NC" header="ID" sortable style="min-width: 0.5rem; padding: 0 0.5rem 0 0.5rem"
                class="text-sm">
                <template #body="{ data }">
                    {{ data.ID_NC }}
                </template>
            </Column>
            <Column field="FECHA_CREACION" header="Fecha C. Solicitud" sortable filterField="FECHA_CREACION"
                dataType="date" style="min-width: 2rem ; padding: 0 0.5rem 0 0.5rem" class="text-sm">

                <template #body="{ data }">
                    {{ formatDate(data.FECHA_CREACION) }}
                </template>

                <template #filter="{ filterModel }">
                    <Calendar v-model="filterModel.value" dateFormat="dd/mm/yy" placeholder="dd/mm/yyyy"
                        mask="99/99/9999" />
                </template>
            </Column>
            <Column header="Solicitante" sortable sortField="SOLICITANTE" filterField="SOLICITANTE"
                style="min-width: 2rem;  padding: 0 0.5rem 0 0.5rem;" class="text-xs">

                <template #body="{ data }">
                    {{ data.SOLICITANTE }}
                </template>

                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" class="p-column-filter"
                        placeholder="Buscar por Solicitante" />
                </template>
            </Column>
            <Column header="Sucursal" sortable sortField="ESTABLECIMIENTO" filterField="ESTABLECIMIENTO"
                style="min-width: 0.5rem; padding: 0 0.5rem 0 0.5rem;" class="text-xs">

                <template #body="{ data }">
                    {{ data.ESTABLECIMIENTO }}
                </template>

                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" class="p-column-filter"
                        placeholder="Buscar por Sucursal" />
                </template>
            </Column>
            <Column field="FECHA_EMISION" header="Fecha Comprobante" sortable filterField="FECHA_EMISION"
                dataType="date" style="min-width: 10rem; padding: 0 0.5rem 0 0.5rem" class="text-sm">

                <template #body="{ data }">
                    {{ formatDate(data.FECHA_EMISION) }}
                </template>

                <template #filter="{ filterModel }">
                    <Calendar v-model="filterModel.value" dateFormat="dd/mm/yy" placeholder="dd/mm/yyyy"
                        mask="99/99/9999" />
                </template>
            </Column>
            <Column header="Tipo Comprobante" sortable sortField="TIPO" filterField="TIPO"
                style="min-width: 5rem; padding: 0 0.5rem 0 0.5rem" class="text-xs">

                <template #body="{ data }">
                    {{ data.TIPO }}
                </template>

                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" class="p-column-filter"
                        placeholder="Buscar por Tipo" />
                </template>
            </Column>
            <Column header="N° Comprobante" sortable sortField="NRO_COMPROBANTE" filterField="NRO_COMPROBANTE"
                style="min-width: 5rem; padding: 0 0.5rem 0 0.5rem" class="text-sm">

                <template #body="{ data }">
                    {{ data.NRO_COMPROBANTE }}
                </template>

                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" class="p-column-filter"
                        placeholder="Search by country" />
                </template>
            </Column>
            <Column header="Estado" sortable sortField="ESTADO" filterField="ESTADO"
                style="min-width: 5rem; padding: 0 0.5rem 0 0.5rem" class="text-xs">

                <template #body="{ data }">
                    <span :class="{
                        'bg-gray-400': data.ESTADO === 'PENDIENTE',
                        'bg-yellow-500': data.ESTADO === 'ACTUALIZADO',
                        'bg-red-500': data.ESTADO === 'OBSERVADO' || data.ESTADO === 'ERROR',
                        'bg-cyan-500': data.ESTADO == 'VALIDADO',
                        'bg-emerald-500': data.ESTADO === 'CREADO',
                    }" class="px-2 py-1 text-white rounded">
                        {{ data.ESTADO }}
                    </span>
                    <button v-if="data.ESTADO === 'OBSERVADO'" class="bg-blue-0 text-white pl-2"
                        @click="mostrarObservacion(data.OBSERVACION)">
                        <svg xmlns="http://www.w3.org/2000/svg" height="16" width="20" viewBox="0 0 640 512">
                            <path
                                d="M88.2 309.1c9.8-18.3 6.8-40.8-7.5-55.8C59.4 230.9 48 204 48 176c0-63.5 63.8-128 160-128s160 64.5 160 128s-63.8 128-160 128c-13.1 0-25.8-1.3-37.8-3.6c-10.4-2-21.2-.6-30.7 4.2c-4.1 2.1-8.3 4.1-12.6 6c-16 7.2-32.9 13.5-49.9 18c2.8-4.6 5.4-9.1 7.9-13.6c1.1-1.9 2.2-3.9 3.2-5.9zM0 176c0 41.8 17.2 80.1 45.9 110.3c-.9 1.7-1.9 3.5-2.8 5.1c-10.3 18.4-22.3 36.5-36.6 52.1c-6.6 7-8.3 17.2-4.6 25.9C5.8 378.3 14.4 384 24 384c43 0 86.5-13.3 122.7-29.7c4.8-2.2 9.6-4.5 14.2-6.8c15.1 3 30.9 4.5 47.1 4.5c114.9 0 208-78.8 208-176S322.9 0 208 0S0 78.8 0 176zM432 480c16.2 0 31.9-1.6 47.1-4.5c4.6 2.3 9.4 4.6 14.2 6.8C529.5 498.7 573 512 616 512c9.6 0 18.2-5.7 22-14.5c3.8-8.8 2-19-4.6-25.9c-14.2-15.6-26.2-33.7-36.6-52.1c-.9-1.7-1.9-3.4-2.8-5.1C622.8 384.1 640 345.8 640 304c0-94.4-87.9-171.5-198.2-175.8c4.1 15.2 6.2 31.2 6.2 47.8l0 .6c87.2 6.7 144 67.5 144 127.4c0 28-11.4 54.9-32.7 77.2c-14.3 15-17.3 37.6-7.5 55.8c1.1 2 2.2 4 3.2 5.9c2.5 4.5 5.2 9 7.9 13.6c-17-4.5-33.9-10.7-49.9-18c-4.3-1.9-8.5-3.9-12.6-6c-9.5-4.8-20.3-6.2-30.7-4.2c-12.1 2.4-24.7 3.6-37.8 3.6c-61.7 0-110-26.5-136.8-62.3c-16 5.4-32.8 9.4-50 11.8C279 439.8 350 480 432 480z" />
                        </svg>
                    </button>
                </template>

                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" class="p-column-filter"
                        placeholder="Buscar por Estado" />
                </template>
            </Column>
            <Column header="Opciones" style="min-width: 8rem" class="text-sm">
                <template #body="{ data }">
                    <button class="bg-red-0 text-white px-2 py-1 w-1/3" @click="getDatosSolicitud(data.ID_NC)">
                        <svg xmlns="http://www.w3.org/2000/svg" height="19" width="19" viewBox="0 0 512 512">
                            <path
                                d="M416 208c0 45.9-14.9 88.3-40 122.7L502.6 457.4c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L330.7 376c-34.4 25.2-76.8 40-122.7 40C93.1 416 0 322.9 0 208S93.1 0 208 0S416 93.1 416 208zM208 352a144 144 0 1 0 0-288 144 144 0 1 0 0 288z" />
                        </svg>
                    </button>
                    <!-- INIT Bandeja -->
                    <button v-show="!['VALIDADO', 'CREADO', 'ERROR'].includes(data.ESTADO) && props.tipo == 'bandeja'"
                        @click="validarItem(data.ID_NC, data.NRO_COMPROBANTE)"
                        class="bg-blue-0 text-white px-2 py-1 w-1/3">
                        <svg xmlns="http://www.w3.org/2000/svg" height="20" width="20" viewBox="0 0 512 512">
                            <path
                                d="M256 48a208 208 0 1 1 0 416 208 208 0 1 1 0-416zm0 464A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM369 209c9.4-9.4 9.4-24.6 0-33.9s-24.6-9.4-33.9 0l-111 111-47-47c-9.4-9.4-24.6-9.4-33.9 0s-9.4 24.6 0 33.9l64 64c9.4 9.4 24.6 9.4 33.9 0L369 209z" />
                        </svg>
                    </button>
                    <button v-show="data.ESTADO !== 'CREADO' && props.tipo == 'bandeja'"
                        @click="observarItem(data.ID_NC)" class="bg-red-0 text-white px-2 py-1 w-1/3">
                        <svg xmlns="http://www.w3.org/2000/svg" height="20" width="20" viewBox="0 0 512 512">
                            <path
                                d="M256 48a208 208 0 1 1 0 416 208 208 0 1 1 0-416zm0 464A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM175 175c-9.4 9.4-9.4 24.6 0 33.9l47 47-47 47c-9.4 9.4-9.4 24.6 0 33.9s24.6 9.4 33.9 0l47-47 47 47c9.4 9.4 24.6 9.4 33.9 0s9.4-24.6 0-33.9l-47-47 47-47c9.4-9.4 9.4-24.6 0-33.9s-24.6-9.4-33.9 0l-47 47-47-47c-9.4-9.4-24.6-9.4-33.9 0z" />
                        </svg>
                    </button>
                    <button v-show="data.ESTADO == 'VALIDADO' && props.tipo == 'bandeja'"
                        @click="generarNotaItem(data.ID_NC)" class="bg-red-0 text-white px-2 py-1 w-1/3">
                        <svg xmlns="http://www.w3.org/2000/svg" height="22" width="22" viewBox="0 0 24 24" fill="none"
                            stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16c0 1.1.9 2 2 2h12a2 2 0 0 0 2-2V8l-6-6z" />
                            <path d="M14 3v5h5M16 13H8M16 17H8M10 9H8" />
                        </svg>
                    </button>
                    <!-- END Bandeja -->
                    <!-- INIT consolidado -->
                    <button v-if="!['VALIDADO', 'CREADO'].includes(data.ESTADO) && props.tipo == 'consolidado'"
                        @click="editarItem(data.ID_NC, data.ID_DETALLE)" class="bg-blue-0 text-white px-2 py-1 w-1/3">
                        <svg xmlns="http://www.w3.org/2000/svg" height="19" width="19" viewBox="0 0 512 512">
                            <path
                                d="M441 58.9L453.1 71c9.4 9.4 9.4 24.6 0 33.9L424 134.1 377.9 88 407 58.9c9.4-9.4 24.6-9.4 33.9 0zM209.8 256.2L344 121.9 390.1 168 255.8 302.2c-2.9 2.9-6.5 5-10.4 6.1l-58.5 16.7 16.7-58.5c1.1-3.9 3.2-7.5 6.1-10.4zM373.1 25L175.8 222.2c-8.7 8.7-15 19.4-18.3 31.1l-28.6 100c-2.4 8.4-.1 17.4 6.1 23.6s15.2 8.5 23.6 6.1l100-28.6c11.8-3.4 22.5-9.7 31.1-18.3L487 138.9c28.1-28.1 28.1-73.7 0-101.8L474.9 25C446.8-3.1 401.2-3.1 373.1 25zM88 64C39.4 64 0 103.4 0 152V424c0 48.6 39.4 88 88 88H360c48.6 0 88-39.4 88-88V312c0-13.3-10.7-24-24-24s-24 10.7-24 24V424c0 22.1-17.9 40-40 40H88c-22.1 0-40-17.9-40-40V152c0-22.1 17.9-40 40-40H200c13.3 0 24-10.7 24-24s-10.7-24-24-24H88z" />
                        </svg>
                    </button>
                    <button v-if="!['VALIDADO', 'CREADO'].includes(data.ESTADO) && props.tipo == 'consolidado'"
                        @click="eliminarItem(data.ID_NC)" class="bg-red-0 text-white px-2 py-1 w-1/3">
                        <svg xmlns="http://www.w3.org/2000/svg" height="19" width="16" viewBox="0 0 448 512">
                            <path
                                d="M268 416h24a12 12 0 0 0 12-12V188a12 12 0 0 0 -12-12h-24a12 12 0 0 0 -12 12v216a12 12 0 0 0 12 12zM432 80h-82.4l-34-56.7A48 48 0 0 0 274.4 0H173.6a48 48 0 0 0 -41.2 23.3L98.4 80H16A16 16 0 0 0 0 96v16a16 16 0 0 0 16 16h16v336a48 48 0 0 0 48 48h288a48 48 0 0 0 48-48V128h16a16 16 0 0 0 16-16V96a16 16 0 0 0 -16-16zM171.8 50.9A6 6 0 0 1 177 48h94a6 6 0 0 1 5.2 2.9L293.6 80H154.4zM368 464H80V128h288zm-212-48h24a12 12 0 0 0 12-12V188a12 12 0 0 0 -12-12h-24a12 12 0 0 0 -12 12v216a12 12 0 0 0 12 12z" />
                        </svg>
                    </button>
                </template>
            </Column>
            <Column field="FECHA_SOLICITUD" header="Fecha N. De Crédito" sortable filterField="FECHA_SOLICITUD"
                dataType="date" style="min-width: 5rem; padding: 0 0.5rem 0 0.5rem" class="text-sm">
                <template #body="{ data }">
                    {{ formatDate(data.FECHA_SOLICITUD) }}
                </template>
                <template #filter="{ filterModel }">
                    <Calendar v-model="filterModel.value" dateFormat="dd/mm/yy" placeholder="dd/mm/yyyy"
                        mask="99/99/9999" />
                </template>
            </Column>
            <Column header="Método" sortable sortField="METODO" filterField="METODO"
                style="min-width: 5rem; padding: 0 0.5rem 0 0.5rem" class="text-sm">
                <template #body="{ data }">
                    {{ capitalizeFirstLetter(data.METODO) }}
                </template>
                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" class="p-column-filter"
                        placeholder="Buscar por Método" />
                </template>
            </Column>
            <Column header="Importe N. De Crédito" style="min-width: 2rem" class="text-sm">

                <template #body="{ data }">
                    {{ formatCurrency(data.MONTO_TOTAL) }}
                </template>
            </Column>
            <Column header="N° N. De Crédito" sortable sortField="NRO_NOTA_CREDITO" filterField="NRO_NOTA_CREDITO"
                style="min-width: 5rem; padding: 0 0.5rem 0 0.5rem" class="text-xs">
                <template #body="{ data }">
                    <span v-show="data.ESTADO_NOTA_CREDITO === 'PENDIENTE'" :class="{
                        'bg-gray-300': data.ESTADO_NOTA_CREDITO === 'PENDIENTE',
                        // 'bg-red-500': data.ESTADO_NOTA_CREDITO === 'ERROR',
                        // 'bg-emerald-500': data.ESTADO === 'CREADO',
                    }" class="px-2 py-1 text-white rounded">
                        {{ data.ESTADO_NOTA_CREDITO }}
                    </span>
                    <span v-show="data.ESTADO === 'CREADO'" :class="{
                        'bg-gray-300': data.ESTADO_NOTA_CREDITO === 'PENDIENTE',
                        // 'bg-red-500': data.ESTADO_NOTA_CREDITO === 'ERROR',
                        // 'bg-emerald-500': data.ESTADO === 'CREADO',
                    }" class="px-2 py-1 rounded">
                        <a @click="downloadNota(data.NRO_NOTA_CREDITO)" class="rounded bg-white hover:text-cyan-400 cursor-pointer"><b>{{ data.NRO_NOTA_CREDITO }}</b></a>
                    </span>
                    <button v-if="data.ESTADO === 'ERROR' || data.ESTADO_NOTA_CREDITO === 'ERROR'"
                        @click="reintentarNC(data.ID_NC, data.OBS_ESTADO_RPA_NOTA_CREDITO)"
                        class="text-center text-white px-2 py-1">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 25 25" fill="none"
                            stroke="#ef4444" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M2.5 2v6h6M21.5 22v-6h-6" />
                            <path d="M22 11.5A10 10 0 0 0 3.2 7.2M2 12.5a10 10 0 0 0 18.8 4.2" />
                        </svg>
                    </button>
                </template>
                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" class="p-column-filter"
                        placeholder="Buscar por Nota de Crédito" />
                </template>
            </Column>
            <Column header="Acepta" sortable sortField="ACEPTA" filterField="ACEPTA"
                style="min-width: 5rem; padding: 0 0.5rem 0 0.5rem" class="text-xs">

                <template #body="{ data }">
                    <span :class="{
                        'bg-gray-300': data.ACEPTA === 'PENDIENTE',
                        'bg-red-500': data.ACEPTA === 'OBSERVADO',
                        'bg-cyan-500': data.ACEPTA == 'ACEPTADO',
                    }" class="px-2 py-1 text-white rounded">
                        {{ data.ACEPTA }}
                    </span>
                </template>

                <template #filter="{ filterModel }">
                    <InputText v-model="filterModel.value" type="text" class="p-column-filter"
                        placeholder="Buscar por estado Acepta" />
                </template>
            </Column>
        </DataTable>
    </div>
    <ModalReview v-if="isOpen" @show-modal="closeModal" @close="closeModal" :open="isOpen"
        :detalleSolicitud="datos_detalle_solicitud" />
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { FilterMatchMode, FilterOperator } from 'primevue/api';
import { capitalizeFirstLetter, formatCurrency, getDateGMT } from '../utils';
import { downloadNotaTxt } from '../service/downloadFile'

import Swal from "sweetalert2";
import axios from "axios";
import ModalReview from "../components/ModalReview";
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Calendar from 'primevue/calendar'

const props = defineProps({
    "tipo": {
        type: String
    },
    "listaSolicitudes": {
        type: Array,
        required: true
    }
});
const emit = defineEmits([
    "editar-item",
    "eliminar-item",
    "validar_item",
    "observar_item",
    "generar_nota_item",
    "reintentar_nota_item"
]);
const isOpen = ref(false);
const datos_detalle_solicitud = ref({});

const solicitudes = ref();
const filters = ref();
const loading = ref(true);


onMounted(() => {
    console.log('onMounted-props.listaSolicitudes', props.listaSolicitudes)
    solicitudes.value = getSolicitudes(props.listaSolicitudes);
    console.log(' solicitudes.value ',  solicitudes.value )
    loading.value = false;
});


const editarItem = (idSol, nroComprobante) => {
    emit("editar-item", idSol, nroComprobante);
};
const eliminarItem = (item) => {
    emit("eliminar-item", item);
};
const validarItem = (itemNota, nroComprobante) => {
    emit("validar_item", itemNota, nroComprobante);
};
const observarItem = (item_nota) => {
    emit("observar_item", item_nota);
};
const generarNotaItem = (item_nota) => {
    emit("generar_nota_item", item_nota);
};
const reintentarNC = (item_nota, obs_rpa_nota_credito) => {
    emit("reintentar_nota_item", item_nota, obs_rpa_nota_credito)
}

const openModal = () => {
    isOpen.value = true;
};
const closeModal = () => {
    isOpen.value = false;
};

const mostrarObservacion = (dato) => {
    Swal.fire({
        title: "Detalle de la observacion",
        text: dato,
        icon: "info",
        showConfirmButton: true,
        allowOutsideClick: false,
    });
};

const getDatosSolicitud = async (idSol) => {
    try {
        console.log("entro activador modal");
        const response = await axios.get(
            `/solicitud_nota_credito/datos_solicitud/${idSol}`
        );
        if (response.status == 200) {
            openModal();
            datos_detalle_solicitud.value = response.data;
        }
    } catch (error) {
        console.error(error);
        Swal.fire({
            title: "ERROR",
            text: `No se tiene datos de esta solicitud: ${idSol}`,
            icon: "error",
        });
    }
};

const initFilters = () => {
    filters.value = {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        ID_NC: { value: null, matchMode: FilterMatchMode.CONTAINS },
        FECHA_CREACION: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }] },
        SOLICITANTE: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
        ESTABLECIMIENTO: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
        FECHA_EMISION: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }] },
        TIPO: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
        NRO_COMPROBANTE: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
        ESTADO: { operator: FilterOperator.OR, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
        FECHA_SOLICITUD: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }] },
        METODO: { operator: FilterOperator.OR, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
        NRO_NOTA_CREDITO: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
        ACEPTA: { operator: FilterOperator.OR, constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }] },
    };
};

initFilters();

const formatDate = (value) => {
    // const value = '2018-11-21'
    // const date= new Date(value);
    return value.toLocaleDateString('es-PE', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        separator: '/'
    });
};

const clearFilter = () => {
    initFilters();
};

const getSolicitudes = (data) => {
    return [...(data || [])].map((item) => {
        let newItem = { ...item };
        newItem.FECHA_CREACION = getDateGMT(newItem.FECHA_CREACION);
        newItem.FECHA_EMISION = getDateGMT(item.FECHA_EMISION);
        newItem.FECHA_SOLICITUD = getDateGMT(item.FECHA_SOLICITUD);
        return newItem;
    });
};

const downloadNota = async (nroNotaCredito) => {
    try {
        await downloadNotaTxt(nroNotaCredito);
    } catch (error) {
        Swal.fire({
            title: "Archivo no encontrado",
            text: `Error al descargar el archivo:${nroNotaCredito}.txt`,
            icon: "error",
        });
    }
}

</script>
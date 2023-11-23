<template>
    <Header />
    <div class="container px-6 mx-auto block">
        <div class="flex items-center justify-center py-5"><span class="font-bold text-gray-600">BANDEJA DE SOLICITUDES DE NOTAS DE
                CRÉDITO - SERVICIOS</span></div>
    </div>
    <div class="px-4 flex justify-center">
    <button class="text-sm rounded-full bg-green-600 p-2 text-white font-bold flex" type="button"><svg class="h-5 w-5 white"  fill="none" viewBox="0 0 24 24" stroke="currentColor">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 9l3 3m0 0l-3 3m3-3H8m13 0a9 9 0 11-18 0 9 9 0 0118 0z"/>
</svg>
 &nbsp;Enviar Consolidado</button>
    </div>
    <div class="px-6 mx-auto">
        <DataTable class="table-auto" :columns="columms" :data="data_table" :options='{
            columnDefs: [
                { targets: "_all", className: "py-5 px-4 border-b text-sm text-left"}
            ],
            language:{
                lengthMenu: `<div class="text-sm py-3">Mostrar _MENU_ registros</div>`,
                search: `<label class="text-sm">Buscar: &nbsp;&nbsp;</label><input type="text" class="border border-gray-300 rounded px-2 py-1" placeholder="Buscar" />`,
                zeroRecords: `No hay registros que mostrar`,
                info: `<label class="text-sm py-3">Mostrando del <span class="font-bold text-gray-600">_START_</span> a <span class="font-bold text-gray-600">_END_</span> de <span class="font-bold text-gray-600">_TOTAL_</span> registros</label>`,
                paginate:{
                    first:`<label class="text-sm text-gray-600 font-bold py-3">Primero</label>`,
                    previous:`<label class="text-sm text-gray-600 font-bold py-3">Anterior</label>`,
                    next:`<label class="text-sm text-gray-600 font-bold py-3">Siguiente</label>`,
                    last:`<label class="text-sm text-gray-600 font-bold py-3">Último</label>`
                }
            },
        }'>
            <thead>
                <tr>
                    <th class="text-sm text-gray-600 text-center">Id</th>
                    <th class="text-sm text-gray-600 text-center">Name</th>
                    <th class="text-sm text-gray-600 text-center">Position</th>
                    <th class="text-sm text-gray-600 text-center">Salary</th>
                    <th class="text-sm text-gray-600 text-center">Start Date</th>
                    <th class="text-sm text-gray-600 text-center">Office</th>
                    <th class="text-sm text-gray-600 text-center">Extn</th>
                </tr>
            </thead>
        </DataTable>
    </div>
    <!-- -- -->
    <!-- -- -->
</template>
<script setup>
// Importando layouts
import Header from '../../layouts/Header.vue'
import DataTable from 'datatables.net-vue3';
import DataTablesCore from 'datatables.net';

DataTable.use(DataTablesCore)
//
</script>
<script>
import data from "../../../../dist/muestra.json"
export default {
    name: "BNotaServicios",
    components: { DataTable },
    data() {
        return {
            columms: [
                { data: 'id' },
                { data: 'name' },
                { data: 'position' },
                { data: 'salary' },
                { data: 'start_date' },
                { data: 'office' },
                { data: 'extn' },
            ],
            data_table: data["data"]
        }
    },
}
</script>
<style scope></style>
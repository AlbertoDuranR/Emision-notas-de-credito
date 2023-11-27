<template>
    <Header />
    <div class="container px-6 mx-auto block">
        <div class="flex items-center justify-center py-5"><span class="font-bold text-gray-600">CONSOLIDADO DE NOTAS DE
                CRÉDITO - FINANCIEROS</span></div>
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
                    <th class="text-sm text-gray-600 text-center">ID_NC</th>
                    <th class="text-sm text-gray-600 text-center">ID_DETALLE</th>
                    <th class="text-sm text-gray-600 text-center">ESTABLECIMIENTO</th>
                    <th class="text-sm text-gray-600 text-center">ESTADO</th>
                    <th class="text-sm text-gray-600 text-center">EMISION_COMPROBANTE</th>
                    <th class="text-sm text-gray-600 text-center">NRO</th>
                    <th class="text-sm text-gray-600 text-center">IMPORTE</th>
                    <th class="text-sm text-gray-600 text-center">DESCUENTO</th>
                    <th class="text-sm text-gray-600 text-center">TOTAL_DESCUENTO</th>
                    <th class="text-sm text-gray-600 text-center">BOLETEO</th>
                    <th class="text-sm text-gray-600 text-center">FECHA_SOLICITUD</th>
                    <th class="text-sm text-gray-600 text-center">SOLICITANTE</th>
                    <th class="text-sm text-gray-600 text-center">LABORA_EN</th>
                    <th class="text-sm text-gray-600 text-center">OPCIONES</th>
                </tr>
            </thead>
            <tbody>
  <tr v-for="item in lista_solicitudes" :key="item.ID_NC">
    <td class="text-sm text-gray-600 text-center">{{ item.ID_NC }}</td>
    <td class="text-sm text-gray-600 text-center">{{ item.ID_DETALLE }}</td>
    <td class="text-sm text-gray-600 text-center">{{ item.ESTABLECIMIENTO }}</td>
    <!-- ... otras columnas ... -->
    <td class="text-sm text-gray-600 text-center">
      <span :class="{'bg-yellow-500': item.ESTADO === 'PENDIENTE', 'bg-emerald-500': item.ESTADO === 'EMITIDO', 'bg-orange-500': item.ESTADO === 'ACTUALIZADO', 'bg-red-500': item.ESTADO === 'OBSERVADO'}" class="px-2 py-1 text-white rounded">
        {{ item.ESTADO }}
      </span>
    </td>
    <!-- ... otras columnas ... -->
    <td class="text-sm text-gray-600 text-center">{{ item.EMISION_COMPROBANTE }}</td>
    <td class="text-sm text-gray-600 text-center">{{ item.NRO }}</td>
    <td class="text-sm text-gray-600 text-center">{{ item.IMPORTE }}</td>
    <td class="text-sm text-gray-600 text-center">{{ item.DESCUENTO }}</td>
    <td class="text-sm text-gray-600 text-center">{{ item.TOTAL_DESCUENTO }}</td>
    <td class="text-sm text-gray-600 text-center">{{ item.BOLETEO }}</td>
    <td class="text-sm text-gray-600 text-center">{{ item.FECHA_SOLICITUD }}</td>
    <td class="text-sm text-gray-600 text-center">{{ item.SOLICITANTE }}</td>
    <td class="text-sm text-gray-600 text-center">{{ item.LABORA_EN }}</td>
    <td class="text-sm text-gray-600 text-center">
            <button @click="editarItem(item.ID_NC)" class="bg-blue-500 text-white px-2 py-1 mr-1">Editar</button>
            <button @click="eliminarItem(item.ID_NC)" class="bg-red-500 text-white px-2 py-1">Eliminar</button>
    </td>
  </tr>
</tbody>
        </DataTable>
    </div>
    <!-- -- -->
    <!-- -- -->
</template>
<script setup>
// Importando layouts
import Header from '../../layouts/Header.vue'
//
import DataTable from 'datatables.net-vue3';
import DataTablesCore from 'datatables.net';

DataTable.use(DataTablesCore)
</script>
<script>
import data from "../../../../dist/muestra.json"

export default {
    name: "CNotaFinancieros",
    components: { DataTable },
    props:{
        lista_solicitudes:Array
    },
    methods: {
    editarItem(item) {
      // Lógica para editar el elemento (puedes implementar según tus necesidades)
      console.log('Editar:', item);
      this.$inertia.visit(`/solicitud_nota_credito/financieros/edit/${item}/`)
    },
    eliminarItem(item) {
      // Lógica para eliminar el elemento (puedes implementar según tus necesidades)
      console.log('Eliminar:', item);
      
    }
  }
}
</script>
<style scope></style>
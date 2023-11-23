<template>
  <Header />
  <div class="container px-6 mx-auto block">
    <div class="flex items-center justify-center py-5">
      <span class="font-bold text-gray-600"
        >CONSOLIDADO DE NOTAS DE CRÉDITO - PUNTOS DE VENTA</span
      >
    </div>
  </div>
  <div class="px-4 flex justify-center">
    <button
      class="text-sm rounded-full bg-green-600 p-2 text-white font-bold flex"
      type="button"
    >
      <svg
        class="h-5 w-5 white"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M13 9l3 3m0 0l-3 3m3-3H8m13 0a9 9 0 11-18 0 9 9 0 0118 0z"
        />
      </svg>
      &nbsp;Enviar Consolidado
    </button>
  </div>
  <!-- Sección del DataTable -->
  <div class="px-6 mx-auto">
    <!-- Componente DataTable para mostrar una tabla -->
    <DataTable
      class="table-auto"
      :columns="columms"
      :data="data_table"
      :options="{
        columnDefs: [
          {
            targets: '_all',
            className: 'py-5 px-4 border-b text-sm text-left',
          },
        ],
        language: {
          lengthMenu: `<div class=&quot;text-sm py-3&quot;>Mostrar _MENU_ registros</div>`,
          search: `<label class=&quot;text-sm&quot;>Buscar: &nbsp;&nbsp;</label><input type=&quot;text&quot; class=&quot;border border-gray-300 rounded px-2 py-1&quot; placeholder=&quot;Buscar&quot; />`,
          zeroRecords: `No hay registros que mostrar`,
          info: `<label class=&quot;text-sm py-3&quot;>Mostrando del <span class=&quot;font-bold text-gray-600&quot;>_START_</span> a <span class=&quot;font-bold text-gray-600&quot;>_END_</span> de <span class=&quot;font-bold text-gray-600&quot;>_TOTAL_</span> registros</label>`,
          paginate: {
            first: `<label class=&quot;text-sm text-gray-600 font-bold py-3&quot;>Primero</label>`,
            previous: `<label class=&quot;text-sm text-gray-600 font-bold py-3&quot;>Anterior</label>`,
            next: `<label class=&quot;text-sm text-gray-600 font-bold py-3&quot;>Siguiente</label>`,
            last: `<label class=&quot;text-sm text-gray-600 font-bold py-3&quot;>Último</label>`,
          },
        },
      }"
    >
    <!-- Encabezados de la tabla -->
      <thead>
        <tr>
          <th class="text-sm text-gray-600 text-center">ID_NC</th>
          <th class="text-sm text-gray-600 text-center">ID_DETALLE</th>
          <th class="text-sm text-gray-600 text-center">CREADOR_USUARIO</th>
          <th class="text-sm text-gray-600 text-center">TIPO_COMPROBANTE</th>
          <th class="text-sm text-gray-600 text-center">FECHA_CREAR_NC</th>
          <th class="text-sm text-gray-600 text-center">ESTADO</th>
          <th class="text-sm text-gray-600 text-center">EMISION_COMPROBANTE</th>
          <th class="text-sm text-gray-600 text-center">NRO</th>
          <th class="text-sm text-gray-600 text-center">IMPORTE</th>
          <th class="text-sm text-gray-600 text-center">IMPORTE_PRODUCTOS</th>
          <th class="text-sm text-gray-600 text-center">METODO</th>
        </tr>
      </thead>
    </DataTable>
  </div>
  <!-- -- -->
  <!-- -- -->
</template>
<script setup>
// Importando layouts
import Header from "../../layouts/Header.vue";
import DataTable from "datatables.net-vue3";
import DataTablesCore from "datatables.net";

// Utiliza la biblioteca DataTable
DataTable.use(DataTablesCore);
//
</script>
<script>
//import data from "../../../../dist/muestra.json";

export default {
  name: "CNotaPDV",
  components: { DataTable },
  props: {
    lista_solicitudes: Array,
  },
  data() {
    return {
      columms: [
        { data: "ID_NC" },
        { data: "ID_DETALLE" },
        { data: "CREADOR_USUARIO" },
        { data: "TIPO_COMPROBANTE" },
        { data: "FECHA_CREAR_NC" },
        { data: "ESTADO" },
        { data: "EMISION_COMPROBANTE" },
        { data: "NRO" },
        { data: "IMPORTE" },
        { data: "IMPORTE_PRODUCTOS" },
        { data: "METODO" },
      ],
      data_table: this.lista_solicitudes,
    };
  },
  mounted() {},
  methods: {},
};
</script>
<style scope></style>

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
  <div class="px-6 mx-auto">
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
          <th class="text-sm text-gray-600 text-center">OPCIONES</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in lista_solicitudes" :key="item.ID_NC">
          <td class="text-sm text-gray-600 text-center">{{ item.ID_NC }}</td>
          <td class="text-sm text-gray-600 text-center">
            {{ item.ID_DETALLE }}
          </td>
          <td class="text-sm text-gray-600 text-center">
            {{ item.CREADOR_USUARIO }}
          </td>
          <td class="text-sm text-gray-600 text-center">
            {{ item.TIPO_COMPROBANTE }}
          </td>
          <td class="text-sm text-gray-600 text-center">
            {{ item.FECHA_CREAR_NC }}
          </td>
          <td class="text-sm text-gray-600 text-center">
            <span
              :class="{
                'bg-yellow-500': item.ESTADO === 'PENDIENTE',
                'bg-emerald-500': item.ESTADO === 'EMITIDO',
                'bg-orange-500': item.ESTADO === 'ACTUALIZADO',
                'bg-red-500': item.ESTADO === 'OBSERVADO',
              }"
              class="px-2 py-1 text-white rounded"
            >
              {{ item.ESTADO }}
            </span>
          </td>
          <td class="text-sm text-gray-600 text-center">
            {{ item.EMISION_COMPROBANTE }}
          </td>
          <td class="text-sm text-gray-600 text-center">{{ item.NRO }}</td>
          <td class="text-sm text-gray-600 text-center">{{ item.IMPORTE }}</td>
          <td class="text-sm text-gray-600 text-center">
            {{ item.IMPORTE_PRODUCTOS }}
          </td>
          <td class="text-sm text-gray-600 text-center">{{ item.METODO }}</td>
          <td class="text-sm text-gray-600 text-center">
            <button
              @click="editarItem(item.ID_NC,item.ID_DETALLE)"
              class="bg-blue-500 text-white px-2 py-1 mr-2"
            >
              Editar
            </button>
            <button
              @click="eliminarItem(item.ID_NC)"
              class="bg-red-500 text-white px-2 py-1"
            >
              Eliminar
            </button>
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
import Header from "../../layouts/Header.vue";
import DataTable from "datatables.net-vue3";
import DataTablesCore from "datatables.net";
import axios from "axios";

DataTable.use(DataTablesCore);
//
</script>

<script>
export default {
  name: "CNotaPDV",
  components: { DataTable },
  props: {
    lista_solicitudes: Array,
  },
  mounted() {
    // Imprimir datos en la consola
    //console.log(this.lista_solicitudes);
  },
  methods: {
    editarItem(item_nota, item_producto) {
  console.log("Editar:", item_nota, item_producto);
  
  this.$swal.fire({
    title: "Cargando la ventana de edición",
    text: "Espere por favor...",
    icon: "info",
    showConfirmButton: true,
    allowOutsideClick: false,
  });

  // Agregar las variables a la URL como parámetros de ruta
  this.$inertia.visit(`/solicitud_nota_credito/punto_venta/edit/${item_nota}/${item_producto}`);
}
,
    eliminarItem(item) {
      // Lógica para eliminar el elemento (puedes implementar según tus necesidades)
      //console.log("Eliminar item:", item);
      this.$swal
        .fire({
          title: "Advertencia!",
          text: "¿Estás seguro de eliminar?",
          icon: "warning",
          showCancelButton: true,
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33",
          confirmButtonText: "Sí, eliminar",
          cancelButtonText: "Cancelar",
        })
        .then((result) => {
          if (result.isConfirmed) {
            // Lógica para la confirmación
            axios
              .post("/solicitud_nota_credito/punto_venta/delete/", { id: item })
              .then((response) => {
                console.log(response);
                this.$swal.fire(
                  "Eliminado",
                  "El elemento ha sido eliminado.",
                  "success"
                );
                // Recargar la página completa después de eliminar
                location.reload();
              })
              .catch((err) => {
                console.log(err);
                Swal.fire({
                  title: "Error de Registro",
                  text: "Error al Eliminar datos, verificar los campos",
                  icon: "error",
                });
              });
          } else if (result.dismiss === this.$swal.DismissReason.cancel) {
            // Lógica para la cancelación
            this.$swal.fire(
              "Cancelado",
              "No se realizó ninguna acción.",
              "info"
            );
          }
        });
    },
  },
};
</script>
<style scope></style>

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
          <th class="text-sm text-gray-600 text-center">ID</th>
          <th class="text-sm text-gray-600 text-center">ID_DETALLE</th>
          <th class="text-sm text-gray-600 text-center">FECHA SOLICITUD</th>
          <th class="text-sm text-gray-600 text-center">USUARIO CREADOR</th>
          <th class="text-sm text-gray-600 text-center">SUCURSAL</th>
          <th class="text-sm text-gray-600 text-center">
            FECHA DE E.N.C. ORIGEN
          </th>
          <th class="text-sm text-gray-600 text-center">
            TIPO COMPROBANTE ORIGEN
          </th>
          <th class="text-sm text-gray-600 text-center">
            N° COMPROBANTE ORIGEN
          </th>
          <th class="text-sm text-gray-600 text-center">ESTADO</th>
          <th class="text-sm text-gray-600 text-center">OPCIONES</th>
          <th class="text-sm text-gray-600 text-center">METODO</th>
          <th class="text-sm text-gray-600 text-center">IMPORTE TOTAL</th>
          <th class="text-sm text-gray-600 text-center">ACEPTA</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in lista_solicitudes" :key="item.ID_NC">
          <td class="text-sm text-gray-600 text-center">{{ item.ID_NC }}</td>
          <td class="text-sm text-gray-600 text-center">
            {{ item.ID_DETALLE }}
          </td>
          <td class="text-sm text-gray-600 text-center">
            {{ item.FECHA_SOLICITUD }}
          </td>
          <td class="text-sm text-gray-600 text-center">
            {{ item.USUARIO_CREADOR }}
          </td>
          <td class="text-sm text-gray-600 text-center">
            {{ item.ESTABLECIMIENTO }}
          </td>
          <td class="text-sm text-gray-600 text-center">
            {{ item.FECHA_EMISION }}
          </td>
          <td class="text-sm text-gray-600 text-center">{{ item.TIPO }}</td>
          <td class="text-sm text-gray-600 text-center">
            {{ item.NRO_COMPROBANTE }}
          </td>
          <td class="text-sm text-gray-600 text-center">
            <span
              :class="{
                'bg-yellow-500': item.ESTADO === 'PENDIENTE',
                'bg-emerald-500': item.ESTADO === 'EMITIDO',
                'bg-orange-500': item.ESTADO === 'ACTUALIZADO',
                'bg-red-500': item.ESTADO === 'OBSERVADO',
                'bg-cyan-600': item.ESTADO == 'VALIDADO',
              }"
              class="px-2 py-1 text-white rounded"
            >
              {{ item.ESTADO }}
            </span>
          </td>
          <td class="text-sm text-gray-600 text-center">
            <button
              v-if="item.ESTADO !== 'VALIDADO'"
              @click="editarItem(item.ID_NC, item.ID_DETALLE)"
              class="bg-blue-0 text-white px-2 py-1 mr-2"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="16"
                width="16"
                viewBox="0 0 512 512"
              >
                <path
                  d="M441 58.9L453.1 71c9.4 9.4 9.4 24.6 0 33.9L424 134.1 377.9 88 407 58.9c9.4-9.4 24.6-9.4 33.9 0zM209.8 256.2L344 121.9 390.1 168 255.8 302.2c-2.9 2.9-6.5 5-10.4 6.1l-58.5 16.7 16.7-58.5c1.1-3.9 3.2-7.5 6.1-10.4zM373.1 25L175.8 222.2c-8.7 8.7-15 19.4-18.3 31.1l-28.6 100c-2.4 8.4-.1 17.4 6.1 23.6s15.2 8.5 23.6 6.1l100-28.6c11.8-3.4 22.5-9.7 31.1-18.3L487 138.9c28.1-28.1 28.1-73.7 0-101.8L474.9 25C446.8-3.1 401.2-3.1 373.1 25zM88 64C39.4 64 0 103.4 0 152V424c0 48.6 39.4 88 88 88H360c48.6 0 88-39.4 88-88V312c0-13.3-10.7-24-24-24s-24 10.7-24 24V424c0 22.1-17.9 40-40 40H88c-22.1 0-40-17.9-40-40V152c0-22.1 17.9-40 40-40H200c13.3 0 24-10.7 24-24s-10.7-24-24-24H88z"
                />
              </svg>
            </button>
            <button
              v-if="item.ESTADO !== 'VALIDADO'"
              @click="eliminarItem(item.ID_NC)"
              class="bg-red-0 text-white px-2 py-1"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="16"
                width="14"
                viewBox="0 0 448 512"
              >
                <path
                  d="M268 416h24a12 12 0 0 0 12-12V188a12 12 0 0 0 -12-12h-24a12 12 0 0 0 -12 12v216a12 12 0 0 0 12 12zM432 80h-82.4l-34-56.7A48 48 0 0 0 274.4 0H173.6a48 48 0 0 0 -41.2 23.3L98.4 80H16A16 16 0 0 0 0 96v16a16 16 0 0 0 16 16h16v336a48 48 0 0 0 48 48h288a48 48 0 0 0 48-48V128h16a16 16 0 0 0 16-16V96a16 16 0 0 0 -16-16zM171.8 50.9A6 6 0 0 1 177 48h94a6 6 0 0 1 5.2 2.9L293.6 80H154.4zM368 464H80V128h288zm-212-48h24a12 12 0 0 0 12-12V188a12 12 0 0 0 -12-12h-24a12 12 0 0 0 -12 12v216a12 12 0 0 0 12 12z"
                />
              </svg>
            </button>
          </td>
          <td class="text-sm text-gray-600 text-center">{{ item.METODO }}</td>
          <td class="text-sm text-gray-600 text-center">
            {{ item.MONTO_TOTAL }}
          </td>
          <td class="text-sm text-gray-600 text-center">{{ item.ACEPTA }}</td>
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
      this.$inertia.visit(
        `/solicitud_nota_credito/punto_venta/edit/${item_nota}/${item_producto}`
      );
    },
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

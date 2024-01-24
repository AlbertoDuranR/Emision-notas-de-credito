<template>
  <Header />
  <div class="container px-6 mx-auto block">
    <div class="flex items-center justify-center py-5">
      <span class="font-bold text-gray-600"
        >BANDEJA DE SOLICITUDES DE NOTAS DE CRÉDITO - PUNTOS DE VENTA</span
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
          <!-- <th class="text-sm text-gray-600 text-center">ID_DETALLE</th> -->
          <th class="text-sm text-gray-600 text-center">FECHA SOLICITUD</th>
          <th class="text-sm text-gray-600 text-center">USUARIO CREADOR</th>
          <th class="text-sm text-gray-600 text-center">SUCURSAL</th>
          <th class="text-sm text-gray-600 text-center">
            FECHA COMPROBANTE
          </th>
          <th class="text-sm text-gray-600 text-center">
            TIPO COMPROBANTE
          </th>
          <th class="text-sm text-gray-600 text-center">
            N° COMPROBANTE
          </th>
          <th class="text-sm text-gray-600 text-center">ESTADO</th>
          <th class="text-sm text-gray-600 text-center">OPCIONES</th>
          <th class="text-sm text-gray-600 text-center">FECHA N. DE CRÉDITO</th>
          <th class="text-sm text-gray-600 text-center">METODO</th>
          <th class="text-sm text-gray-600 text-center">IMPORTE N. DE CRÉDITO</th>
          <th class="text-sm text-gray-600 text-center">N° N. DE CRÉDITO</th>
          <th class="text-sm text-gray-600 text-center">ACEPTA</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in lista_solicitudes" :key="item.ID_NC">
          <td class="text-sm text-gray-600 text-center">{{ item.ID_NC }}</td>
          <!--
            <td class="text-sm text-gray-600 text-center">
            {{ item.ID_DETALLE }}
          </td>
          -->
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
                'bg-emerald-500': item.ESTADO === 'PENDIENTE',
                'bg-yellow-500': item.ESTADO === 'ACTUALIZADO',
                'bg-red-500': item.ESTADO === 'OBSERVADO',
                'bg-cyan-500': item.ESTADO == 'VALIDADO',
              }"
              class="px-2 py-1 text-white rounded"
            >
              {{ item.ESTADO }}
            </span>
            <button v-if="item.ESTADO === 'OBSERVADO'" class="bg-blue-0 text-white pl-2" @click="mostrarObservacion(item.OBSERVACION)">
              <svg xmlns="http://www.w3.org/2000/svg" height="16" width="20" viewBox="0 0 640 512"><path d="M88.2 309.1c9.8-18.3 6.8-40.8-7.5-55.8C59.4 230.9 48 204 48 176c0-63.5 63.8-128 160-128s160 64.5 160 128s-63.8 128-160 128c-13.1 0-25.8-1.3-37.8-3.6c-10.4-2-21.2-.6-30.7 4.2c-4.1 2.1-8.3 4.1-12.6 6c-16 7.2-32.9 13.5-49.9 18c2.8-4.6 5.4-9.1 7.9-13.6c1.1-1.9 2.2-3.9 3.2-5.9zM0 176c0 41.8 17.2 80.1 45.9 110.3c-.9 1.7-1.9 3.5-2.8 5.1c-10.3 18.4-22.3 36.5-36.6 52.1c-6.6 7-8.3 17.2-4.6 25.9C5.8 378.3 14.4 384 24 384c43 0 86.5-13.3 122.7-29.7c4.8-2.2 9.6-4.5 14.2-6.8c15.1 3 30.9 4.5 47.1 4.5c114.9 0 208-78.8 208-176S322.9 0 208 0S0 78.8 0 176zM432 480c16.2 0 31.9-1.6 47.1-4.5c4.6 2.3 9.4 4.6 14.2 6.8C529.5 498.7 573 512 616 512c9.6 0 18.2-5.7 22-14.5c3.8-8.8 2-19-4.6-25.9c-14.2-15.6-26.2-33.7-36.6-52.1c-.9-1.7-1.9-3.4-2.8-5.1C622.8 384.1 640 345.8 640 304c0-94.4-87.9-171.5-198.2-175.8c4.1 15.2 6.2 31.2 6.2 47.8l0 .6c87.2 6.7 144 67.5 144 127.4c0 28-11.4 54.9-32.7 77.2c-14.3 15-17.3 37.6-7.5 55.8c1.1 2 2.2 4 3.2 5.9c2.5 4.5 5.2 9 7.9 13.6c-17-4.5-33.9-10.7-49.9-18c-4.3-1.9-8.5-3.9-12.6-6c-9.5-4.8-20.3-6.2-30.7-4.2c-12.1 2.4-24.7 3.6-37.8 3.6c-61.7 0-110-26.5-136.8-62.3c-16 5.4-32.8 9.4-50 11.8C279 439.8 350 480 432 480z"/></svg>
            </button>
          </td>
          <td class="text-sm text-gray-600 text-center">
            <button
              v-show="item.ESTADO != 'VALIDADO'"
              @click="validar_item(item.ID_NC, item.NRO_COMPROBANTE)"
              class="bg-blue-0 text-white px-2 py-1"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="20"
                width="20"
                viewBox="0 0 512 512"
              >
                <path
                  d="M256 48a208 208 0 1 1 0 416 208 208 0 1 1 0-416zm0 464A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM369 209c9.4-9.4 9.4-24.6 0-33.9s-24.6-9.4-33.9 0l-111 111-47-47c-9.4-9.4-24.6-9.4-33.9 0s-9.4 24.6 0 33.9l64 64c9.4 9.4 24.6 9.4 33.9 0L369 209z"
                />
              </svg>
            </button>
            <button
              @click="observar_item(item.ID_NC)"
              class="bg-red-0 text-white px-2 py-1"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="20"
                width="20"
                viewBox="0 0 512 512"
              >
                <path
                  d="M256 48a208 208 0 1 1 0 416 208 208 0 1 1 0-416zm0 464A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM175 175c-9.4 9.4-9.4 24.6 0 33.9l47 47-47 47c-9.4 9.4-9.4 24.6 0 33.9s24.6 9.4 33.9 0l47-47 47 47c9.4 9.4 24.6 9.4 33.9 0s9.4-24.6 0-33.9l-47-47 47-47c9.4-9.4 9.4-24.6 0-33.9s-24.6-9.4-33.9 0l-47 47-47-47c-9.4-9.4-24.6-9.4-33.9 0z"
                />
              </svg>
            </button>
            <button
              v-show="item.ESTADO == 'VALIDADO'"
              @click="generar_nota_item(item.ID_NC)"
              class="bg-red-0 text-white px-2 py-1"
            >
              <svg xmlns="http://www.w3.org/2000/svg"
                height="22"
                width="22"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16c0 1.1.9 2 2 2h12a2 2 0 0 0 2-2V8l-6-6z"/>
                <path d="M14 3v5h5M16 13H8M16 17H8M10 9H8"/>
              </svg>
            </button>
          </td>
          <td class="text-sm text-gray-600 text-center">{{ item.FECHA_CREACION }}</td>
          <td class="text-sm text-gray-600 text-center">{{ item.METODO }}</td>
          <td class="text-sm text-gray-600 text-center">
            {{ item.MONTO_TOTAL }}
          </td>
          <td class="text-sm text-gray-600 text-center">{{ item.ACEPTA }}</td>
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
  name: "BNotaPDV",
  components: { DataTable },
  props: {
    lista_solicitudes: Array,
  },
  mounted() {
    // Imprimir datos en la consola
    //console.log(this.lista_solicitudes);
  },
  methods: {
    validar_item(itemNota, nroComprobante) {
      console.log("Editar:", itemNota);

      this.$swal
        .fire({
          title: "Advertencia!",
          text: "¿Estás seguro de validar la solicitud?",
          icon: "warning",
          showCancelButton: true,
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33",
          confirmButtonText: "Sí, validar",
          cancelButtonText: "Cancelar",
        })
        .then((result) => {
          if (result.isConfirmed) {
            // Lógica para la confirmación
            axios
              .post("/solicitud_nota_credito/punto_venta/validar/", {
                id: itemNota,
                nro_comprobante: nroComprobante
              })
              .then((response) => {
                console.log(response);
                this.$swal.fire(
                  "Validado",
                  "El elemento ha sido validado.",
                  "success"
                );
                // Recargar la página completa después de eliminar
                location.reload();
              })
              .catch((err) => {
                const msg_error = err.response.data.message
                this.$swal.fire({
                  title: "Error de Validación",
                  text: `${msg_error}`,
                  icon: "error",
                });
                location.reload();
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
    observar_item(item_nota) {
      this.$swal
        .fire({
          title: "Observar solicitud",
          text: "Ingresa la observación",
          icon: "warning",
          showCancelButton: true,
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33",
          confirmButtonText: "Sí, observar",
          cancelButtonText: "Cancelar",
          input: "textarea", // Cambiar a un campo de entrada de texto tipo textarea
          inputAttributes: {
            placeholder: "Describe la observación", // Título del campo de entrada
            rows: 3, // Altura del textarea (puedes ajustar este valor según tus necesidades)
          },
        })
        .then((result) => {
          if (result.isConfirmed) {
            console.log(result);
            // Verificar si se ingresó un texto
            if (result.value == "" || result.value === null) {
              this.$swal.fire({
                title: "Error",
                text: "Debes ingresar una razón para observar la solicitud.",
                icon: "error",
              });
            } else {
              // Lógica para la observación
              axios
                .post("/solicitud_nota_credito/punto_venta/observacion/", {
                  id: item_nota,
                  observacion: result.value, // Agregar la razón al objeto que envías al servidor
                })
                .then((response) => {
                  console.log(response);
                  this.$swal.fire(
                    "Observar",
                    "El elemento ha sido observado y será enviado a verificación.",
                    "success"
                  );
                  // Recargar la página completa después de observar
                  location.reload();
                })
                .catch((err) => {
                  console.log(err);
                  this.$swal.fire({
                    title: "Error de Registro",
                    text: "Error al Observar datos",
                    icon: "error",
                  });
                });
            }
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
    ver_observacion(observacion){
      this.swal.fire({
        title: 'Observación',
        text: observacion,
        icon: 'info',
      });
    },
    generar_nota_item(item_nota) {
      this.$swal
        .fire({
          title: "Advertencia!",
          text: "¿Estás seguro de Generar la Nota de Crédito?",
          icon: "warning",
          showCancelButton: true,
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33",
          confirmButtonText: "Sí, Generar",
          cancelButtonText: "Cancelar",
        })
        .then((result) => {
          if (result.isConfirmed) {
            // Lógica para la confirmación
            axios
              .post("/nota_credito/punto_venta/create/", {
                id: item_nota,
                estado: "VALIDADO",
              })
              .then((response) => {
                console.log(response);
                this.$swal.fire(
                  "CREADO",
                  "Nota de crédito CREADA",
                  "success"
                );
                // Recargar la página completa
                location.reload();
              })
              .catch((err) => {
                console.log(err);
                Swal.fire({
                  title: "Error de Registro",
                  text: "Error al crear la Nota de Crédito",
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
    mostrarObservacion(dato){
      this.$swal.fire({
        title: "Detalle de la observacion",
        text: dato,
        icon: "info",
        showConfirmButton: true,
        allowOutsideClick: false,
      });
    }
  },
};
</script>
<style scope></style>

<template>
    <Header />
    <div class="container px-6 mx-auto block">
        <div class="flex items-center justify-center py-5"><span class="font-bold text-gray-600">BANDEJA DE SOLICITUDES DE NOTAS DE
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
          <th class="text-sm text-gray-600 text-center">% DEL DESCUENTO</th>
          <th class="text-sm text-gray-600 text-center">DESCUENTO TOTAL</th>
          <th class="text-sm text-gray-600 text-center">ESTADO</th>
          <th class="text-sm text-gray-600 text-center">OPCIONES</th>
          <th class="text-sm text-gray-600 text-center">
            IMPORTE NOTA DE CREDITO
          </th>
          <th class="text-sm text-gray-600 text-center">ACEPTA</th>
        </tr>
            </thead>
            <tbody>
        <tr v-for="item in lista_solicitudes" :key="item.ID_NC">
          <td class="text-sm text-gray-600 text-center">{{ item.ID_NC }}</td>
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
          <td class="text-sm text-gray-600 text-center">
            {{ item.TIPO_COMPROBANTE }}
          </td>
          <td class="text-sm text-gray-600 text-center">
            {{ item.NUMERO_COMPROBANTE }}
          </td>
          <td class="text-sm text-gray-600 text-center">
            {{ item.DESCUENTO }}
          </td>
          <td class="text-sm text-gray-600 text-center">
            {{ item.TOTAL_DESCUENTO }}
          </td>
          <td class="text-sm text-gray-600 text-center">
            <span
              :class="{
                'bg-yellow-500': item.ESTADO === 'PENDIENTE',
                'bg-emerald-500': item.ESTADO === 'EMITIDO',
                'bg-orange-500': item.ESTADO === 'ACTUALIZADO',
                'bg-red-500': item.ESTADO === 'OBSERVADO',
                'bg-cyan-600': item.ESTADO == 'VALIDADO'
              }"
              class="px-2 py-1 text-white rounded"
            >
              {{ item.ESTADO }}
            </span>
          </td>
          <td class="text-sm text-gray-600 text-center">
            <button
              @click="validar_item(item.ID_NC)"
              class="bg-blue-0 text-white px-2 py-1 mr-2"
            >
            <svg 
                xmlns="http://www.w3.org/2000/svg" height="16" width="16" viewBox="0 0 512 512"><path d="M256 48a208 208 0 1 1 0 416 208 208 0 1 1 0-416zm0 464A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM369 209c9.4-9.4 9.4-24.6 0-33.9s-24.6-9.4-33.9 0l-111 111-47-47c-9.4-9.4-24.6-9.4-33.9 0s-9.4 24.6 0 33.9l64 64c9.4 9.4 24.6 9.4 33.9 0L369 209z"/>
            </svg>


            </button>
            <button
              @click="observar_item(item.ID_NC)"
              class="bg-red-0 text-white px-2 py-1"
            >
            <svg xmlns="http://www.w3.org/2000/svg" height="16" width="16" viewBox="0 0 512 512"><path d="M256 48a208 208 0 1 1 0 416 208 208 0 1 1 0-416zm0 464A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM175 175c-9.4 9.4-9.4 24.6 0 33.9l47 47-47 47c-9.4 9.4-9.4 24.6 0 33.9s24.6 9.4 33.9 0l47-47 47 47c9.4 9.4 24.6 9.4 33.9 0s9.4-24.6 0-33.9l-47-47 47-47c9.4-9.4 9.4-24.6 0-33.9s-24.6-9.4-33.9 0l-47 47-47-47c-9.4-9.4-24.6-9.4-33.9 0z"/></svg>
            </button>
          </td>
          <td class="text-sm text-gray-600 text-center">
            {{ item.IMPORTE_TOTAL }}
          </td>
          <td class="text-sm text-gray-600 text-center">{{ item.ACEPTA }}</td>

          <!-- ... otras columnas ... -->
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

import DataTable from 'datatables.net-vue3';
import DataTablesCore from 'datatables.net';
import axios from "axios";

DataTable.use(DataTablesCore)
//
</script>
<script>
import data from "../../../../dist/muestra.json"

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
    validar_item(item_nota) {
      console.log("Editar:", item_nota);

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
              .post("/solicitud_nota_credito/financieros/validar/", { id: item_nota, estado: 'VALIDADO' })
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
                console.log(err);
                Swal.fire({
                  title: "Error de Registro",
                  text: "Error al validar la solicitud",
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
    observar_item(item_nota) {
      // Lógica para eliminar el elemento (puedes implementar según tus necesidades)
      //console.log("Eliminar item:", item);
      this.$swal
        .fire({
          title: "Advertencia!",
          text: "¿Estás seguro de observar la solicitud?",
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
              .post("/solicitud_nota_credito/financieros/validar/", { id: item_nota, estado: 'OBSERVADO' })
              .then((response) => {
                console.log(response);
                this.$swal.fire(
                  "Observar",
                  "El elemento ha sido observado y sera enviado a verificacion.",
                  "success"
                );
                // Recargar la página completa después de eliminar
                location.reload();
              })
              .catch((err) => {
                console.log(err);
                Swal.fire({
                  title: "Error de Registro",
                  text: "Error al Observar datos",
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
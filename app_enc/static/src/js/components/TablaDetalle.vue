<template>
  <div class="px-5 mx-auto">
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
          <th class="text-sm text-gray-600 text-center">FECHA COMPROBANTE</th>
          <th class="text-sm text-gray-600 text-center">TIPO COMPROBANTE</th>
          <th class="text-sm text-gray-600 text-center">N° COMPROBANTE</th>
          <th class="text-sm text-gray-600 text-center">ESTADO</th>
          <th class="text-sm text-gray-600 text-center">OPCIONES</th>
          <th class="text-sm text-gray-600 text-center">FECHA N. DE CRÉDITO</th>
          <th class="text-sm text-gray-600 text-center">METODO</th>
          <th class="text-sm text-gray-600 text-center">
            IMPORTE N. DE CRÉDITO
          </th>
          <th class="text-sm text-gray-600 text-center">N° N. DE CRÉDITO</th>
          <th class="text-sm text-gray-600 text-center">ACEPTA</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in listaSolicitudes" :key="item.ID_NC">
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
            <button
              v-if="item.ESTADO === 'OBSERVADO'"
              class="bg-blue-0 text-white pl-2"
              @click="mostrarObservacion(item.OBSERVACION)"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="16"
                width="20"
                viewBox="0 0 640 512"
              >
                <path
                  d="M88.2 309.1c9.8-18.3 6.8-40.8-7.5-55.8C59.4 230.9 48 204 48 176c0-63.5 63.8-128 160-128s160 64.5 160 128s-63.8 128-160 128c-13.1 0-25.8-1.3-37.8-3.6c-10.4-2-21.2-.6-30.7 4.2c-4.1 2.1-8.3 4.1-12.6 6c-16 7.2-32.9 13.5-49.9 18c2.8-4.6 5.4-9.1 7.9-13.6c1.1-1.9 2.2-3.9 3.2-5.9zM0 176c0 41.8 17.2 80.1 45.9 110.3c-.9 1.7-1.9 3.5-2.8 5.1c-10.3 18.4-22.3 36.5-36.6 52.1c-6.6 7-8.3 17.2-4.6 25.9C5.8 378.3 14.4 384 24 384c43 0 86.5-13.3 122.7-29.7c4.8-2.2 9.6-4.5 14.2-6.8c15.1 3 30.9 4.5 47.1 4.5c114.9 0 208-78.8 208-176S322.9 0 208 0S0 78.8 0 176zM432 480c16.2 0 31.9-1.6 47.1-4.5c4.6 2.3 9.4 4.6 14.2 6.8C529.5 498.7 573 512 616 512c9.6 0 18.2-5.7 22-14.5c3.8-8.8 2-19-4.6-25.9c-14.2-15.6-26.2-33.7-36.6-52.1c-.9-1.7-1.9-3.4-2.8-5.1C622.8 384.1 640 345.8 640 304c0-94.4-87.9-171.5-198.2-175.8c4.1 15.2 6.2 31.2 6.2 47.8l0 .6c87.2 6.7 144 67.5 144 127.4c0 28-11.4 54.9-32.7 77.2c-14.3 15-17.3 37.6-7.5 55.8c1.1 2 2.2 4 3.2 5.9c2.5 4.5 5.2 9 7.9 13.6c-17-4.5-33.9-10.7-49.9-18c-4.3-1.9-8.5-3.9-12.6-6c-9.5-4.8-20.3-6.2-30.7-4.2c-12.1 2.4-24.7 3.6-37.8 3.6c-61.7 0-110-26.5-136.8-62.3c-16 5.4-32.8 9.4-50 11.8C279 439.8 350 480 432 480z"
                />
              </svg>
            </button>
          </td>
          <td class="text-sm text-gray-600 text-center">
            <button
              class="bg-red-0 text-white px-2 py-1 w-1/3"
              @click="getDatosSolicitud(item.ID_NC)"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="19"
                width="19"
                viewBox="0 0 512 512"
              >
                <path
                  d="M416 208c0 45.9-14.9 88.3-40 122.7L502.6 457.4c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L330.7 376c-34.4 25.2-76.8 40-122.7 40C93.1 416 0 322.9 0 208S93.1 0 208 0S416 93.1 416 208zM208 352a144 144 0 1 0 0-288 144 144 0 1 0 0 288z"
                />
              </svg>
            </button>
            <!-- INIT Bandeja -->
            <button
              v-show="item.ESTADO != 'VALIDADO' && props.tipo == 'bandeja'"
              @click="validarItem(item.ID_NC, item.NRO_COMPROBANTE)"
              class="bg-blue-0 text-white px-2 py-1 w-1/3"
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
              v-show="props.tipo == 'bandeja'"
              @click="observarItem(item.ID_NC)"
              class="bg-red-0 text-white px-2 py-1 w-1/3"
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
              v-show="item.ESTADO == 'VALIDADO' && props.tipo == 'bandeja'"
              @click="generarNotaItem(item.ID_NC)"
              class="bg-red-0 text-white px-2 py-1 w-1/3"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="22"
                width="22"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#000000"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path
                  d="M14 2H6a2 2 0 0 0-2 2v16c0 1.1.9 2 2 2h12a2 2 0 0 0 2-2V8l-6-6z"
                />
                <path d="M14 3v5h5M16 13H8M16 17H8M10 9H8" />
              </svg>
            </button>
            <!-- END Bandeja -->
            <!-- INIT consolidado -->
            <button
              v-if="item.ESTADO !== 'VALIDADO' && props.tipo == 'consolidado'"
              @click="editarItem(item.ID_NC, item.ID_DETALLE)"
              class="bg-blue-0 text-white px-2 py-1 w-1/3"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="19"
                width="19"
                viewBox="0 0 512 512"
              >
                <path
                  d="M441 58.9L453.1 71c9.4 9.4 9.4 24.6 0 33.9L424 134.1 377.9 88 407 58.9c9.4-9.4 24.6-9.4 33.9 0zM209.8 256.2L344 121.9 390.1 168 255.8 302.2c-2.9 2.9-6.5 5-10.4 6.1l-58.5 16.7 16.7-58.5c1.1-3.9 3.2-7.5 6.1-10.4zM373.1 25L175.8 222.2c-8.7 8.7-15 19.4-18.3 31.1l-28.6 100c-2.4 8.4-.1 17.4 6.1 23.6s15.2 8.5 23.6 6.1l100-28.6c11.8-3.4 22.5-9.7 31.1-18.3L487 138.9c28.1-28.1 28.1-73.7 0-101.8L474.9 25C446.8-3.1 401.2-3.1 373.1 25zM88 64C39.4 64 0 103.4 0 152V424c0 48.6 39.4 88 88 88H360c48.6 0 88-39.4 88-88V312c0-13.3-10.7-24-24-24s-24 10.7-24 24V424c0 22.1-17.9 40-40 40H88c-22.1 0-40-17.9-40-40V152c0-22.1 17.9-40 40-40H200c13.3 0 24-10.7 24-24s-10.7-24-24-24H88z"
                />
              </svg>
            </button>
            <button
              v-if="item.ESTADO !== 'VALIDADO' && props.tipo == 'consolidado'"
              @click="eliminarItem(item.ID_NC)"
              class="bg-red-0 text-white px-2 py-1 w-1/3"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="19"
                width="16"
                viewBox="0 0 448 512"
              >
                <path
                  d="M268 416h24a12 12 0 0 0 12-12V188a12 12 0 0 0 -12-12h-24a12 12 0 0 0 -12 12v216a12 12 0 0 0 12 12zM432 80h-82.4l-34-56.7A48 48 0 0 0 274.4 0H173.6a48 48 0 0 0 -41.2 23.3L98.4 80H16A16 16 0 0 0 0 96v16a16 16 0 0 0 16 16h16v336a48 48 0 0 0 48 48h288a48 48 0 0 0 48-48V128h16a16 16 0 0 0 16-16V96a16 16 0 0 0 -16-16zM171.8 50.9A6 6 0 0 1 177 48h94a6 6 0 0 1 5.2 2.9L293.6 80H154.4zM368 464H80V128h288zm-212-48h24a12 12 0 0 0 12-12V188a12 12 0 0 0 -12-12h-24a12 12 0 0 0 -12 12v216a12 12 0 0 0 12 12z"
                />
              </svg>
            </button>
            <!-- INIT consolidado -->
          </td>
          <td class="text-sm text-gray-600 text-center">
            {{ item.FECHA_CREACION }}
          </td>
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
  <ModalReview
    v-if="isOpen"
    @show-modal="closeModal"
    @close="closeModal"
    :open="isOpen"
    :detalleSolicitud="datos_detalle_solicitud"
  />
</template>

<script setup>
import { ref } from "vue";
import DataTable from "datatables.net-vue3";
import DataTablesCore from "datatables.net";
import Swal from "sweetalert2";
import axios from "axios";
import ModalReview from "../components/ModalReview";

DataTable.use(DataTablesCore);

const props = defineProps(["tipo", "listaSolicitudes"]);
console.log("props", props.tipo);
const emit = defineEmits([
  "editar-item",
  "eliminar-item",
  "validar_item",
  "observar_item",
  "generar_nota_item",
]);
const isOpen = ref(false);
const datos_detalle_solicitud = ref({});

const mostrarObservacion = (dato) => {
  Swal.fire({
    title: "Detalle de la observacion",
    text: dato,
    icon: "info",
    showConfirmButton: true,
    allowOutsideClick: false,
  });
};

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
const openModal = () => {
  isOpen.value = true;
};
const closeModal = () => {
  isOpen.value = false;
};

const getDatosSolicitud = async (idSol) => {
  try {
    console.log("entro activador modal");
    const response = await axios.get(
      `/solicitud_nota_credito/datos_solicitud/${idSol}`
    );
    console.log("response", response);
    if (response.status == 200) {
      openModal();
      datos_detalle_solicitud.value = response.data;
    }
  } catch (error) {
    console.log(error);
    this.$swal.fire({
      title: "ERROR",
      text: `No se tiene datos de esta solicitud: ${idSol}`,
      icon: "error",
    });
  }
};
</script>

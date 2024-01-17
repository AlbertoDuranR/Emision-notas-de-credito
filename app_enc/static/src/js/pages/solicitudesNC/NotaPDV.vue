<template>
  <Header />
  <div class="container px-6 mx-auto block">
    <div class="flex items-center justify-center py-5">
      <span class="font-bold text-gray-600"
        >SOLICITUD NOTA DE CRÉDITO - PUNTOS DE VENTA</span
      >
    </div>
    <div class="grid grid-cols-3 pt-2">
      <div class="flex"></div>
      <div class="block">
        <form
          action=""
          v-on:submit.prevent="enviarSolicitud()"
          :ref="formContainer"
        >
          <div class="px-4 flex justify-center">
            <button
              class="text-sm rounded-full bg-green-600 p-2 text-white font-bold flex"
              type="submit"
            >
              <svg
                class="h-5 w-5 text-white"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <line x1="12" y1="5" x2="12" y2="19" />
                <line x1="5" y1="12" x2="19" y2="12" />
              </svg>
              &nbsp;Solicitar NC
            </button>
          </div>
          <div class="py-2">
            <span class="text-sm font-bold text-gray-600 py-5"
              >Datos de Documentos de Origen</span
            >
          </div>
          <div class="space-y-1 py-2">
            <label class="text-sm">Fecha emisión del comprobantes:</label>
            <VueDatePicker
              v-model="datos_documento.fecha_emsion.date"
            
            ></VueDatePicker>
          </div>
          <div class="space-y-1 py-2">
            <label class="text-sm">N° Comprobante:</label>
            <input
              v-model="datos_documento.nro_comprobante"
              type="text"
              class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
            
              />
          </div>
          <div class="space-y-1 py-2">
            <label class="text-sm">Importe Total:</label>
            <input
              v-model="datos_documento.importe_total"
              type="text"
              class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
            
              />
          </div>
          <div class="pt-4 pb-1">
            <span class="text-sm font-bold text-gray-600 py-5"
              >Detalle de la Solicitud</span
            >
          </div>
          <div class="space-y-1 py-2">
            <label class="text-sm">Fecha emisión de la nota de crédito:</label>
            <VueDatePicker
              v-model="detalle_solicitud.fecha_solicitud.date"
            ></VueDatePicker>
          </div>
          <div class="space-y-1 py-2">
            <label class="text-sm">Motivo:</label>
            <input
              v-model="detalle_solicitud.motivo"
              type="text"
              class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
            
              />
          </div>
          <div class="space-y-1 py-2">
            <label class="text-sm">Justificación:</label>
            <textarea
              v-model="detalle_solicitud.justificacion"
              name="textarea-name"
              rows="5"
              class="focus:shadow-soft-primary-outline min-h-unset text-sm leading-5.6 ease-soft block h-auto w-full appearance-none rounded-lg border border-solid border-gray-300 bg-white bg-clip-padding px-3 py-2 font-normal text-gray-700 outline-none transition-all placeholder:text-gray-500 focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500"
            
              ></textarea>
          </div>
          <div class="space-y-1 py-2">
            <label class="text-sm">Método:</label>
            <fieldset class="blocks">
              <div class="my-8"></div>
              <input
                id="draft"
                class="sr-only my-5 peer/draft"
                type="radio"
                name="status"
                value="Total"
                v-model="detalle_solicitud.metodo"
                checked
              />
              <label
                class="p-5 mx-3 my-5 bg-white border rounded-lg cursor-pointer peer-checked/draft:border-sky-500 hover:border-sky-500 peer-checked/draft:border-sky-500 peer-checked/draft:ring-1 peer-checked/draft:bg-sky-100"
                for="draft"
              >
                Total
              </label
              >
              <input
                id="published"
                class="sr-only peer/published"
                type="radio"
                name="status"
                value="Parcial"
                v-model="detalle_solicitud.metodo"
                @click="getProductosDelComprobante"
              />
              <label
                class="p-5 mx-3 my-5 bg-white border rounded-lg cursor-pointer peer-checked/published:border-sky-500 hover:border-sky-500 peer-checked/published:border-sky-500 peer-checked/published:ring-1 peer-checked/published:bg-sky-100"
                for="published"
              >
                Parcial
              </label>
              <div class="my-8"></div>
              <div
                class="hidden flex items-center justify-center peer-checked/draft:block"
              ></div>
              <div class="hidden peer-checked/published:block">
                <div class="space-y-1 py-2">
                  <div id="app" class="relative">
                    <div>
                      <label class="typo__label text-sm">Producto:</label>
                      <multiselect
                        v-model="metodo_parcial_productos.value"
                        id="multiselect"
                        :options="productos"
                        :multiple="true"
                        :close-on-select="false"
                        :clear-on-select="false"
                        :preserve-search="true"
                        placeholder="Seleccionar producto..."
                        label="Product"
                        track-by="Product"
                        @update:modelValue="handleSelectionChange"
                      >
                      </multiselect>
                      <div class="py-2"></div>
                      <div
                        v-for="(val, index) in metodo_parcial_productos.value"
                        :key="index"
                        class="py-2"
                      >
                        <div
                          class="text-center text-sm font-bold bg-gray-600 text-white rounded-lg py-1"
                        >
                          {{
                            val["ProductNumber"] +
                            " - " +
                            val["ProductDescription"]
                          }}
                        </div>
                        <div class="flex">
                          <div class="space-y-1 py-2 px-2">
                            <label class="text-sm text-center">Unidad:</label>
                            <multiselect
                              v-model="
                                metodo_parcial_productos.value[index].SalesUnitSymbol
                              "
                              id="multiselect_unidad"
                              :options="
                                metodo_parcial_productos.unidad.unidades
                              "
                              :preserve-search="true"
                              placeholder="Unidad"
                              label="UnitSymbol"
                              track-by="UnitSymbol"
                            >
                            </multiselect>
                          </div>
                          <div class="space-y-1 py-2 px-2">
                            <label class="text-sm">Precio:</label>
                            {{val["InvoicedQuantity"]}}{{val["SalesUnitSymbol"]}}{{val["SalesPrice"]}}
                            <input
                              type="text"
                              v-model="
                                metodo_parcial_productos.value[index].SalesPrice
                              "
                              class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
                              @input="handleInputChange(index)"
                              />
                          </div>
                          <div class="space-y-1 py-2 px-2">
                            <label class="text-sm">Cantidad:</label>
                            <input
                              type="text"
                              v-model="
                                metodo_parcial_productos.value[index].InvoicedQuantity
                              "
                              class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
                              @input="handleInputChange(index)"
                              />
                          </div>
                          <div class="space-y-1 py-2 px-2">
                            <label class="text-sm">Monto Total:</label>
                            <input
                              v-model="
                                metodo_parcial_productos.value[index].Total
                              "
                              type="text"
                              class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </fieldset>
          </div>
        </form>
      </div>
    </div>
  </div>
  <notifications />
</template>
<script setup>
import { ref, onMounted, onUpdated } from 'vue';
import axios from 'axios';
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
import Multiselect from "vue-multiselect";
import { notify } from "@kyvg/vue3-notification";
import { useLoading } from "vue3-loading-overlay";
import "vue3-loading-overlay/dist/vue3-loading-overlay.css";
import Swal from 'sweetalert2'

import Header from "../../layouts/Header.vue";


const props = defineProps(['unidades', '_token'])
const formContainer = ref(null);
const fullPage = ref(true);
const csrf_token = ref('');
const datos_documento = ref({
  fecha_emsion: {
    date: null,
  },
  nro_comprobante: '',
  importe_total: '',
});
const detalle_solicitud = ref({
  fecha_solicitud: {
    date: null,
  },
  motivo: '',
  justificacion: '',
  metodo: 'Total',
});
const productos = ref([]);
// const productos = ref([
//     {
//         "ProductNumber": 101764,
//         "ProductDescription": "NAKAMITO SAZONADOR GLUTANO MONOSODICO 500G",
//         "Product": "101764 - NAKAMITO SAZONADOR GLUTANO MONOSODICO 500G",
//         "InvoicedQuantity": 1,
//         "SalesPrice": 6.2,
//         "SalesUnitSymbol": "U"
//     },
//     {
//         "ProductNumber": 101765,
//         "ProductDescription": "NAKAMITO 00G",
//         "Product": "101765 - NAKAMITO G",
//         "InvoicedQuantity": 2,
//         "SalesPrice": 6,
//         "SalesUnitSymbol": "U"
//     },
// ]);
console.log('productos.length', productos.length)
const metodo_parcial_productos = ref({
  products: [],
  value: null,
  // selectedOptions: [],
  unidad: {
    unidades: props.unidades,
    valores: [],
    // selectedOptions: [],
  },
  precio: {
    // valores: Array.from({ length: 10 }, () => ({
    //   value: null,
    // })),
    valores: []
  },
  cantidad: {
    valores: [],
  },
  monto_total: {
    valores: [],
  },
});

const enviarSolicitud = () => {
  console.log(metodo_parcial_productos.value);
  const send_data = {
    "datos_documento": datos_documento.value,
    "detalle_solicitud": detalle_solicitud.value,
    "metodo_parcial_productos": metodo_parcial_productos.value
  }
  console.log('enviar solcitud 1::', send_data)
  const jsonString = JSON.stringify(send_data);
  console.log('enviarr Solicitud', jsonString);
  // axios
  //   .post('/solicitud_nota_credito/punto_venta/create/', jsonString)
  //   .then((response) => {
  //     location.reload();
  //     notify({
  //       title: 'Registro Exitoso',
  //       text: '' + response.data.message,
  //     });
  //   })
  //   .catch((err) => {
  //     console.log(err);
  //     notify({
  //       title: 'Error de Registro',
  //       text: 'Error al guardar datos verificar los campos',
  //       type: 'error',
  //     });
  //   });
};

const refreshLoading = () => {
  const onCancel = () => {
    console.log('User cancelled the loader.');
  };
  let loader = useLoading();
  loader.show({
    container: fullPage.value ? null : formContainer.value,
    canCancel: true,
    onCancel: onCancel,
  });
  setTimeout(() => {
    loader.hide();
  }, 2000);
};

const getProductosDelComprobante = async () => {
  console.log('Click, nro_comprobante:', datos_documento.value.nro_comprobante);
  // return
  if (datos_documento.value.nro_comprobante == '') {
    Swal.fire({
      title: 'Verificar Campos',
      text: `N° Comprobante No puede estar Vacío o no existe`,
      icon: 'warning',
    });
    return;
  }
  try {
    const response = await axios.get(`/comprobante/detalle_comprobante/${datos_documento.value.nro_comprobante}`);
    // console.log('obtenerProductss:::', response.data);
    productos.value = response.data;
    console.log('metodo_parcial_productos.productos:::', productos.value);
  } catch (error) {
    console.error('Error al obtener productos del comprobante', error);
    Swal.fire({
      title: 'Verificar Campos',
      text: 'Error al obtener productos del comprobante',
      icon: 'error',
    });
  }
};

onMounted(() => {
  console.log('onMounted')
  // csrf_token = document.querySelector(
  //     "[name=csrfmiddlewaretoken]"
  //   ).value;
}),

onUpdated(() => {
  console.log('onUpdated')
  console.log('Metodo_parcial_productos.value: ', metodo_parcial_productos.value, metodo_parcial_productos.value.precio.valores[0]?.value)
})

const handleSelectionChange = (value) => {
  value.forEach((element, index) => {
    console.log('for::', index, element)
    metodo_parcial_productos.value.value[index]["Total"] = (element.InvoicedQuantity * element.SalesPrice).toString()
    // metodo_parcial_productos.value.value[index]["SalesUnitSymbol"] = {UnitSymbol: element.SalesUnitSymbol} Revisar si sirve esto para cambiar Unidad
  });
  // const precio = metodo_parcial_productos.value.precio.valores[0]?.value
  // console.log('start SelectProduct', precio)
  // metodo_parcial_productos.value.precio.valores[0].value='20'
}
const handleInputChange = (index) => {
  console.log("hanldeInputChange"," metodo_parcial_productos.value[index].InvoicedQuantity", index, metodo_parcial_productos.value.value[index].InvoicedQuantity)
  metodo_parcial_productos.value.value[index].Total = metodo_parcial_productos.value.value[index].InvoicedQuantity * metodo_parcial_productos.value.value[index].SalesPrice
}

refreshLoading();
</script>

<style scope>
@import "https://unpkg.com/vue-multiselect@2.1.6/dist/vue-multiselect.min.css";
</style>

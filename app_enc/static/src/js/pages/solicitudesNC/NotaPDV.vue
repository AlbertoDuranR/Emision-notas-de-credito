<template>
  <Header />
  <div class="container px-6 mx-auto block">
    <div class="flex items-center justify-center py-5">
      <span class="font-bold text-gray-600"
        >SOLICITUD NOTA DE CRÉDITO - PUNTOS DE VENTA</span
      >
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-3 pt-2">
      <div class="flex"></div>
      <div class="block mb-10">
        <form
          action=""
          v-on:submit.prevent="enviarSolicitud()"
          :ref="formContainer"
        >
          <loading-overlay
            :active="isLoading"
            :can-cancel="true"
            :color="'#dc2626'"
          >
          </loading-overlay>
          <div class="py-2">
            <span class="text-sm font-bold text-gray-600 py-5"
              >Datos de Documentos de Origen</span
            >
          </div>
          <div class="space-y-1 py-2">
            <label class="text-sm">N° Comprobante:</label>
            <input
              v-model="datos_documento.nro_comprobante"
              type="text"
              class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
              @blur="getDatosDelComprobante"
            />
          </div>
          <div class="space-y-1 py-2">
            <label class="text-sm">Fecha emisión del comprobantes:</label>
            <VueDatePicker
              v-model="datos_documento.fecha_emision.date"
              required
            ></VueDatePicker>
          </div>
          <div class="space-y-1 py-2">
            <label class="text-sm">Importe Total:</label>
            <input
              v-model="datos_documento.importe_total"
              type="number"
              step="any"
              placeholder="0.00"
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
              required
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
              required
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
                value="total"
                v-model="detalle_solicitud.metodo"
                checked
              />
              <label
                class="p-5 mx-3 my-5 bg-white border rounded-lg cursor-pointer peer-checked/draft:border-sky-500 hover:border-sky-500 peer-checked/draft:border-sky-500 peer-checked/draft:ring-1 peer-checked/draft:bg-sky-100"
                for="draft"
              >
                Total
              </label>
              <input
                id="published"
                class="sr-only peer/published"
                type="radio"
                name="status"
                value="parcial"
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
                <div class="space-y-1 py-2 relative">
                  <loading-overlay
                    :active="isLoadingProductos"
                    :can-cancel="true"
                    :is-full-page="false"
                    :color="'#dc2626'"
                  >
                  </loading-overlay>
                  <div id="app" class="relative">
                    <div>
                      <label class="typo__label text-sm">Producto:</label>
                      <multiselect
                        v-model="metodo_parcial_productos.selected_products"
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
                        v-for="(
                          product, index
                        ) in metodo_parcial_productos.selected_products"
                        :key="index"
                        class="py-2"
                      >
                        <div
                          class="text-center text-sm font-bold bg-gray-600 text-white rounded-lg py-1"
                        >
                          {{
                            product["ProductNumber"] +
                            " - " +
                            product["ProductDescription"]
                          }}
                        </div>
                        <div class="columns-4">
                          <div class="space-y-1 py-2 px-2">
                            <label class="text-sm">Cantidad:</label>
                            <input
                              type="number"
                              v-model="product.InvoicedQuantity"
                              class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
                              @input="handleInputChange(index)"
                            />
                          </div>
                          <div class="space-y-1 py-2 px-2">
                            <label class="text-sm text-center">Unidad:</label>
                            <multiselect
                              id="multiselect_unidad"
                              v-model="product.SalesUnitSymbol"
                              :options="unidades"
                              :close-on-select="true"
                              :show-labels="false"
                              placeholder="Unidad"
                            >
                            </multiselect>
                          </div>
                          <div class="space-y-1 py-2 px-2">
                            <label class="text-sm">Precio:</label>
                            <input
                              type="number"
                              step="any"
                              v-model="product.SalesPrice"
                              class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
                              @input="handleInputChange(index)"
                            />
                          </div>
                          <div class="space-y-1 py-2 px-2">
                            <label class="text-sm">Monto Total:</label>
                            <input
                              v-model="product.Total"
                              type="number"
                              step="any"
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
          <div class="px-2 flex justify-center">
            <button
              class="w-60 rounded-full bg-green-600 py-3 text-white font-bold flex justify-center hover:opacity-70"
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
                <path
                  d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"
                ></path>
                <polyline points="17 21 17 13 7 13 7 21"></polyline>
                <polyline points="7 3 7 8 15 8"></polyline>
              </svg>
              &nbsp;Solicitar NC
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
  <notifications />
</template>
<script setup>
import { ref, onMounted, onUpdated } from "vue";
import axios from "axios";

import Header from "../../layouts/Header.vue";
import LoadingOverlay from "vue3-loading-overlay";
import Multiselect from "vue-multiselect";
import Swal from "sweetalert2";
import VueDatePicker from "@vuepic/vue-datepicker";

import { notify } from "@kyvg/vue3-notification";
import { useLoading } from "vue3-loading-overlay";
import convertirFormatoFecha from "../../utils";

import "@vuepic/vue-datepicker/dist/main.css";
import "vue3-loading-overlay/dist/vue3-loading-overlay.css";

const props = defineProps(["unidades", "_token"]);
const isLoadingProductos = ref(false);
const isLoading = ref(false);
const formContainer = ref(null);
const fullPage = ref(true);
const csrf_token = ref("");
const datos_documento = ref({
  fecha_emision: {
    date: null,
  },
  nro_comprobante: "",
  importe_total: "",
});
const detalle_solicitud = ref({
  fecha_solicitud: {
    date: null,
  },
  motivo: "",
  justificacion: "",
  metodo: "total",
});

const unidades = props.unidades.map((objUnidad) => objUnidad.UnitSymbol); // ['U', 'LTR.']
const productos = ref([]);
const metodo_parcial_productos = ref({
  products: [],
  selected_products: null,
});
/**
  Ex. select_product
    {
      "ProductNumber": 101764,
      "ProductDescription": "NAKAMITO SAZONADOR GLUTANO MONOSODICO 500G",
      "Product": "101764 - NAKAMITO SAZONADOR GLUTANO MONOSODICO 500G",
      "InvoicedQuantity": 1,
      "SalesPrice": 6.2,
      "SalesUnitSymbol": "U"
    }
*/

const enviarSolicitud = () => {
  let metodoParcialProductos = [];
  if (detalle_solicitud.value.metodo == "parcial") {
    metodoParcialProductos = metodo_parcial_productos.value.selected_products;
  }
  const send_data = {
    datos_documento: datos_documento.value,
    detalle_solicitud: detalle_solicitud.value,
    metodo_parcial_productos: metodoParcialProductos,
  };
  const jsonString = JSON.stringify(send_data);
  console.log("enviarr Solicitud", jsonString);
  // return
  isLoading.value = true;
  axios
    .post("/solicitud_nota_credito/punto_venta/create/", jsonString)
    .then((response) => {
      location.reload();
      notify({
        title: "Registro Exitoso",
        text: "" + response.data.message,
      });
    })
    .catch((err) => {
      console.log(err);
      notify({
        title: "Error de Registro",
        text: "Error al guardar datos verificar los campos",
        type: "error",
      });
    });
};

const refreshLoading = () => {
  const onCancel = () => {
    console.log("User cancelled the loader.");
  };
  let loader = useLoading();
  loader.show({
    container: fullPage.value ? null : formContainer.value,
    canCancel: true,
    onCancel: onCancel,
  });
  setTimeout(() => {
    loader.hide();
  }, 1000);
};

const getDatosDelComprobante = async () => {
  if (datos_documento.value.nro_comprobante == "") {
    notify({
      title: "Verificar Campos",
      text: "Ingresar Nro Comprobante",
      type: "warn",
    });
    return;
  }

  isLoading.value = true;
  try {
    const response = await axios.get(
      `/comprobante/get_datos_comprobante/${datos_documento.value.nro_comprobante}`
    );
    if (response.status == 200 && response.data[0]) {
      datos_documento.value.importe_total = response.data[0].TotalInvoiceAmount;
      const fechaEmision = response.data[0].InvoiceDate;
      datos_documento.value.fecha_emision.date =
        convertirFormatoFecha(fechaEmision);
    }
    console.log("fechaFormateada: ", datos_documento.value.fecha_emision.date);
  } catch (error) {
    Swal.fire({
      title: "Verificar Campos",
      text: `${error.response.data.error}`,
      icon: "error",
    });
    datos_documento.value.importe_total = "";
    datos_documento.value.fecha_emision.date.importe_total = null;
  } finally {
    isLoading.value = false;
  }
};

const getProductosDelComprobante = async () => {
  if (datos_documento.value.nro_comprobante == "") {
    notify({
      title: "Verificar Campos",
      text: "N° Comprobante no puede estar Vacío",
      type: "warn",
    });
    return;
  }
  isLoadingProductos.value = true;
  try {
    const response = await axios.get(
      `/comprobante/detalle_comprobante/${datos_documento.value.nro_comprobante}`
    );
    productos.value = response.data;
  } catch (error) {
    Swal.fire({
      title: "Verificar Campos",
      text: `${error.response.data.error}`,
      icon: "error",
    });
    productos.value = [];
  } finally {
    isLoadingProductos.value = false;
  }
};

onMounted(() => {
  csrf_token.value = document.querySelector("[name=csrfmiddlewaretoken]").value;
}),
  onUpdated(() => {
    console.log("onUpdated");
    console.log("Metodo_parcial_productos: ", metodo_parcial_productos);
    console.log("datos_documento: ", datos_documento);
  });

const handleSelectionChange = (value) => {
  value.forEach(
    (element, index) =>
      (metodo_parcial_productos.value.selected_products[index]["Total"] = (
        element.InvoicedQuantity * element.SalesPrice
      ).toFixed(2))
  );
};
const handleInputChange = (index) => {
  metodo_parcial_productos.value.selected_products[index].Total = (
    metodo_parcial_productos.value.selected_products[index].InvoicedQuantity *
    metodo_parcial_productos.value.selected_products[index].SalesPrice
  ).toFixed(2);
};

refreshLoading();
</script>

<style scope>
@import "https://unpkg.com/vue-multiselect@2.1.6/dist/vue-multiselect.min.css";
</style>

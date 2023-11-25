<template>
  <Header />
  <div class="container px-6 mx-auto block">
    <div class="flex items-center justify-center py-5">
      <span class="font-bold text-gray-600"
        >ACTUALIZAR - SOLICITUD NOTA DE CRÉDITO - PUNTOS DE VENTA - N°
        {{ id }}</span
      >
    </div>
    <form
      action=""
      v-on:submit.prevent="enviarSolicitud()"
      :ref="formContainer"
    >
      <div class="col-span-2 flex justify-center">
        <div class="px-4">
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
            &nbsp;Actualizar NC
          </button>
        </div>
      </div>

      <div class="grid grid-cols-3 gap-10 pt-2">
        <!-- Columna 1: Datos de Documentos de Origen -->
        <div class="col-span-1 text-cente px-5">
          <div class="py-2">
            <input
              type="text"
              class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
              v-model="datos_documento.id_nc"
            />
            <input
              type="text"
              class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
              v-model="datos_documento.id_detalle_nc"
            />
            <span class="text-sm font-bold text-gray-600 py-5 textcenter"
              >Datos de Documentos de Origen</span
            >
            <div class="space-y-1 py-2">
              <label class="text-sm">Fecha emisión del comprobantes:</label>
              <VueDatePicker
                v-model="datos_documento.fecha_emsion.date"
              ></VueDatePicker>
            </div>
            <div class="space-y-1 py-2">
              <label class="text-sm">Nro. Comprobante:</label>
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
          </div>
          <!-- ... Código existente para Datos de Documentos de Origen ... -->
        </div>

        <!-- Columna 2: Detalle de la Solicitud -->
        <div class="col-span-1 text-cente px-5">
          <div class="py-2">
            <span class="text-sm font-bold text-gray-600 py-5 r"
              >Detalle de la Solicitud</span
            >
            <div class="space-y-1 py-2">
              <label class="text-sm"
                >Fecha emisión de la nota de crédito:</label
              >
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
                  >Total</label
                >
                <input
                  id="published"
                  class="sr-only peer/published"
                  type="radio"
                  name="status"
                  value="Parcial"
                  v-model="detalle_solicitud.metodo"
                />
                <label
                  class="p-5 mx-3 my-5 bg-white border rounded-lg cursor-pointer peer-checked/published:border-sky-500 hover:border-sky-500 peer-checked/published:border-sky-500 peer-checked/published:ring-1 peer-checked/published:bg-sky-100"
                  for="published"
                  >Parcial</label
                >
                <div class="my-8"></div>
                <div
                  class="hidden flex items-center justify-center peer-checked/draft:block"
                ></div>
                <div class="hidden peer-checked/published:block">
                  <div class="space-y-1 py-2">
                    <div id="app" class="relative">
                      <!-- <select v-model="selectedOptions" multiple id="multiselect"
                                              class="block w-full px-4 py-2 pr-8 leading-tight bg-white border border-gray-300 rounded appearance-none focus:outline-none focus:bg-white focus:border-gray-500">
                                              <option v-for="option in options" :key="option" :value="option">{{ option }}</option>
                                          </select>
                                          <div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
                                              <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor"
                                                  viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                      d="M15 19l-7-7 7-7"></path>
                                              </svg>
                                          </div> -->
                      <div>
                        <label class="typo__label text-sm">Producto:</label>
                        <multiselect
                          v-model="metodo_parcial_productos.value"
                          id="multiselect"
                          :options="metodo_parcial_productos.products"
                          :multiple="true"
                          :close-on-select="false"
                          :clear-on-select="false"
                          :preserve-search="true"
                          placeholder="Seleccionar producto..."
                          label="Product"
                          track-by="Product"
                        >
                          <!-- <template slot="selection" slot-scope="{ values, search, isOpen }"><span
                                                          class="multiselect__single" v-if="values.length" v-show="!isOpen">{{
                                                              values.length }} options selected</span></template> -->
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
                                  metodo_parcial_productos.unidad.valores[index]
                                    .value
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
                              <input
                                type="text"
                                v-model="
                                  metodo_parcial_productos.precio.valores[index]
                                    .value
                                "
                                class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
                              />
                            </div>
                            <div class="space-y-1 py-2 px-2">
                              <label class="text-sm">Cantidad:</label>
                              <input
                                type="text"
                                v-model="
                                  metodo_parcial_productos.cantidad.valores[
                                    index
                                  ].value
                                "
                                class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
                              />
                            </div>
                            <div class="space-y-1 py-2 px-2">
                              <label class="text-sm">Monto Total:</label>
                              <input
                                v-model="
                                  metodo_parcial_productos.monto_total.valores[
                                    index
                                  ].value
                                "
                                type="text"
                                class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
                              />
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <!-- 
                                      <div id="etiquetas" class="mt-4 flex flex-wrap">
                                          <span v-for="option in selectedOptions" :key="option"
                                              class="inline-flex items-center px-2 py-1 mr-2 mt-2 text-sm font-medium text-gray-700 bg-gray-200 rounded-full">
                                              {{ value }}
                                          </span>
                                      </div> -->
                  </div>
                </div>
              </fieldset>
            </div>
          </div>
          <!-- ... Código existente para Detalle de la Solicitud ... -->
        </div>

        <!-- Columna 3: Detalle de los productos -->
        <div class="col-span-1 text-cente px-5">
          <div class="py-2">
            <span class="text-sm font-bold text-gray-600 py-5 r"
              >Productos seleccionados</span
            >
            <table class="w-full mt-4 border-t border-gray-300">
      <thead>
        <tr>
          <th class="py-2 px-4 border-b">Codigo</th>
          <th class="py-2 px-4 border-b">Descripción</th>
          <th class="py-2 px-4 border-b">Unidad</th>
          <th class="py-2 px-4 border-b">Precio</th>
          <th class="py-2 px-4 border-b">Cantidad</th>
          <th class="py-2 px-4 border-b">Monto Total</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(val, index) in lista_productosEdit" :key="index">
          <td class="py-2 px-4 border-b">{{ val.PRODUCTO_CODIGO }}</td>
          <td class="py-2 px-4 border-b">{{ val.PRODUCTO_DESCCRIPCION }}</td>
          <td class="py-2 px-4 border-b">{{ val.PRODUCTO_UNIDAD }}</td>
          <td class="py-2 px-4 border-b">{{ val.PRODUCTO_PRECIO }}</td>
          <td class="py-2 px-4 border-b">{{ val.PRODUCTO_CANTIDAD }}</td>
          <td class="py-2 px-4 border-b">{{ val.PRODUCTO_MONTO }}</td>
        </tr>
      </tbody>
    </table>
          </div>
        </div>
      </div>
    </form>
  </div>
  <notifications />
</template>

<script setup>
// Importando layouts
import Header from "../../layouts/Header.vue";
//
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
//
import Multiselect from "vue-multiselect";
//
import axios from "axios";
//
import { notify } from "@kyvg/vue3-notification";
//
import { ref } from "vue";
// Import the method.
import { useLoading } from "vue3-loading-overlay";
// Import stylesheet
import "vue3-loading-overlay/dist/vue3-loading-overlay.css";
// Init plugin

// const fullPage = ref(true);
// let formContainer = ref(null);
</script>
<script>
export default {
  name: "NotaPDVEdit",
  components: { VueDatePicker, Multiselect },
  props: {
    productos: Array,
    unidades: Array,
    lista_solicitudesEdit: Array,
    lista_productosEdit: Array,
    id: Number,
    _token: String,
  },
  data() {
    return {
      // csrf_token:this._token,
      formContainer: ref(null),
      fullPage: ref(true),
      csrf_token: "",
      datos_documento: {
        id_nc: this.lista_solicitudesEdit[0].ID_NC,
        id_detalle_nc: this.lista_solicitudesEdit[0].ID_DETALLE,
        fecha_emsion: {
          date: new Date(
            this.lista_solicitudesEdit[0].FECHA_EMISION + "T00:00:00"
          ),
        },
        nro_comprobante: this.lista_solicitudesEdit[0].NUMERO_COMPROBANTE,
        importe_total: this.lista_solicitudesEdit[0].IMPORTE_TOTAL,
      },
      detalle_solicitud: {
        fecha_solicitud: {
          date: new Date(
            this.lista_solicitudesEdit[0].FECHA_SOLICITUD + "T00:00:00"
          ),
        },
        motivo: this.lista_solicitudesEdit[0].MOTIVO,
        justificacion: this.lista_solicitudesEdit[0].JUSTIFICACION,
        metodo: this.lista_solicitudesEdit[0].METODO,
      },
      metodo_parcial_productos: {
        products: this.productos,
        value: null,
        selectedOptions: [],
        unidad: {
          unidades: this.unidades,
          valores: Array.from({ length: this.productos.length }, () => ({
            value: null,
          })),
          selectedOptions: [],
        },
        precio: {
          valores: Array.from({ length: this.productos.length }, () => ({
            value: null,
          })),
        },
        cantidad: {
          valores: Array.from({ length: this.productos.length }, () => ({
            value: null,
          })),
        },
        monto_total: {
          valores: Array.from({ length: this.productos.length }, () => ({
            value: null,
          })),
        },
      },
    };
  },
  mounted() {
    this.csrf_token = document.querySelector(
      "[name=csrfmiddlewaretoken]"
    ).value;
  },
  methods: {
    //
    enviarSolicitud() {
      console.log(this.$data.metodo_parcial_productos);
      let jsonString = JSON.stringify(this.$data);
      console.log(jsonString);
      axios
        .post("/solicitud_nota_credito/punto_venta/edit/", jsonString)
        .then((response) => {
          console.log(response);
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
    },
    //
    refreshLoading() {
      const onCancel = () => {
        console.log("User cancelled the loader.");
      };
      let loader = useLoading();
      loader.show({
        // Optional parameters
        container: this.fullPage ? null : formContainer.value,
        canCancel: true,
        onCancel: onCancel,
      });
      setTimeout(() => {
        loader.hide();
      }, 2000);
    },
  },

  created() {
    this.refreshLoading();
  },
};
</script>
<style scope>
@import "https://unpkg.com/vue-multiselect@2.1.6/dist/vue-multiselect.min.css";
</style>

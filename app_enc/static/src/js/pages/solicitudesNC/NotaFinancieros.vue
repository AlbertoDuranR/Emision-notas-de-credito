<template>
  <Header />
  <div class="container px-6 mx-auto block">
    <div class="flex items-center justify-center py-5">
      <span class="font-bold text-gray-600"
        >SOLICITUD NOTA DE CRÉDITO - FINANCIERAS</span
      >
    </div>
    <div class="grid grid-cols-3 pt-2">
      <div class="flex"></div>
      <div class="block mb-10">
        <form action="" v-on:submit.prevent="enviarSolicitud()">
          <div class="relative">
            <loading-overlay
              :active="isLoadingComprobante"
              :can-cancel="true"
              :is-full-page="false"
              :color="'#dc2626'"
            >
            </loading-overlay>
            <div class="py-2">
            <span class="text-sm font-bold text-gray-600 py-5"
              >Datos de Documento Solicitud</span
            >
            </div>
            <div class="space-y-1 py-2">
              <label class="typo__label text-sm">Establecimiento:</label>
              <multiselect
                v-model="datos_documento.establecimiento.value"
                id="multiselect"
                :options="datos_documento.establecimiento.options"
                :preserve-search="true"
                placeholder="Seleccionar local..."
                label="mar_descripcion"
                track-by="mar_descripcion"
              >
              </multiselect>
            </div>
            <div class="space-y-1 py-2">
              <label class="text-sm">Nro. Comprobante:</label>
              <input
                type="text"
                class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
                v-model="datos_documento.nro_comprobante"
                @blur="getDatosDelComprobante"
              />
            </div>
            <div class="space-y-1 py-2">
              <label class="text-sm">Fecha emisión del comprobantes:</label>
              <VueDatePicker
                v-model="datos_documento.fecha_emision.date"
              ></VueDatePicker>
            </div>
            <div class="space-y-1 py-2">
              <label class="text-sm">Importe Real:</label>
              <input
                type="number"
                step="any"
                placeholder="0.00"
                class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
                v-model="datos_documento.importe_real"
                @input="handleDescuentoInput"
              />
            </div>
            <div class="flex space-x-4">
              <div class="space-y-1 py-2">
                <label class="text-sm">Descuento (%):</label>
                <input
                  type="number"
                  class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
                  placeholder="00"
                  v-model="datos_documento.descuento"
                  @input="handleDescuentoInput"
                />
              </div>
              <div class="space-y-1 py-2">
                <label class="text-sm">Total Descuento:</label>
                <input
                  type="number"
                  step="any"
                  placeholder="0.00"
                  class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
                  v-model="datos_documento.total_descuento"
                  disabled
                />
              </div>
            </div>
            <div class="space-y-1 py-2">
              <label class="text-sm">Boleteo:</label>
              <input
                type="number"
                step="any"
                placeholder="0.00"
                class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
                v-model="datos_documento.boleteo"
                disabled
              />
            </div>
          </div>
          <div class="mb-2 relative">
            <loading-overlay
              :active="isLoadingDni"
              :can-cancel="true"
              :is-full-page="false"
              :color="'#dc2626'"
            >
            </loading-overlay>
            <div class="pt-4 pb-1">
            <span class="text-sm font-bold text-gray-600 py-5"
              >Detalle de Solicitante</span
            >
            </div>
            <div class="space-y-1 py-2">
              <label class="text-sm">Fecha emisión de la nota de crédito:</label>
              <VueDatePicker
                v-model="detalle_solicitante.fecha_solicitud.date"
              ></VueDatePicker>
            </div>
            <div class="space-y-1 py-2">
              <label class="text-sm">DNI:</label>
              <input
                type="text"
                class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
                v-model="detalle_solicitante.dni"
                @input="handleDniInput"
                maxlength="8"
              />
            </div>
            <div class="space-y-1 py-2">
              <label class="text-sm">Apellido Materno:</label>
              <input
                type="text"
                class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
                v-model="detalle_solicitante.ap_materno"
                readonly
              />
            </div>
            <div class="space-y-1 py-2">
              <label class="text-sm">Apelido Paterno:</label>
              <input
                type="text"
                class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
                v-model="detalle_solicitante.ap_paterno"
                readonly
              />
            </div>
            <div class="space-y-1 py-2">
              <label class="text-sm">Nombres:</label>
              <input
                type="text"
                class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
                v-model="detalle_solicitante.nombres"
                readonly
              />
            </div>
            <label class="typo__label text-sm">Lugar donde labora:</label>
            <multiselect
              v-model="detalle_solicitante.lugar_donde_labora.value"
              id="multiselect"
              :options="detalle_solicitante.lugar_donde_labora.options"
              :preserve-search="true"
              placeholder="Seleccionar lugar de trabajo..."
              label="mar_descripcion"
              track-by="mar_descripcion"
            >
            </multiselect>
          </div>
          <div class="py-4 px-2 flex justify-center">
            <button
              class="w-60 rounded-full bg-green-600 py-3 text-white font-bold flex justify-center hover:opacity-70"
              type="submit"
            >
              <svg  class="h-5 w-5 text-white"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round">
                <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
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
// Importando layouts
import Header from "../../layouts/Header.vue";
//
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
import LoadingOverlay from 'vue3-loading-overlay';
//
import Multiselect from "vue-multiselect";
//
//
import axios from "axios";
//
import { notify } from "@kyvg/vue3-notification";
import { convertirFormatoFecha } from "../../utils"
</script>
<script>
export default {
  name: "NotaFinancieros",
  components: { VueDatePicker, Multiselect },
  props: {
    lista_markets: Array,
  },
  data() {
    return {
      datos_documento: {
        establecimiento: {
          options: this.lista_markets,
          value: null,
          selectedOptions: [],
        },
        fecha_emision: {
          date: null,
        },
        nro_comprobante: "",
        importe_real: "",
        descuento: "",
        total_descuento: "",
        boleteo: "",
      },
      detalle_solicitante: {
        fecha_solicitud: {
          date: null,
        },
        dni: "",
        ap_materno: "",
        ap_paterno: "",
        nombres: "",
        lugar_donde_labora: {
          options: this.lista_markets,
          value: null,
          selectedOptions: [],
        },
      },
      isLoadingComprobante: false,
      isLoadingDni: false,
    };
  },
  mounted() {
    this.csrf_token = document.querySelector(
      "[name=csrfmiddlewaretoken]"
    ).value;
  },
  methods: {
    handleDniInput() {
      if (this.detalle_solicitante.dni.length === 8) {
        // Execute the query to RENIEC
        this.queryReniec();
        //console.log("CUMPLIO 8");
      }else{
          this.detalle_solicitante.ap_materno = ""
          this.detalle_solicitante.ap_paterno = ""
          this.detalle_solicitante.nombres = ""
      }
    },

    queryReniec() {
      this.isLoadingDni = true
      let jsonString = {
        dni : this.detalle_solicitante.dni
      }

      axios.post("/solicitud_nota_credito/financieros/reniec/", jsonString)
        .then(data => {
          // Handle the RENIEC response
          console.log(data);
          let ap = data["data"]["ap_paterno"]
          let am = data["data"]["ap_materno"]
          let nombres = data["data"]["nombres"]

          //this.reniecData.dni = data.nombres || "";
          this.detalle_solicitante.ap_materno = am
          this.detalle_solicitante.ap_paterno = ap
          this.detalle_solicitante.nombres = nombres

        })
        .catch(error => {
          console.error(error);
          // Handle the error if needed
        })
        .finally(() => {
          this.isLoadingDni = false
        });
    },

    enviarSolicitud() {
      let jsonString = JSON.stringify(this.$data);
      this.isLoading = true;
      axios
        .post("/solicitud_nota_credito/financieros/create/", jsonString)
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
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    async getDatosDelComprobante() {
      if (this.datos_documento.nro_comprobante == '') {
        notify({
          title: 'Verificar Campos',
          text: 'Ingresar Nro Comprobante',
          type: 'warn',
        });
        return;
      }

      this.isLoadingComprobante = true;
      try {
        const response = await axios.get(`/comprobante/get_datos_comprobante/${this.datos_documento.nro_comprobante}`);
        if(response.status == 200 && response.data[0]) {
          this.datos_documento.importe_real = (response.data[0].TotalInvoiceAmount).toFixed(2)
          this.handleDescuentoInput()
          const fechaEmision = response.data[0].InvoiceDate
          this.datos_documento.fecha_emision.date = convertirFormatoFecha(fechaEmision)
        }
      } catch (error) {
        console.log(error)
        this.$swal.fire({
          title: 'Verificar Campos',
          text: `Error con el N° comprobante`,
          icon: 'error',
        });
        this.datos_documento.importe_real='';
        this.datos_documento.fecha_emision.date=null;
      } finally {
        this.isLoadingComprobante = false;
      }
    },

    handleDescuentoInput(){
      const redondearImporteTotal = Math.round(this.datos_documento.importe_real)
      this.datos_documento.total_descuento = (redondearImporteTotal * this.datos_documento.descuento / 100).toFixed(2)
      this.datos_documento.boleteo = (this.datos_documento.importe_real - this.datos_documento.total_descuento).toFixed(2)
    },
  },
};
</script>
<style scope>
@import "https://unpkg.com/vue-multiselect@2.1.6/dist/vue-multiselect.min.css";
</style>

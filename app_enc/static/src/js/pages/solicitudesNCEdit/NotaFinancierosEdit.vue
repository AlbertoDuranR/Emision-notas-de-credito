<template>
  <!-- <Header /> -->
  <div class="container px-6 mx-auto block">
    <div class="flex items-center justify-center py-5">
      <span class="font-bold text-gray-600"
        >EDICION SOLICITUD NOTA DE CRÉDITO - FINANCIERAS - N° {{ id }}</span
      >
    </div>
    <div class="grid grid-cols-3 pt-2">
      <div class="flex"></div>
      <div class="block">
        <form action="" v-on:submit.prevent="enviarSolicitud()">
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
              &nbsp;Actualizar NC
            </button>
          </div>
          <input
              type="text"
              class="hidden mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
              v-model="datos_documento.id_nc"
            />
            <input
              type="text"
              class="hidden mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
              v-model="datos_documento.id_detalle_nc"
            />
            <input
              type="text"
              class="hidden mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
              v-model="datos_documento.id_detalle_cliente"
            />
          <div class="py-2">
            <span class="text-sm font-bold text-gray-600 py-5"
              >Datos de Documento Solicitud</span
            >
          </div>
          <div class="space-y-1 py-2">
            <label class="typo__label text-sm">Establecimiento:</label>
            <multiselect
  v-model="datos_documento.establecimiento.value"
  :options="datos_documento.establecimiento.options"
  :preserve-search="true"
  placeholder="Seleccionar local..."
  label="mar_descripcion"
  track-by="mar_descripcion"
>
</multiselect>
          </div>
          <div class="space-y-1 py-2">
            <label class="text-sm">Fecha emisión del comprobantes:</label>
            <VueDatePicker
              v-model="datos_documento.fecha_emision.date"
            ></VueDatePicker>
          </div>
          <div class="space-y-1 py-2">
            <label class="text-sm">Nro. Comprobante:</label>
            <input
              type="text"
              class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
              v-model="datos_documento.nro_comprobante"
            />
          </div>
          <div class="space-y-1 py-2">
            <label class="text-sm">Importe Real:</label>
            <input
              type="text"
              class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
              v-model="datos_documento.importe_real"
            />
          </div>
          <div class="flex space-x-4">
            <div class="space-y-1 py-2">
              <label class="text-sm">Descuento (%):</label>
              <input
                type="text"
                class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
                v-model="datos_documento.descuento"
              />
            </div>
            <div class="space-y-1 py-2">
              <label class="text-sm">Total Descuento:</label>
              <input
                type="text"
                class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
                v-model="datos_documento.total_descuento"
              />
            </div>
          </div>
          <div class="space-y-1 py-2">
            <label class="text-sm">Boleteo:</label>
            <input
              type="text"
              class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500 disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none invalid:border-pink-500 invalid:text-pink-600 focus:invalid:border-pink-500 focus:invalid:ring-pink-500"
              v-model="datos_documento.boleteo"
            />
          </div>
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
  :options="detalle_solicitante.lugar_donde_labora.options"
  :preserve-search="true"
  placeholder="Seleccionar lugar de trabajo..."
  label="mar_descripcion"
  track-by="mar_descripcion"
>
</multiselect>
          <div class="py-2"></div>
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
//
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
//
import Multiselect from "vue-multiselect";
//
//
import axios from "axios";
//
import { notify } from "@kyvg/vue3-notification";
//
</script>
<script>
export default {
  name: "NotaFinancierosEdit",
  components: { VueDatePicker, Multiselect },
  props: {
    lista_solicitudesEdit: Array,
    lista_markets: Array,
    id: Number
  },
  data() {
    return {
      datos_documento: {
        id_nc: "",
        id_detalle_nc: "",
        id_detalle_cliente: "",
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
    };
  },

  computed: {

    
    defaultEstablecimiento() {
      return this.datos_documento.establecimiento.options.find(option => option.mar_id ===  parseInt(this.lista_solicitudesEdit[0].ID_ESTABLECIMIENTO));
    },
    defaultLugarLabora() {
    return this.detalle_solicitante.lugar_donde_labora.options.find(option => option.mar_id === parseInt(this.lista_solicitudesEdit[0].ID_MARKET));
  },
  },
  mounted() {
    this.csrf_token = document.querySelector(
      "[name=csrfmiddlewaretoken]"
    ).value;




    // Usamos $nextTick para asegurarnos de que el componente se haya renderizado completamente
    this.$nextTick(() => {
      // Establecemos el valor predeterminado usando la propiedad computada
      this.datos_documento.establecimiento.value = this.defaultEstablecimiento;
    });

    // Usamos $nextTick para asegurarnos de que el componente se haya renderizado completamente
    this.$nextTick(() => {
      // Establecemos el valor predeterminado usando la propiedad computada
      this.detalle_solicitante.lugar_donde_labora.value = this.defaultLugarLabora;
    });


    let solicitud = this.lista_solicitudesEdit[0];

    console.log(this.lista_solicitudesEdit[0].ID_MARKET);

    this.datos_documento.id_nc = solicitud.ID_NC;
    this.datos_documento.id_detalle_nc = solicitud.ID_DETALLE;
    this.datos_documento.id_detalle_cliente = solicitud.ID_DETALLE_SOLICITANTE;

    this.datos_documento.fecha_emision.date = new Date(solicitud.FECHA_EMISION + "T00:00:00");
    this.datos_documento.nro_comprobante = solicitud.NRO_COMPROBANTE;
    this.datos_documento.importe_real = solicitud.IMPORTE_REAL;
    this.datos_documento.descuento =  Math.floor(solicitud.DESCUENTO);
    this.datos_documento.total_descuento = solicitud.TOTAL_DESCUENTO;
    this.datos_documento.boleteo = solicitud.BOLETEO;

    this.detalle_solicitante.fecha_solicitud.date = new Date(solicitud.FECHA_SOLICITUD + "T00:00:00");
    this.detalle_solicitante.dni = solicitud.DNI;
    this.detalle_solicitante.ap_materno = solicitud.APELLIDO_MATERNO;
    this.detalle_solicitante.ap_paterno = solicitud.APELLIDO_PATERNO;
    this.detalle_solicitante.nombres = solicitud.NOMBRES;
    this.detalle_solicitante.lugar_donde_labora.value = solicitud.ID_MARKET;

  },
  methods: {
    //
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
        });
    },
    enviarSolicitud() {
      let jsonString = JSON.stringify(this.$data);
      axios
        .post("/solicitud_nota_credito/financieros/edit/", jsonString)
        .then((response) => {
          console.log(response);
         // Mostrar SweetAlert 2
        this.$swal
          .fire({
            title: "Solicitud Editada",
            text: "seleccione ok para dirigirse al consolidado",
            icon: "success",
            showConfirmButton: true,
            allowOutsideClick: false,
          })
          .then(() => {
            // Después de que se complete la animación de SweetAlert 2
            // Ejecutar la visita a la ruta de Inertia
            this.$inertia.visit(`/consolidacion_nota_credito/financieros/`);
          });

        })
        .catch((err) => {
          console.log(err);
          notify({
            title: "Error de Registro",
            text: "Error al actualizar datos verificar los campos",
            type: "error",
          });
        });
    },
  },
};
</script>
<style scope>
@import "https://unpkg.com/vue-multiselect@2.1.6/dist/vue-multiselect.min.css";
</style>
